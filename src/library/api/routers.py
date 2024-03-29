from django.urls import path
from rest_framework.routers import DefaultRouter

from library.api.views import ReaderViewSet, BookViewSet, ItemViewSet, ImportDataApiView, ExportReportApiView

router = DefaultRouter()
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'books', BookViewSet, basename='book')
router.register(r'items', ItemViewSet, basename='item')
urlpatterns = [
  path('import_books/', ImportDataApiView.as_view()),
  path('export_reader_report/', ExportReportApiView.as_view())
] + router.urls
