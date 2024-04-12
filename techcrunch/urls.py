from django.urls import path
from .views import user_search_view, category_report_view, export_view, export_zip_download


urlpatterns = [
    path("user_search", user_search_view),
    path("category_report", category_report_view),
    path("export", export_view),
    path("exported-zipped-file/<slug:file_name>", export_zip_download),
]
