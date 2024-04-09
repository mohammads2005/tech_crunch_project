from import_export import resources, fields, widgets
from .models import Author, Category, Article


class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
        fields = ("id", "full_name", "profile", "created_date")


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ("id", "category_name", "link", "created_date")


class ArticleResource(resources.ModelResource):
    categories = fields.Field(
        column_name="categories",
        attribute="categories",
        widget=widgets.ManyToManyWidget(Category, ","),
    )
    author = fields.Field(
        column_name="author",
        attribute="author",
        widget=widgets.ForeignKeyWidget(Author, "full_name"),
    )

    class Meta:
        model = Article
        fields = (
            "id",
            "headline",
            "author",
            "categories",
            "url",
            "content",
            "image",
            "created_date",
            "modified_date",
        )
