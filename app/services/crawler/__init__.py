import requests
from app.crawlers import crawlerTypes
# 여기에 crawler랑 라우터랑 연결을 하자는 것이에요
class CrawlerService:
    crawlers = []

    def getConfigs(self):
        pass

    def getSearchs(self):
        res = requests.get(f'http://127.0.0.1:5000/keyword')
        data = res.json()
        searchs = [ each['search'] for each in data ]
        return searchs

    def initCrawler(self):
        for crawlerType in crawlerTypes:
            for each in data:
                keyword = each['keyword']
                newsCrawler = type(crawlerType.__class__.__name__, (crawlerType,), {
                    "__init__": crawlerType.__init__,
                })
                instance = newsCrawler(keyword)
                self.crawlers.append(instance)
        pass

    def registCrawler(self):
        pass

    def deleteCrawler(self):
        pass
