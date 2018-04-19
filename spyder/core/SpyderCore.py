from spyder.core import SearchEngines
from multiprocessing.dummy import Pool as ThreadPool
from eventsourcing.EventSourcerHandler import EventSourcerHandler
from consumers.mongodb.MongoAgent import MongoAgent
import datetime
from threading import Thread

class SpyderCore:

    def __init__(self, reactive=False, n_threads=2, iterations=2, max_deep=20):
        print("SpyderCore.__init__")
        print("Maxdeep", max_deep)
        self.pool = ThreadPool(n_threads)
        self.iterations = iterations
        self.max_deep = max_deep
        self.search_engine = SearchEngines.GoogleSearchEngine()
        self.criteria = ""
        self.event_sourcer = EventSourcerHandler()
        self.mongo_agent = MongoAgent()
        self.mongo_agent.startDB()
        self.reactive = reactive
        self.thread = None
        if reactive:
            self.thread = Thread(target=self.mongo_agent.connect_to_eventsourcing, args=(self.event_sourcer, ))
            self.thread.start()

    def start(self, criteria):
        self.criteria = criteria
        content = self.search_engine.search(criteria)
        print("Start event sourcing...")
        start_time = datetime.datetime.utcnow()
        self.event_sourcer.start_ES()
        print("Start multithreading")
        for i in range(0, self.iterations, 1):
            self.pool.map(self.startAnalyze, content[0])
            print("Navigate to", content[1])
            content = self.search_engine.linkSearch(content[1])
        self.event_sourcer.end_ES()
        end_scan_time = datetime.datetime.utcnow()
        print("Scanning ended, take", end_scan_time-start_time)
        if not self.reactive:
            self.mongo_agent.connect_to_eventsourcing(self.event_sourcer)
        elif self.thread is not None:
            self.thread.join()

        if self.event_sourcer.values_in_queue():
            print("Some error has ocurred, remains more elements in queue")
        end_time = datetime.datetime.utcnow()
        print("End parsing, consumer takes ", end_time-end_scan_time, "to process the events, and totally spend",end_time-start_time)
        return True

    def startAnalyze(self, link):
        self.analyze(link)

    def analyze(self, link, deep=0, readedLinks=[]):
        if self.event_sourcer.link_visited(link):
            return link
        if deep > self.max_deep:
            return link
        links = self.search_engine.getUrl(link)
        if links is None or len(links) == 0:
            return link
        print("From link", link, "links returned", len(links))
        process_links = []
        for l in links:
            serialized_item = self.serialize_link(l, link, deep)
            self.event_sourcer.put(serialized_item)
            if l not in readedLinks:
                readedLinks.append(l)
                process_links.append(l)

        for l in process_links:
            self.analyze(l, deep+1, readedLinks)
        return link

    def serialize_link(self, link, parent, deep):
        return {"link": link, "parent": parent,
                "criteria": self.criteria,
                "deep_found": deep,
                "extracted_time": datetime.datetime.utcnow()}


spyderCore = SpyderCore(max_deep=3, reactive=False)
content = spyderCore.start("DragonBall")
