from ._news import NewsController, NewsListController

class StoController(NewsController):
    category = 'sto'

class StoListController(NewsListController):
    category = 'sto'