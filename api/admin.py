from django.contrib import admin
from api.models import Book, BookType

# Register your models here.
admin.site.register(Book)
admin.site.register(BookType)
