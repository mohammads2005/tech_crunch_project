from unicodedata import category
from django import forms
from .models import Category


class UserKeywordSearchForm(forms.Form):
    EXPORT_TYPE = (
        ("csv", "CSV"),
        ("json", "JSON"),
        ("xls", "XLS"),
    )
    keyword = forms.CharField(label="Keyword", max_length=255)
    page_count = forms.IntegerField(
        label="Number of Pages to Search", max_value=100, min_value=1, initial=1
    )
    file_type = forms.CharField(
        label="File Type",
        widget=forms.Select(choices=EXPORT_TYPE),
        initial="JSON",
    )


class CategoryReportForm(forms.Form):
    category_select = forms.ChoiceField(
        label="Select Category",
        choices=(),
        initial=None,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        searched_categories = Category.objects.values_list("category_name", flat=True)
        CATEGORIES = tuple((category, category) for category in searched_categories)
        self.fields["category_select"].choices = CATEGORIES
