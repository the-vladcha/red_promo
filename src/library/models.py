from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone


class Reader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return ' '.join((self.last_name, self.first_name, self.middle_name))

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Item(models.Model):
    class Status(models.IntegerChoices):
        RESERVED = 1
        NOT_RETURNED = 2

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_items')
    current_reader = models.ForeignKey(Reader, on_delete=models.PROTECT, related_name='reader_items')
    status = models.IntegerField(choices=Status.choices, default=Status.RESERVED)
    reserved_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class History(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    reader = models.ForeignKey(Reader, on_delete=models.SET_NULL, null=True)
    reserved_at = models.DateTimeField(default=timezone.now)
    reserved_to = models.DateTimeField(blank=True, null=True)
    overdue = models.BooleanField(default=False)


@receiver(post_delete, sender=Item)
def create_profile(sender: Item, instance: Item, *args, **kwargs) -> None:
    History.objects.create(
        book=instance.book,
        reader=instance.current_reader,
        reserved_at=instance.reserved_at,
        reserved_to=timezone.now(),
    )


@receiver(post_save, sender=Item)
def create_profile(sender: Item, instance: Item, *args, **kwargs) -> None:
    if instance.status == Item.Status.NOT_RETURNED.value:
        History.objects.create(
            book=instance.book,
            reader=instance.current_reader,
            reserved_at=instance.reserved_at,
            overdue=True,
        )
