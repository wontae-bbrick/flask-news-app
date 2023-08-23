from ._news import NewsController, NewsListController

class StoController(NewsController):
    keyword = 'sto'

class StoListController(NewsListController):
    keyword = 'sto'