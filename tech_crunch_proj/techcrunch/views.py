from django.shortcuts import render
from .forms import UserKeywordSearchForm, CategoryReportForm

# Create your views here.


def user_search_view(request):
    if request.method == "POST":
        search_form = UserKeywordSearchForm(request.POST,)
        if search_form.is_valid():
            pass


def category_report_view(request):
    if request.method == "POST":
        report_form = CategoryReportForm(request.POST,)
        if report_form.is_valid():
            pass
