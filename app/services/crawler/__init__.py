import requests
from app.crawlers import crawlerTypes
import time
# 여기에 crawler랑 라우터랑 연결을 하자는 것이에요
class CrawlerService:
    crawlers = []
    keywords = []

    def getConfigs(self):
        # platform model에 요청 보내서 가져오기
        # 각각 보내주는 것
        pass

    def getKeywords(self):
        res = requests.get(f'http://127.0.0.1:5000/keyword')
        data = res.json()
        self.keywords = [ each['keyword'] for each in data ]
        
    # def addKeywords(self, keyword):
        # self.keywords.append(keyword)

    def initCrawlerWKeyword(self):
        self.crawlers = []
        for crawlerType in crawlerTypes:
            for keyword in self.keywords:
                newsCrawler = type(crawlerType.__class__.__name__, (crawlerType,), {
                    "__init__": crawlerType.__init__,
                })
                instance = newsCrawler(keyword)
                self.crawlers.append(instance)

    def readyAllCrawlers(self):
        self.getKeywords()
        self.initCrawlerWKeyword()

    def runAllCrawlers(self):
        for crawler in self.crawlers:
            crawler.run()
            time.sleep(1)

    # 이 서비스는 받은다음에 하는게 아니겠어요? 
    def registCrawler(self):
        requests.post(f'http://127.0.0.1:5000/news/{self.keyword}', json=self.target_content_map)
        pass

    def deleteCrawler(self):
        # 이것도 delete로 하는거야
        requests.delete(f'http://127.0.0.1:5000/news/{self.keyword}')
        pass
