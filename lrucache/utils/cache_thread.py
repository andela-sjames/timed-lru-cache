"Thread safe RLock defined for lru cache."


# https://stackoverflow.com/questions/16567958/when-and-how-to-use-pythons-rlock
def RLock():
    """
    Make the container thread safe if running in a threaded context.
    """
    import threading
    return threading.RLock()
