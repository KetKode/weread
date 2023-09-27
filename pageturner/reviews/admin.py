from django.contrib import admin
from .models import Publisher, Book, Review, Author

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Review)

