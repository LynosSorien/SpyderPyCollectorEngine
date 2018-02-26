import threading

class EventSourcerHandler:
    def __init__(self):
        self.queue = []
        self.ended = False
        self.started = False
        self.lock = threading.RLock()

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

