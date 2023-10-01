import greenlet

class scheduler():
    parent = None
    
    def __init__(self):
        scheduler.parent = greenlet.getcurrent()
        self.routines = []
        self.executing = []
        self.tickCount = 0

    def add(self, routine):
        groutine = greenlet.greenlet(routine)
        self.routines.append(groutine);
        self.executing.append(groutine);

    def add_front(self, routine):
        groutine = greenlet.greenlet(routine)
        self.routines.insert(0,groutine);
        self.executing.insert(0,groutine);

    def run(self):
        self.executing = self.routines.copy()
        for glet in self.executing:
            glet.switch()
            if glet.dead == True:
                self.routines.remove(glet)
        self.tickCount += 1


    def getTickCount(self):
        return self.tickCount
        
