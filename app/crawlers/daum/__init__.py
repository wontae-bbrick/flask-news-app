from ..NewsCrawler import NewsCrawler
from datetime import datetime, timedelta
import re
#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > a
class DaumNewsCrawler(NewsCrawler):
    def __init__(self, category):
        super(DaumNewsCrawler, self).__init__(category)
        self.base_url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q='
        self.platform = '다음뉴스'
        self.target_csstag_map = {
            'press': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > span > a:nth-child(1)',
            'datetime': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > span > span',
            'title': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > a',
            'url': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > a',
        }
        self.target_content_map['platform'] = '다음뉴스'

    def unwrap_htmltag(self, target, htmltag):
        unwrapped = ''
        if target == 'url':
            # 이게 이상한건아
            unwrapped = htmltag['href']
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


# 마지막인가.... 
daumNewsAi = DaumNewsCrawler('ai')
daumNewsSto = DaumNewsCrawler('sto')