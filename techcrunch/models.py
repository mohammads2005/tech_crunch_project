from abc import abstractmethod
from django.db import models
from datetime import datetime
from django.utils.html import mark_safe


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
    full_name = models.CharField(max_length=55, verbose_name="Full Name")
    profile = models.URLField(max_length=255, verbose_name="Tech Crunch Profile")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ("full_name",)

    def __str__(self) -> str:
        return self.full_name


class Category(BaseModel):
    id = models.IntegerField(primary_key=True, verbose_name="Category's ID")
    category_name = models.CharField(max_length=255, verbose_name="Category's Name")
    link = models.URLField(max_length=255, verbose_name="Category's Link")

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
    url = models.URLField(max_length=255, verbose_name="Article's Link")
    content = models.TextField(verbose_name="Article's Content")
    categories = models.ManyToManyField(
        Category, related_name="article", verbose_name="Categories"
    )
    image = models.ImageField(upload_to="media/", verbose_name="Image")

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="max-width:50px; max-height:50px" />')
        else:
            return "No Image Found!"

    image_tag.short_description = "Image"

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return self.headline[:10]


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
    articles = models.ForeignKey(
        Article,
        related_name="dailysearch",
        verbose_name="Articles",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    headline = models.TextField(verbose_name="Headline")
    url = models.URLField(max_length=255, verbose_name="Article's Link")
    is_scraped = models.BooleanField(default=False, verbose_name="Is Scraped")

    class Meta:
        verbose_name = "Daily Search"

    def __str__(self) -> str:
        return str(self.created_date)


class ArticleSearchByKeyword(BaseModel):
    user_keyword_search = models.ForeignKey(
        UserKeywordSearch,
        related_name="article_search_by_keyword",
        verbose_name="User Keyword Search",
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        related_name="article_search_by_keyword",
        verbose_name="Article",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    headline = models.TextField(verbose_name="Headline")
    url = models.URLField(max_length=255, verbose_name="Article's Link")
    is_scraped = models.BooleanField(default=False, verbose_name="Is Scraped")

    def __str__(self) -> str:
        return self.headline[:10]
