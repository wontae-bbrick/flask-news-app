from ..NewsCrawler import NewsCrawler
from datetime import datetime, timedelta
import re

class GoogleNewsCrawler(NewsCrawler):
    def __init__(self, keyword):
        super(GoogleNewsCrawler, self).__init__(keyword)
        self.base_url = 'https://news.google.com/search?hl=ko&gl=KR&ceid=KR%3Ako&q='
        self.platform = '구글뉴스'
        # 이 매핑이 지금 잘못되었음
        # article.MQsxIb
        self.target_csstag_map = {
            'press': 'article.MQsxIb a.wEwyrc',
            'datetime': 'article.MQsxIb time.WW6dff',
            'title': 'article.MQsxIb h3 a',
            'url': 'article.MQsxIb a.VDXfz',
        }
        self.target_content_map['platform'] = '구글뉴스'
        #yDmH0d > c-wiz:nth-child(30) > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb > div:nth-child(99) > div > article
    def unwrap_htmltag(self, target, htmltag):
        unwrapped = ''
        if target == 'url':
            unwrapped = htmltag['href']
            unwrapped = 'https://news.google.com/'+unwrapped[2:]
        elif target == 'press':
            unwrapped = htmltag.text
        elif target == 'datetime':
            unwrapped = htmltag['datetime']
            unwrapped = " ".join(unwrapped[:-1].split('T'))
        else:
            unwrapped = htmltag.text
        return unwrapped
    

# 구글뉴스가 안 들어가는 것 같음