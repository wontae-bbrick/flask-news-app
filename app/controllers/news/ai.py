from ._news import NewsController, NewsListController

# 얘들이 자체적으로 되어야하는거 아냐?
class AiController(NewsController):
    keyword = 'ai'

class AiListController(NewsListController):
    keyword = 'ai'