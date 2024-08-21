from download_pbf import *
from crawl_by_api import *
from insert_mongo import *

if __name__ == '__main__':
    get_all_pbf()
    get_by_api()
    insert_mongo()
