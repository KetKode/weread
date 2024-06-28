import django_filters

from .models import Book, BookCollection


class BookFilter(django_filters.FilterSet):
    selected_genres = django_filters.MultipleChoiceFilter(
        field_name="main_genre",
        choices=Book.objects.values_list("main_genre", "main_genre").distinct(),
        widget=django_filters.widgets.CSVWidget(),
    )

    selected_age = django_filters.MultipleChoiceFilter(
        field_name="age",
        choices=Book.objects.values_list("main_age", "main_age").distinct(),
        widget=django_filters.widgets.CSVWidget(),
    )

    book_lists = django_filters.ModelMultipleChoiceFilter(
        field_name="name",
        queryset=BookCollection.objects.all(),
        widget=django_filters.widgets.CSVWidget(),
    )

    selected_format = django_filters.ModelMultipleChoiceFilter(
        field_name="format_book",
        choices=Book.objects.values_list("format_book", "format_book").distinct(),
        widget=django_filters.widgets.CSVWidget(),
    )

    selected_language = django_filters.ModelMultipleChoiceFilter(
        field_name="language",
        choices=Book.objects.values_list("language", "language").distinct(),
        widget=django_filters.widgets.CSVWidget(),
    )

    year_range = django_filters.RangeFilter(field_name="year")

    class Meta:
        model = Book
        fields = {"title": ["icontains"], "author__name": ["icontains"]}
