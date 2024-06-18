from submarinenetworks import *

def crawl_all():
    get_cable_links()
    get_cable_introduction()
    get_article_links()
    get_articles()
    get_station_article_links()
    get_station_article()

if __name__ == '__main__':
    crawl_all()
