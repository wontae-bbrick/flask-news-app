import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime, timedelta
import re
class NewsCrawler:
    def __init__(self, keyword):
        self.base_url = ''
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
        self.keyword = keyword
        self.html = ''
        self.platform = ''
        self.target_csstag_map = {}
        self.target_content_map = defaultdict(str)
        self.target_content_map['keyword'] = keyword

    # override
    def unwrap_htmltag(self, target, htmltag):
        unwrapped = ''
        if target == 'url':
            unwrapped = htmltag['href']
        elif target == 'press':
            unwrapped = htmltag.text
            unwrapped = unwrapped[:-6] if '언론사 선정' in unwrapped else unwrapped       
        elif target == 'datetime':
            unwrapped = htmltag.text
            number_pattern = "\d+"
            number = int(re.findall(number_pattern, unwrapped)[0])
            d = None
            if unwrapped[-3] == '간':
                d = datetime.today() - timedelta(hours=number)
            elif unwrapped[-3] == '분':
                d = datetime.today() - timedelta(minutes=number)
            else: 
                d = datetime.today() - timedelta(days=number)

            unwrapped = str(d)
        else:
            unwrapped = htmltag.text
        return unwrapped

    def get_data(self, html): 
        for target, csstag in self.target_csstag_map.items():
            selected = html.select_one(csstag)
            unwrapped = self.unwrap_htmltag(target, selected)
            self.target_content_map[target] = unwrapped.strip()


    def get_html(self, keyword):
        url = self.base_url + keyword
        res = requests.get(url, headers=self.headers)
        raw = res.text
        self.html = BeautifulSoup(raw,'html.parser')

    def isLatestTheSame(self, compared):
        res = requests.get(f'http://127.0.0.1:5000/news/{self.keyword}', params={'latest': True, 'platform': self.platform})
        data = res.json()
        return data[compared] == self.target_content_map[compared]

    def insertToDB(self):
        requests.post(f'http://127.0.0.1:5000/news/{self.keyword}', json=self.target_content_map)

    # def get_keywords(self):
    #     res = requests.get(f'http://127.0.0.1:5000/keyword')
    #     data = res.json()
    #     return data

    def run(self):
        self.get_html(self.keyword)
        self.get_data(self.html)
        if not self.isLatestTheSame(compared='url'):
            self.insertToDB()