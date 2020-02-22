from anki.cards import Card
from anki.consts import *

from .reprocess import reprocess

oldFlush = Card.flush
oldFlushSched = Card.flushSched


def flush(self):
    print("our flush")
    if self.queue in {QUEUE_TYPE_LRN, QUEUE_TYPE_DAY_LEARN_RELEARN, QUEUE_TYPE_REV}:
        # Only consider review and learning
        reprocess(self)
    oldFlush(self)


Card.flush = flush


def flushSched(self):
    print("our flush")
    if self.queue in {QUEUE_TYPE_LRN, QUEUE_TYPE_DAY_LEARN_RELEARN, QUEUE_TYPE_REV}:
        # Only consider review and learning
        reprocess(self)
    oldFlushSched(self)


Card.flushSched = flushSched
