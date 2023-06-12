from datetime import timedelta

from rest_framework import serializers

from library.models import Reader, Book, Item


class BookSerializer(serializers.ModelSerializer):
    in_stock_count = serializers.SerializerMethodField()
    next_return = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'amount', 'in_stock_count', 'next_return')

    def get_in_stock_count(self, obj: Book):
        return obj.amount - obj.book_items.all().count()

    def get_next_return(self, obj: Book):
        if self.get_in_stock_count(obj) == 0:
            latest_item: Item = obj.book_items.filter(status=Item.Status.RESERVED.value).latest("reserved_at")
            if latest_item:
                return latest_item.reserved_at + timedelta(days=14)
        return None


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'passport_number')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('book', 'current_reader', 'status')


class DataImportSerializer(serializers.Serializer):
    filename = serializers.FilePathField(path='data', match=r".*\.csv$")
