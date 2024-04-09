from django.contrib import admin
from django.contrib.admin import register
from .models import Author, Category, Article, KeyWord, UserKeywordSearch, DailySearch, ArticleSearchByKeyword

# Register your models here.


@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "profile", "created_date")
    list_display_links = ("id", "full_name")
    list_filter = ("created_date",)


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "link", "created_date")
    list_display_links = ("id", "category_name")
    list_filter = ("created_date",)


@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "headline", "image", "created_date", "modified_date")
    list_display_links = ("id", "headline")
    list_filter = ("author", "categories", "created_date")


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
    list_filter = ("created_date",)
