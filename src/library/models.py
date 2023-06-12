from django.db import models


class Reader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

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


# class History(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL)
#     reader = models.ForeignKey(Reader, on_delete=models.SET_NULL)
#     reserved_at = models.DateTimeField(default=timezone.now)
#     reserved_to = models.DateTimeField(blank=True, null=True)
#     overdue = models.BooleanField(default=False)
