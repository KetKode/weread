import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    selected_genres = django_filters.MultipleChoiceFilter(
        field_name='main_genre',
        choices=Book.objects.values_list('main_genre', 'main_genre').distinct(),
        widget=django_filters.widgets.CSVWidget(),
    )

    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author__name': ['icontains'],
        }