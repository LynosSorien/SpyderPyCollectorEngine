import abc

class Consumer:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def connect_to_eventsourcing(self, eventsourcing):
        '''
        Vinculates the eventsourcing with the consumer.
        :param eventsourcing:
        :return:
        '''

    @abc.abstractmethod
    def notify_event(self):
        '''
        Notifies new event from event sourcing to consumers
        :return:
        '''
        return


