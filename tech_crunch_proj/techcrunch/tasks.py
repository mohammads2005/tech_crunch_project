from django.conf import settings
from celery import shared_task

from .techcrunch_scraper import ScraperHandler
from .models import KeyWord, UserKeywordSearch, ArticleSearchByKeyword, DailySearch


@shared_task
def by_keyword_scraper(keyword, page_count):
    user_keyword, _ = KeyWord.objects.get_or_create(word=keyword)

    user_keyword_search = UserKeywordSearch.objects.create(
        keyword=user_keyword,
        page_count=page_count,
    )

    scraper_handler = ScraperHandler(
        base_url=settings.TECH_CRUNCH_BASE_URL,
        search_url=settings.TECH_CRUNCH_SEARCH_URL,
        json_url=settings.TECH_CRUNCH_JSON_URL,
    )

    scraped_items_count = scraper_handler.search_by_keyword(usersearch_instance=user_keyword_search)
    
    return {
        "keyword": keyword,
        "page_count": page_count,
        "scraped_items_count": scraped_items_count,
    }


@shared_task
def daily_scraper():
    scraper_handler = ScraperHandler(
        base_url=settings.TECH_CRUNCH_BASE_URL,
        search_url=settings.TECH_CRUNCH_SEARCH_URL,
        json_url=settings.TECH_CRUNCH_JSON_URL,
    )
    
    scraped_items_count = scraper_handler.daily_search()
    
    return {"scraped_items_count": scraped_items_count}


@shared_task
def scrape_daily_remaining_items():
    new_scraped_items = list()

    remaining_articles = DailySearch.objects.filter(is_scraped=False).all()

    scraper_handler = ScraperHandler(
        base_url=settings.TECH_CRUNCH_BASE_URL,
        search_url=settings.TECH_CRUNCH_SEARCH_URL,
        json_url=settings.TECH_CRUNCH_JSON_URL,
    )

    for remaining_article in remaining_articles:
        slug = remaining_article.url.split("/")[-2]
        new_article = scraper_handler.article_parser(slug=slug)

        remaining_article.articles = new_article
        remaining_article.is_scraped = True
        remaining_article.save()

        new_scraped_items.append(remaining_article)

    return {
        "search_type": "Daily",
        "new_scraped_items_count": len(new_scraped_items),
    }


@shared_task
def scrape_search_ramining_items():
    new_scraped_items = list()

    remaining_articles = ArticleSearchByKeyword.objects.filter(is_scraped=False).all()

    scraper_handler = ScraperHandler(
        base_url=settings.TECH_CRUNCH_BASE_URL,
        search_url=settings.TECH_CRUNCH_SEARCH_URL,
        json_url=settings.TECH_CRUNCH_JSON_URL,
    )

    for remaining_article in remaining_articles:
        slug = remaining_article.url.split("/")[-2]
        new_article = scraper_handler.article_parser(slug=slug)

        remaining_article.article = new_article
        remaining_article.is_scraped = True
        remaining_article.save()

        new_scraped_items.append(remaining_article)

    return {
        "search_type": "By Keyword",
        "new_scraped_items_count": len(new_scraped_items),
    }
