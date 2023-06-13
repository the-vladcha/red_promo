import csv
from pathlib import Path

from django.db.models import Count, QuerySet
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, mixins, views, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.settings import BOOKS_PATH
from library.api.serializers import ReaderSerializer, BookSerializer, ItemSerializer
from library.models import Reader, Book, Item, History
from library.tasks import import_csv


class ReaderViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ReaderSerializer
    queryset = Reader.objects.all()


class BookViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class ItemViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book: Book = serializer.validated_data['book']
        if book.amount - Item.objects.filter(book=serializer.validated_data['book']).count() > 0:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"content": "The book is out of stock"}, status=status.HTTP_400_BAD_REQUEST)


class ImportDataApiView(views.APIView):

    def post(self, request: Request) -> Response:
        filename: str | None = request.data.get("filename")
        if filename and filename.endswith('.csv') and Path(BOOKS_PATH, filename).exists():
            import_csv.delay(request.data.get("filename"))
            return Response({}, status=status.HTTP_201_CREATED)
        return Response({"error": "Bad filename"}, status=status.HTTP_400_BAD_REQUEST)


class ExportReportApiView(views.APIView):

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reader_report.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['reader', 'number_of_books_read'])
        reader_statistics: QuerySet = History.objects \
            .filter(reserved_at__gte=timezone.now() - timezone.timedelta(days=30)) \
            .values('reader').annotate(rcount=Count('reader')).order_by('reader')
        for reader_statistic in reader_statistics:
            row: list = [
                Reader.objects.get(pk=reader_statistic.get('reader')).full_name,
                str(reader_statistic.get('rcount')),
            ]
            writer.writerow(row)

        return response
