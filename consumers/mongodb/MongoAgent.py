from pymongo import MongoClient
from consumers.Consumer import Consumer
import time


class MongoAgent(Consumer):
    def __init__(self, sleep_time=0.2):
        self.client = MongoClient("localhost", 27017)
        self.db = None
        self.events = None
        self.sleep_time = sleep_time

    def startDB(self, database_name="spyderpy_ub"):
        self.db = self.client[database_name]
        self.events = self.db['events']

    def connect_to_eventsourcing(self, eventsourcing):
        print("Start connection to eventsourcing from MongoAgent")
        while not eventsourcing.started:
            time.sleep(self.sleep_time)
        print("Start mongo parser!")
        while not eventsourcing.ended or eventsourcing.values_in_queue():
            if eventsourcing.values_in_queue():
                event = eventsourcing.pop()
                self.events.insert_one(event)
            else:
                time.sleep(self.sleep_time)
        print("End mongo parser!")
        return True

    def notify_event(self):
        return
