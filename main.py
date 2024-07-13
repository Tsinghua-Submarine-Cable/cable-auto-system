import telegeography
import infrapedia
import submarinenetworks
import wiki


def telegeography_auto():
    telegeography.get_telegeography_by_api()
    submarinenetworks.insert_mongo()

def infrapedia_auto():
    infrapedia.download_pbf()
    infrapedia.get_eol_from_pbf()
    infrapedia.get_by_api()
    submarinenetworks.insert_mongo()

def submarine_networks_auto():
    submarinenetworks.get_cable_links()
    submarinenetworks.get_cable_introduction()
    submarinenetworks.get_station_links()
    submarinenetworks.get_station_article_links()
    submarinenetworks.get_station_article()
    submarinenetworks.station_ai_extract()
    submarinenetworks.insert_mongo()

def wikipedia_auto():
    wiki.crawl_wikipedia()
    wiki.cable_ai_extract()
    wiki.insert_mongo()



if __name__ == '__main__':
    telegeography_auto()
    infrapedia_auto()
    submarine_networks_auto()
    wikipedia_auto()


