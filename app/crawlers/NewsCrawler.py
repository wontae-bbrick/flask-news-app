import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime, timedelta
import re

# 이거 클래스로 만들자... 오버라이딩을 할 수 있잖아
# 현재시간... 날짜

class NewsCrawler:
    base_url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty'
    query = '&query='
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

    # override
    target_csstag_map = {
        'platform': 'a.info:first-child',
        'press': 'a.info:last-child',
        'datetime': 'div.info_group > span.info',
        'title': 'a.news_tit',
        'url': 'a.news_tit',
    }

    # override
    def unwrap_htmltag(target, htmltag):
        unwrapped = ''
        if target == 'url':
            # 이게 이상한건아
            unwrapped = htmltag['href']
        elif target == 'platform':
            unwrapped = htmltag.text
            unwrapped = unwrapped[:-6] if '언론사 선정' in unwrapped else unwrapped       
        elif target == 'datetime':
            unwrapped = htmltag.text
            number_pattern = "\d+"
            number = int(re.findall(number_pattern, unwrapped)[0])
            # 숫자만 가져오는 방법...? 정규표현식
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

    def get_target_content(html): 
        target_content_map = defaultdict(str)
        for target, csstag in target_csstag_map.items():
            selected = html.select_one(csstag)
            unwrapped = unwrap_htmltag(target, selected)
            target_content_map[target] = unwrapped

        return target_content_map    

    def get_html(keyword):
        url = base_url + query + keyword
        res = requests.get(url, headers=headers)
        raw = res.text
        html = BeautifulSoup(raw,'html.parser')
        return html

    # 이걸이제 밖으로 어떻게 빼냐는거야

    def isLatestTheSame(self):
        res = requests.get(f'http://127.0.0.1:5000/{category}', params={'latest': True})
        data = res.json()
        if data['title'] == self.target_content_map['title']:
            return True
        else:
            return False

    def insertToDB(self):
        requests.post(f'http://127.0.0.1:5000/{self.category}', json=self.target_content_map)

    def run(category):
        # 동시에 thread로 어떻게 돌릴래?
        html = get_html(category)
        target_content_map = get_target_content(html)
        target_content_map['category'] = category
        pass
