from django.conf import settings
from celery import shared_task

from .techcrunch_scraper import ScraperHandler
from .models import KeyWord, UserKeywordSearch, ArticleSearchByKeyword, DailySearch, Category

import matplotlib.pyplot as plt
import numpy as np
import requests
import zipfile
import os


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
def category_report():
    category_names = list()
    category_total_articles = list()

    scraped_categories = Category.objects.all()

    for category in scraped_categories:
        category_names.append(category.category_name)
        category_total_articles.append(len(category.article.all()))
    
    axis_x = np.array(category_names)
    axis_y = np.array(category_total_articles)

    plt.figure(figsize=(10, 10))
    plt.subplots_adjust(
        left=0.1, bottom=0.2, right=0.9, top=0.8, wspace=0.8, hspace=0.4
    )
    plt.style.use("_mpl-gallery")

    plt.subplot(1, 1, 1)
    plt.stem(axis_x, axis_y, linefmt="k--")
    plt.ylim(0)
    plt.title("Total Sales per Month")
    plt.xlabel("Months")
    plt.ylabel("Total Sale")
    plt.xticks(rotation=45)

    plt.show()

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


@shared_task
def export_data(image, html_source, id, file_name, slug):
    image_response = requests.get(url=image)
    
    zip_path = os.path.join(settings.BASE_DIR, f"{file_name}.zip")
    
    with zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED) as zip_file:
        if "url.txt" not in zip_file.namelist():
            zip_file.writestr("url.txt", f"exported-zipped-file/{slug}")

        zip_file.writestr(f"{id}.jpg", image_response.content)
        zip_file.writestr(f"{id}.html", html_source)

        zip_file.close()

    return "DONE!"
