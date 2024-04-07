from abc import abstractmethod
import keyword
from sre_parse import CATEGORIES
from tabnanny import verbose
from tkinter.tix import Tree
from unicodedata import category
from django.db import models
from datetime import datetime

from django.forms import IntegerField

# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        abstract = True
        ordering = ("pk",)

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Please implement __str__ method")


class Author(BaseModel):
    id = models.IntegerField(primary_key=True, verbose_name="Author's ID")
    full_name = models.CharField(max_length=50, verbose_name="Full Name")
    profile = models.URLField(max_length=100, verbose_name="Tech Crunch Profile")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ("full_name",)

    def __str__(self) -> str:
        return self.full_name


class Category(BaseModel):
    id = models.IntegerField(primary_key=True, verbose_name="Category's ID")
    category_name = models.CharField(max_length=50, verbose_name="Category's Name")
    link = models.URLField(max_length=50, verbose_name="Category's Link")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("category_name",)

    def __str__(self) -> str:
        return self.category_name


class Article(BaseModel):
    id = models.IntegerField(primary_key=True, verbose_name="Article's ID")
    headline = models.TextField(verbose_name="Headline")
    author = models.ForeignKey(
        Author, 
        related_name="article",
        verbose_name="Author", 
        on_delete=models.CASCADE,
    )
    url = models.URLField(max_length=200, verbose_name="Article's Link")
    content = models.TextField(verbose_name="Article's Content")
    categories = models.ManyToManyField(
        Category, related_name="article", verbose_name="Categories"
    )
    image = models.URLField(max_length=200, verbose_name="Image Link")
    is_scraped = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return self.headline


class KeyWord(BaseModel):
    word = models.CharField(max_length=255, verbose_name="Keyword")

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self) -> str:
        return self.word


class UserKeywordSearch(BaseModel):
    keyword = models.ForeignKey(
        KeyWord,
        related_name="usersearch",
        verbose_name="Keyword",
        on_delete=models.CASCADE,
    )
    page_count = models.IntegerField(default=1, verbose_name="Total Pages to Search")

    class Meta:
        verbose_name = "User Search"

    def __str__(self) -> str:
        return self.keyword.word


class DailySearch(BaseModel):
    articles = models.ManyToManyField(
        Article, related_name="dailysearch", verbose_name="Articles", blank=True
    )

    class Meta:
        verbose_name = "Daily Search"

    def __str__(self) -> str:
        return str(self.created_date)
