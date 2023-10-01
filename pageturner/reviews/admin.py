from django.contrib import admin
from .models import Publisher, Book, Review, Author
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class BookResource(resources.ModelResource):
    class Meta:
        model = Book

    def before_import_row(self, row, **kwargs):
        author_name = row.get('author')  # Assuming 'author' is the column name in your CSV file

        # Try to get the Author instance by name, or create it if it doesn't exist
        author, created = Author.objects.get_or_create(name=author_name)

        # Update the 'author' field in the row with the Author instance
        row['author'] = author.id  # Assuming 'author' is the foreign key field in your Book model


class BookAdmin(ImportExportModelAdmin):
    resource_classes = [BookResource]


admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Review)