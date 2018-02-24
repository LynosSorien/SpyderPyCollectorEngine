from spyder.core import SearchEngines
from multiprocessing.dummy import Pool as ThreadPool


class SpyderCore:

    def __init__(self, startUrl, n_threads=8, iterations=2, max_deep=5):
        print("SpyderCore.__init__")
        self.startUrl = startUrl
        self.base = "http://www.google.com"
        self.pool = ThreadPool(n_threads)
        self.iterations = iterations
        self.max_deep = max_deep
        self.search_engine = SearchEngines.GoogleSearchEngine()

    def start(self, criteria):
        content = self.search_engine.search(criteria)
        print("Start multithreading")
        for i in range(0, self.iterations, 1):
            self.pool.map(self.startAnalyze, content[0])
            content = self.search_engine.linkSearch(content[1])
        return content

    def startAnalyze(self, link):
        self.analyze(link, 0)

    def analyze(self, link, deep):
        print("analyze", link)



spyderCore = SpyderCore("http://www.google.com/search")
content = spyderCore.start("Dragon Ball Super")
