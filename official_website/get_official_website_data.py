import json
import os

from scrapegraphai.graphs import *
import pymongo

graph_config = {
    "llm": {
        "api_key": "sk-8TVNENpSop8RDTKC8cEfBc77A7Ab4c6388F53a802a364753",
        "model": "gpt-4",
    }
}

def get_official_website_data():
    proxy = 'http://127.0.0.1:10810'
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['OPENAI_API_KEY'] = 'sk-8TVNENpSop8RDTKC8cEfBc77A7Ab4c6388F53a802a364753'
    os.environ["OPENAI_API_BASE"] = 'https://api.xty.app/v1'

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["auto_submarine_cable"]
    my_col = my_db["2024-03-02_cable"]

    urls = set()
    for col in my_col.find():
        if col['url'] is not None:
            urls.add(col['url'])

    existed_urls = set();
    for root, dirs, files in os.walk('./data'):
        for f in files:
            fp = open('./data/' + f, 'r')
            dic = json.load(fp)
            existed_urls.add(dic['url'])

    cnt = len(existed_urls) + 1
    for url in urls:
        if url in existed_urls:
            continue

        try:
            scrape_graph = SmartScraperGraph(
                prompt="Please extract the submarine cable information from the website, and put them in a json. If there are no information about submarine cable, return error.",
                source=url,
                config=graph_config,
            )

            result = scrape_graph.run()
            print(url)
            print(result)
            result['url'] = url
            with open('./data/{}.json'.format(cnt), 'w') as f:
                f.write(json.dumps(result))
                cnt += 1
        except Exception as e:
            print(url + ' ', e)
            continue


if __name__=='__main__':
    get_official_website_data()
