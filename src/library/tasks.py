import csv
from pathlib import Path

from celery import shared_task
from django.utils import timezone

from app.celery import app
from app.settings import BASE_DIR
from library.models import Book, Item


@shared_task()
def import_csv(filename):
    path = Path(BASE_DIR, 'data', filename)
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            Book.objects.create(
                title=row[0],
                author=row[1],
                genre=row[2],
                amount=row[3],
            )


@app.task
def update_item_status():
    Item.objects.filter(
        status=Item.Status.RESERVED,
        reserved_at__lt=timezone.now() - 14).update(status=Item.Status.NOT_RETURNED.value)
