import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
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
        self.date_format = "%Y-%m-%d %H:%M:%S"

    # override
    def unwrap_htmltag(self, target, htmltag):
        pass
    
    # 뭔가 이상합니다.
    def is_valid_datetime(self, string):
        try:
            datetime.strptime(string, self.date_format)
            return True
        except ValueError:
            return False

    def get_data(self, html): 
        for target, csstag in self.target_csstag_map.items():
            selected = html.select_one(csstag)
            unwrapped = self.unwrap_htmltag(target, selected)
            if type(unwrapped) == 'str':
                unwrapped = unwrapped.strip()
            # if target == 'datetime':
            #     unwrapped = self.to_datetime(unwrapped)
            self.target_content_map[target] = unwrapped

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

    def run(self):
        self.get_html(self.keyword)
        self.get_data(self.html)
        if not self.isLatestTheSame(compared='url'):
            self.insertToDB()