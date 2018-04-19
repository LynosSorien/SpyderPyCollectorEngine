import threading

class EventSourcerHandler:
    def __init__(self):
        self.queue = []
        self.visited_links = []
        self.ended = False
        self.started = False
        self.lock = threading.RLock()
        self.link_lock = threading.RLock()
        self.consumers = []

    def values_in_queue(self):
        return not len(self.queue) == 0

    def restart_queue(self):
        self.queue = []

    def start_ES(self):
        self.started = True

    def end_ES(self):
        self.ended = True

    def pop(self):
        event = self.queue[0]
        self.queue.remove(event)
        return event

    def put(self, event):
        with self.lock:
            self.queue.append(event)
            self.visited_links.append(event["link"])

        for consumer in self.consumers:
            pass

    def link_visited(self, link):
        return link in self.visited_links

    def register_as_consumer(self, consumer):
        self.consumers.append(consumer)
