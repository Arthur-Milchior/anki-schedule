import time

from anki.consts import *

from .scheduler import scheduler


def reprocess(card):
    currentSecond = time.time()
    lastReviewSecond = card.col.db.scalar(
        "SELECT id FROM revlog WHERE cid = ? ORDER BY id DESC", card.id) // 1000
    ivlInSecond = scheduler(card)
    ivlInHour = round(ivlInHour / 3600)
    ivlInDay = round(ivlInHour/24)
    nextReviewSecond = lastReviewSecond + ivlInSecond
    card.reps = 0
    remainingIntervalInSecond = nextReviewSecond - currentSecond
    remainingIntervalInDay = round(remainingIntervalInSecond / (24 * 60 * 60))

    remainingSecondsBeforeCutoff = card.col.sched.dayCutoff - currentSecond
    secondsSinceLastReview = currentSecond - lastReviewSecond
    print(f"--------------\nCard {card.id} was last reviewed {fmtTimeSpan(secondsSinceLastReview)} ago. Its interval was {card.ivl}. Interval should be {fmtTimeSpan(ivlInSecond)}. I.e. in {fmtTimeSpan(remainingIntervalInSecond)}. ")

    if nextReviewSecond <= currentSecond:
        # card is already due
        card.queue = QUEUE_TYPE_REV
        card.type = CARD_TYPE_REV
        card.ivl = ivlInHour
        card.due = self.today  # TODO: find real day
        return

    if ivlInHour >= 48:
        # more than 2 day. We can average and set to review
        card.queue = QUEUE_TYPE_REV
        card.type = CARD_TYPE_REV
        card.due = card.col.sched.today + remainingIntervalInDay
        card.ivl = ivlInDay
        return

    # at most 2 day. Stay in learning mode.
    card.queue = QUEUE_TYPE_LRN
    card.type = CARD_TYPE_LRN
    card.due = nextReviewSecond
    t = time.localtime(nextReviewSecond)
