"""Double linked list node class defined."""

from time import time

class DoublylinkedListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        self.time_created = time()

    def remove_bindings(self):
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        self.next = None
        self.prev = None
