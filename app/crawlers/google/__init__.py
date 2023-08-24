from ..NewsCrawler import NewsCrawler
from datetime import datetime, timedelta
import re

class GoogleNewsCrawler(NewsCrawler):
    def __init__(self, keyword):
        super(GoogleNewsCrawler, self).__init__(keyword)
        self.base_url = 'https://news.google.com/search?hl=ko&gl=KR&ceid=KR%3Ako&q='
        self.platform = '구글뉴스'
        self.target_csstag_map = {
            'press': '#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb > div:nth-child(1) > div > div > article:nth-child(1) > div.wsLqz.RD0gLb > div > a',
            'datetime': '#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb > div:nth-child(1) > div > div > article:nth-child(1) > div.QmrVtf.RD0gLb.kybdz > div > time',
            'title': '#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb > div:nth-child(1) > div > div > article:nth-child(1) > h3 > a',
            'url': '#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb > div > main > c-wiz > div.lBwEZb.BL5WZb.GndZbb > div:nth-child(1) > div > div > article:nth-child(1) > h3 > a',
        }
        self.target_content_map['platform'] = '구글뉴스'

    def unwrap_htmltag(self, target, htmltag):
        unwrapped = ''
        if target == 'url':
            unwrapped = htmltag['href']
            unwrapped = 'https://news.google.com/'+unwrapped[1:]
        elif target == 'press':
            unwrapped = htmltag.text
            unwrapped = unwrapped[:-6] if '언론사 선정' in unwrapped else unwrapped       
        elif target == 'datetime':
            unwrapped = htmltag.text
            number_pattern = "\d+"
            number = int(re.findall(number_pattern, unwrapped)[0])
            d = None
            try:
                if unwrapped[-3] == '간':
                    d = datetime.today() - timedelta(hours=number)
                elif unwrapped[-3] == '분':
                    d = datetime.today() - timedelta(minutes=number)
                else: 
                    d = datetime.today() - timedelta(days=number)
            except:
                d = datetime.today() - timedelta(days=1)
        
            unwrapped = str(d)
        else:
            unwrapped = htmltag.text
        return unwrapped
    
