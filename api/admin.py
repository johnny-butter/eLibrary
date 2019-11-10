from django.contrib import admin
from api.models import Book, bookType

# Register your models here.
admin.site.register(Book)
admin.site.register(bookType)
