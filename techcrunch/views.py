from django.shortcuts import render
from django.http import HttpResponse

from .tasks import by_keyword_scraper, daily_scraper, category_report
from .forms import UserSearchForm, CategoryReportForm, ExportForm
from .resources import AuthorResource, CategoryResource, ArticleResource

# Create your views here.


def user_search_view(request):
    if request.method == "POST":
        search_form = UserSearchForm(
            request.POST,
        )
        if search_form.is_valid():
            if search_form.cleaned_data["search_type"] == "by_keyword":
                result = by_keyword_scraper.delay(
                    keyword=search_form.cleaned_data["keyword"],
                    page_count=search_form.cleaned_data["page_count"],
                )

            elif search_form.cleaned_data["search_type"] == "daily_search":
                result = daily_scraper.delay()

    else:
        search_form = UserSearchForm()

    return render(request, "techcrunch/user_search.html", {"form": search_form})


def category_report_view(request):
    if request.method == "POST":
        report_form = CategoryReportForm(
            request.POST,
        )
        if report_form.is_valid() and report_form.cleaned_data["report"] == "show":
            category_report()

    else:
        report_form = CategoryReportForm()
    
    return render(request, "techcrunch/category_report.html", {"form": report_form})


def export_view(request):
    if request.method == "POST":
        export_form = ExportForm(request.POST,)
        
        if export_form.is_valid():
            resource_type = export_form.cleaned_data["resource_type"]
            file_format = export_form.cleaned_data["file_format"]

            match resource_type:
                case "article":
                    resource_instance = ArticleResource()

                case "author":
                    resource_instance = AuthorResource()

                case "category":
                    resource_instance = CategoryResource()

            dataset = resource_instance.export()

            match file_format:
                case "json":
                    response = HttpResponse(dataset.json, content_type="application/json")
                    response["Content-Disposition"] = f'attachment;filename="{resource_type}.json"'

                case "csv":
                    response = HttpResponse(dataset.csv, content_type="text/csv")
                    response["Content-Disposition"] = f'attachment;filename="{resource_type}.csv"'
                
                case "xls":
                    response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
                    response["Content-Disposition"] = f'attachment;filename="{resource_type}.xls"'

        return response

    else:
        export_form = ExportForm()
        return render(request, "techcrunch/export_options.html", {"form": export_form})
