import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from .models import Author, Article, Category, ArticleSearchByKeyword, DailySearch


class ScraperHandler:
    def __init__(self, base_url, search_url, json_url) -> None:
        self.base_url = base_url # The URL to use for daily search in techcrunch.com
        self.search_url = search_url  # The URL to search for the user-entered keyword
        self.json_url = json_url  # The URL for receiving raw json data of articles, categories and authors

    def send_request(self, url):
        """ Simply tries sending a GET request to the target URL

        Args:
            url (str): Target URL

        Returns:
            response: The response from the get request to the URL 
        """

        try:
            response = requests.get(url=url)

        except requests.RequestException as error:
            print(
                f"An error occured while trying to send request to {url}!",
                error,
                sep="\n",
            )
            exit()

        else:
            return response

    def daily_search(self):
        daily_articles = list()

        response = self.send_request(url=self.base_url)
        if response.status_code == 200:
            page_soup = BeautifulSoup(response.text, "html.parser")
            articles = page_soup.find_all("a", attrs={"class", "post-block__title__link"})

            daily_articles += self.parse_daily_item(articles=articles)
            slugs = self.slug_parser(articles=articles)

        for i, slug in enumerate(slugs):
            parsed_article = self.article_parser(slug=slug)
            item_to_complete = daily_articles[i]
            item_to_complete.article = parsed_article
            item_to_complete.is_scraped = True
            item_to_complete.save()

        return len(daily_articles)

    def search_by_keyword(self, usersearch_instance):
        """ By receving the user-input values as an instance of the UserKeywordSearch,
            starts scraping the given number of pages for the given keyword 

        Args:
            usersearch_instance (<class 'UserKeywordSearch'>): An instance of user's inputs

        Returns:
            int: Total number of scraped items
        """

        search_articles = list()
        index = 0

        for i in range(usersearch_instance.page_count):
            response = self.send_request(
                url=self.search_url.format(
                    keyword=usersearch_instance.keyword,
                    page=i,
                )
            )

            if response.status_code == 200:
                page_soup = BeautifulSoup(response.text, "html.parser")
                articles = page_soup.find_all("a", {"class": "thmb"})
                search_articles += self.parse_search_item(
                    articles=articles,
                    usersearch_instance=usersearch_instance,
                )
                articles_slugs = self.slug_parser(articles=articles)

            for slug in articles_slugs:
                parsed_article = self.article_parser(slug=slug)
                item_to_complete = search_articles[index]
                item_to_complete.article = parsed_article
                item_to_complete.is_scraped = True
                item_to_complete.save()
                index += 1

        return len(search_articles)

    def slug_parser(self, articles):
        """ A parser to return the end of a URL known as 'slug'

        Args:
            soup (<class 'BeautifulSoup'>): HTML-parsed source code of the page 

        Returns:
            str: The srting refering to the 'slug' of an article's URL  
        """
        slugs = list()

        for article in articles:
            slugs.append(article["href"].split("/")[-2])

        return slugs

    def parse_daily_item(self, articles):
        daily_articles = list()

        for article in articles:
            daily_search_item = DailySearch.objects.create(
                headline=article.text,
                url=article["href"],
            )

            daily_articles.append(daily_search_item)

        return daily_articles

    def parse_search_item(self, articles, usersearch_instance):
        search_articles = list()

        for article in articles:
            article_search_item = ArticleSearchByKeyword.objects.create(
                user_keyword_search=usersearch_instance,
                headline=article.text,
                url=article["href"],
            )
            search_articles.append(article_search_item)

        return search_articles

    def article_parser(self, slug):
        categories = list()

        article_response_json = self.send_request(
            url=self.json_url.format(
                model="posts?",
                search_type=f"slug={slug}",
            )
        ).json()
        article_response_json = article_response_json[0]

        author = self.author_parser(id=article_response_json["author"])
        content = self.content_parser(article_response_json["content"])
        headline = self.headline_parser(article_response_json["title"])
        image_url = article_response_json["yoast_head_json"]["og_image"][0]["url"]

        for category_id in article_response_json["categories"]:
            categories.append(self.category_parser(id=category_id))

        try:
            article, _ = Article.objects.get_or_create(
                id=article_response_json["id"],
                headline=headline,
                author=author,
                url=article_response_json["link"],
                content=content,
                image=image_url,
                created_date=article_response_json["date"],
                modified_date=article_response_json["modified"],
            )
            article.categories.add(*categories)
            article.save()

        except IntegrityError:
            return None

        return article

    def author_parser(self, id):
        author_response_json = self.send_request(
            url=self.json_url.format(
                model="users/",
                search_type=id,
            )
        ).json()

        if type(author_response_json) == list:
            author_response_json = author_response_json[0]

        try:
            author, _ = Author.objects.get_or_create(
                id=id,
                full_name=author_response_json["name"],
                profile=author_response_json["link"],
            )

        except IntegrityError:
            return None

        return author

    def category_parser(self, id):
        category_response_json = self.send_request(
            url=self.json_url.format(
                model="categories/",
                search_type=id,
            )
        ).json()

        if type(category_response_json) == list:
            category_response_json = category_response_json[0]

        category_name = BeautifulSoup(category_response_json["name"], "html.parser")
        
        try:
            category, _ = Category.objects.get_or_create(
                id=id,
                category_name=category_name.text,
                description=category_response_json["description"],
                link=category_response_json["link"],
            )

        except IntegrityError:
            return None

        return category

    def content_parser(self, raw_content):
        content_soup = BeautifulSoup(raw_content["rendered"], "html.parser")

        return content_soup.text

    def headline_parser(self, raw_headline):
        headline_soup = BeautifulSoup(raw_headline["rendered"], "html.parser")

        return headline_soup.text
