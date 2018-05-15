
from consumers.Consumer import Consumer
import time

class MySqlAgent(Consumer):
    def __init__(self, sleep_time=0.2):
        self.db = None
        self.cur = None
        self.sleep_time = sleep_time

    def startDB(self, database_name="ub_example"):
        print("Starting db mysql")
        self.db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                  user="root",  # your username
                                  passwd="root",  # your password
                                  db=database_name)  # name of the data base
        self.cur = self.db.cursor()
        print("Mysql started")

    def connect_to_eventsourcing(self, eventsourcing):
        print("Start connection to eventsourcing from MySQL")
        while not eventsourcing.started:
            time.sleep(self.sleep_time)
        print("Start mysql parser!")
        while not eventsourcing.ended or eventsourcing.values_in_queue():
            if eventsourcing.values_in_queue():
                event = eventsourcing.pop()
                query ="INSERT INTO links(link, parent, criteria, deep_found, extracted_time) VALUES ('"+event["link"]+"', '"+event["parent"]+"', '"+event["criteria"]+"', "+str(event["deep_found"])+", '"+str(event["extracted_time"])+"')"
                self.cur.execute(query)
            else:
                time.sleep(self.sleep_time)
        self.cur.execute("COMMIT")
        self.db.close()
        print("End mysql parser!")

        return True

    def notify_event(self):
        return
