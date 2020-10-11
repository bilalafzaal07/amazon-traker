from app import celery
from app import scraper



@celery.task()
def make_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)

@celery.task()
def scrape(keyword, asin):
    data = scraper.track(keyword, asin)
    return data
