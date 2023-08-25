from ..NewsCrawler import NewsCrawler
from datetime import datetime, timedelta
import re

class NaverNewsCrawler(NewsCrawler):
    def __init__(self, keyword):
        super(NaverNewsCrawler, self).__init__(keyword)
        self.base_url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query='
        self.platform = '네이버'
        self.target_csstag_map = {
            'press': 'a.info:first-child',
            'datetime': 'div.info_group > span.info',
            'title': 'a.news_tit',
            'url': 'a.news_tit',
        }
        self.target_content_map['platform'] = '네이버'

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
    