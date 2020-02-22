from anki.consts import *
from aqt import mw
from aqt.qt import *


def reschedule_all():
    for cid in mw.col.db.list(f"SELECT id FROM cards where queue in ({QUEUE_TYPE_LRN}, {QUEUE_TYPE_DAY_LEARN_RELEARN}, {QUEUE_TYPE_REV})"):
        card = mw.col.getCard(cid)
        card.flush()


action = QAction(mw)

action.setText("Reschedule")
mw.form.menuTools.addAction(action)
action.triggered.connect(reschedule_all)
