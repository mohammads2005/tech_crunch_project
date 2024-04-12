import os
import logging

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

from .tasks import by_keyword_scraper, daily_scraper, category_report
from .forms import UserSearchForm, CategoryReportForm, ExportForm
from .resources import AuthorResource, CategoryResource, ArticleResource


view_logger = logging.getLogger("techcrunch.view")

# Create your views here.


def user_search_view(request):
    if request.method == "POST":
        view_logger.info("Runnig user_search_view with POST method")

        search_form = UserSearchForm(
            request.POST,
        )
        if search_form.is_valid():
            view_logger.info("The POSTED data are valid in user_search_view")

            if search_form.cleaned_data["search_type"] == "by_keyword":
                view_logger.info("Searching By Keyword in user_search_view")

                result = by_keyword_scraper.delay(
                    keyword=search_form.cleaned_data["keyword"],
                    page_count=search_form.cleaned_data["page_count"],
                )

            elif search_form.cleaned_data["search_type"] == "daily_search":
                view_logger.info("Running a Daily Search in user_search_view")

                result = daily_scraper.delay()

    else:
        view_logger.info(
            "Running GET, DELETE or any method other than POST in user_search_view"
        )

        search_form = UserSearchForm()

    return render(request, "techcrunch/user_search.html", {"form": search_form})


def category_report_view(request):
    if request.method == "POST":
        view_logger.info("Runnig category_report_view with POST method")

        report_form = CategoryReportForm(
            request.POST,
        )
        if report_form.is_valid() and report_form.cleaned_data["report"] == "show":
            view_logger.info("The POSTED data are valid in category_report_view")

            category_report()
        else:
            view_logger.error("Invalid POST in category_report_view")

    else:
        view_logger.info(
            "Running GET, DELETE or any method other than POST in category_report_view"
        )

        report_form = CategoryReportForm()

    return render(request, "techcrunch/category_report.html", {"form": report_form})


def export_view(request):
    if request.method == "POST":
        view_logger.info("Runnig export_view with POST method")

        export_form = ExportForm(
            request.POST,
        )

        if export_form.is_valid():
            view_logger.info("The POSTED data are valid in export_view")

            resource_type = export_form.cleaned_data["resource_type"]
            file_format = export_form.cleaned_data["file_format"]

            match resource_type:
                case "article":
                    resource_instance = ArticleResource()

                    view_logger.info("Resource is set to Article in export_view")

                case "author":
                    resource_instance = AuthorResource()
                    
                    view_logger.info("Resource is set to Author in export_view")

                case "category":
                    resource_instance = CategoryResource()

                    view_logger.info("Resource is set to Category in export_view")

            dataset = resource_instance.export()

            match file_format:
                case "json":
                    response = HttpResponse(
                        dataset.json, content_type="application/json"
                    )
                    response["Content-Disposition"] = (
                        f'attachment;filename="{resource_type}.json"'
                    )

                    view_logger.info("Output file is set to JSON in export_view")

                case "csv":
                    response = HttpResponse(dataset.csv, content_type="text/csv")
                    response["Content-Disposition"] = (
                        f'attachment;filename="{resource_type}.csv"'
                    )
                    
                    view_logger.info("Output file is set to JSON in export_view")

                case "xls":
                    response = HttpResponse(
                        dataset.xls, content_type="application/vnd.ms-excel"
                    )
                    response["Content-Disposition"] = (
                        f'attachment;filename="{resource_type}.xls"'
                    )

                    view_logger.info("Output file is set to JSON in export_view")

        return response

    else:
        view_logger.info(
            "Running GET, DELETE or any method other than POST in export_view"
        )

        export_form = ExportForm()
        return render(request, "techcrunch/export_options.html", {"form": export_form})


def export_zip_download(request, file_name):
    view_logger.info("Running export_zip_download")

    file_path = os.path.join(settings.BASE_DIR, f"{file_name}.zip")

    response = FileResponse(open(file_path, "rb"))
    response["Content-Type"] = "application/zip"
    response["Content-Disposition"] = "attachment;filename={}".format(
        f"{file_name}.zip"
    )

    return response
