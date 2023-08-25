from ..NewsCrawler import NewsCrawler
from datetime import datetime, timedelta
import re
class DaumNewsCrawler(NewsCrawler):
    def __init__(self, keyword):
        super(DaumNewsCrawler, self).__init__(keyword)
        self.base_url = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q='
        self.platform = '다음'
        self.target_csstag_map = {
            'press': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > span > a:nth-child(1)',
            'datetime': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > span > span',
            'title': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > a',
            'url': '#newsColl > div:nth-child(1) > div.cont_divider > ul > li:nth-child(1) > div.wrap_cont > a',
        }
        self.target_content_map['platform'] = '다음'
        self.date_format = "%Y.%m.%d"

    def unwrap_htmltag(self, target, htmltag):
        unwrapped = ''
        if target == 'url':
            unwrapped = htmltag['href']
        elif target == 'datetime':
            unwrapped = htmltag.text
            if not self.is_valid_datetime(unwrapped):            
                number_pattern = "\d+"
                number = int(re.findall(number_pattern, unwrapped)[0])
                d = None
                if unwrapped[-2] == '간':
                    d = datetime.today() - timedelta(hours=number)
                elif unwrapped[-2] == '분':
                    d = datetime.today() - timedelta(minutes=number)
                else: 
                    d = datetime.today() - timedelta(days=number)
                unwrapped = str(d)
        else:
            unwrapped = htmltag.text
            # unwrapped = unwrapped.strftime("%Y-%m-%d %H:%M:%S")
            # unwrapped = unwrapped.strptime("%Y-%m-%d %H:%M:%S")
        return unwrapped
