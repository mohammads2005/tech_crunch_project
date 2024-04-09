from django.shortcuts import render

from .tasks import by_keyword_scraper, daily_scraper
from .forms import UserSearchForm, CategoryReportForm

# Create your views here.


def user_search_view(request):
    if request.method == "POST":
        search_form = UserSearchForm(request.POST,)
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
    
    return render(request, "techcrunch/user_search.html", {'form': search_form})


def category_report_view(request):
    if request.method == "POST":
        report_form = CategoryReportForm(request.POST,)
        if report_form.is_valid():
            pass
