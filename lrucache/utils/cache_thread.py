"Stoppable thread defined to prune lru cache."

import threading

def RLock():
    '''
    make the container threadsafe if running in a threaded context
    '''
    import threading
    return threading.RLock()


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. 
    
    The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, lrucache):
        super(StoppableThread, self).__init__()

        self.lrucache = lrucache
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            self.lrucache.prune()
