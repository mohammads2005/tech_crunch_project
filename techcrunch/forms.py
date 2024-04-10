from django import forms


class UserSearchForm(forms.Form):
    SEARCH_TYPE = (
        ("by_keyword", "By Keyword"),
        ("daily_search", "Daily Search")
    )
    search_type = forms.ChoiceField(label="Search Type", choices=SEARCH_TYPE,)
    keyword = forms.CharField(label="Keyword", max_length=255)
    page_count = forms.IntegerField(
        label="Number of Pages to Search", max_value=100, min_value=1, initial=1
    )


class CategoryReportForm(forms.Form):
    REPORT_STATUS = (
        ("show", "SHOW"),
        ("dont_show", "Don't SHOW"),
    )
    report = forms.ChoiceField(
        label="Select Category",
        choices=REPORT_STATUS,
    )


class ExportForm(forms.Form):
    FILE_FORMATS = (
        ("json", "JSON"),
        ("csv", "CSV"),
        ("xls", "XLS"),
    )
    RESOURCE_TYPES = (
        ("article", "Article"),
        ("author", "Author"),
        ("category", "Category"),
    )

    file_format = forms.ChoiceField(
        label="File Format",
        choices=FILE_FORMATS,
    )
    resource_type = forms.ChoiceField(
        label="Resource Type",
        choices=RESOURCE_TYPES,
    )
