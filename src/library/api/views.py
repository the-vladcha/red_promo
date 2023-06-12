from rest_framework import viewsets, mixins, views, status
from rest_framework.request import Request
from rest_framework.response import Response

from app.settings import BASE_DIR
from library.api.serializers import ReaderSerializer, BookSerializer, ItemSerializer, DataImportSerializer
from library.models import Reader, Book, Item
from library.tasks import import_csv


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
