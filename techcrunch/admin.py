import logging
from datetime import datetime

from django.contrib import admin
from django.conf import settings
from django.contrib.admin import register

from import_export.admin import ExportActionModelAdmin

from .tasks import export_data
from .resources import AuthorResource, CategoryResource, ArticleResource
from .models import (
    Author,
    Category,
    Article,
    KeyWord,
    UserKeywordSearch,
    DailySearch,
    ArticleSearchByKeyword,
)

admin_logger = logging.getLogger(name="techcrunch.admin")

# Register your models here.


@register(Author)
class AuthorAdmin(ExportActionModelAdmin):
    resource_classes = [AuthorResource]
    list_display = ("id", "full_name", "profile", "created_date")
    list_display_links = ("id", "full_name")
    list_filter = ("created_date",)


@register(Category)
class CategoryAdmin(ExportActionModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ("id", "category_name", "link", "created_date")
    list_display_links = ("id", "category_name")
    list_filter = ("created_date",)


@register(Article)
class ArticleAdmin(ExportActionModelAdmin):
    resource_classes = [ArticleResource]
    list_display = ("id", "headline", "image_tag", "created_date", "modified_date")
    readonly_fields = ("image_tag",)
    list_display_links = ("id", "headline")
    list_filter = ("created_date",)

    def export_admin_action(self, request, queryset):
        time_now = datetime.now()
        time_now_string = time_now.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f"export-{time_now_string}"

        for article in queryset:
            try:
                export_data.delay(
                    image=article.image,
                    html_source=article.html_source,
                    id=article.id,
                    file_name=file_name,
                    slug=file_name,
                )
                
                admin_logger.info = (f"Exported data from article with id: {article.id}")
                
            except:
                admin_logger.error(f"Error occured while trying to export data from article: {article.id}")

        return super().export_admin_action(request, queryset)


@register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "created_date")
    list_display_links = ("id", "word")
    list_filter = ("created_date",)


@register(UserKeywordSearch)
class UserKeywordSearchAdmin(admin.ModelAdmin):
    list_display = ("id", "keyword", "page_count", "created_date")
    list_display_links = ("id",)
    list_filter = ("created_date",)


@register(DailySearch)
class DailySearchAdmin(admin.ModelAdmin):
    list_display = ("id", "headline", "is_scraped", "url", "created_date")
    list_display_links = ("id", "headline")
    list_filter = ("created_date",)


@register(ArticleSearchByKeyword)
class ArticleSearchByKeywordAdmin(admin.ModelAdmin):
    list_display = ("id", "headline", "is_scraped", "url", "created_date")
    list_display_links = ("id", "headline")
    list_filter = ("created_date", "is_scraped")
