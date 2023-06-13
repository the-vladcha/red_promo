import csv

from django.db.models import Count
from django.http import HttpResponse
from rest_framework import viewsets, mixins, views, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.settings import BASE_DIR
from library.api.serializers import ReaderSerializer, BookSerializer, ItemSerializer, DataImportSerializer
from library.models import Reader, Book, Item
from library.tasks import import_csv

from src.library.models import History


class ReaderViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ReaderSerializer
    queryset = Reader.objects.all()


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class ItemViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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

    def post(self, request: Request):
        import_csv.delay(request.data.get("filename"))
        # serializer = DataImportSerializer(data=request.data)
        # print(serializer)
        # serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        # Book.import_data(data=open(filename))
        # import_csv.delay(filename)
        return Response({}, status=status.HTTP_201_CREATED)


class ExportReportApiView(views.APIView):

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        writer.writerow(';'.join(('reader', 'number_of_books_read')))
        for reader_static in History.objects.values('reader').annotate(rcount=Count('reader')).order_by('reader'):
            row: str = ';'.join([
                reader_static.reader.full_name,
                reader_static.rcount,
            ])
            writer.writerow(row)

        return response
