import greenlet
from scheduler import scheduler

WAIT_FOREVER = 0xFFFFFFFF

def tick(ticks):
    parent = scheduler.parent
    
    if ticks != WAIT_FOREVER:
        for i in range(ticks):
            parent.switch()
    else:
        while True:
            parent.switch()                


