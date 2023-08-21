from ._news import NewsController, NewsListController

class AiController(NewsController):
    category = 'ai'

class AiListController(NewsListController):
    category = 'ai'