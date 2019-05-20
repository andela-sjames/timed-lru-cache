"Thread safe RLock defined for lru cache."

import threading

def RLock():
    """
    Make the container thread safe if running in a threaded context.
    """
    import threading
    return threading.RLock()
