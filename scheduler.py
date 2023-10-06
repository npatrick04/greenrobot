import greenlet

class scheduler():
    parent = None
    
    def __init__(self):
        scheduler.parent = greenlet.getcurrent()
        self.index = 0
        self.routines = []
        self.executing = []
        self.tickCount = 0

    def add(self, routine, callvalue=None):
        self.index = self.index + 1
        groutine = {"routine":greenlet.greenlet(routine),
                    "callvalue":callvalue,
                    "callarg": callvalue!=None,
                    "routine_id":self.index}
        self.routines.append(groutine)
        self.executing.append(groutine)
        return self.index

    def add_front(self, routine, callvalue=None):
        self.index = self.index + 1
        groutine = {"routine":greenlet.greenlet(routine),
                    "callvalue":callvalue,
                    "callarg": callvalue!=None,
                    "routine_id":self.index}
        self.routines.insert(0,groutine);
        self.executing.insert(0,groutine);
        return self.index

    def remove(self, routine_index):
        groutine = next((item for item in self.routines if item["routine_id"] == routine_index),None)
        if groutine is not None:
            self.routines.remove(groutine)
            self.executing.remove(groutine)

    def is_alive(self, routine_index):
        groutine = next((item for item in self.routines if item["routine_id"] == routine_index),None)
        if groutine is not None:
            return True
        return False
            

    def run(self):
        self.executing = self.routines.copy()
        for groutine in self.executing:
            glet = groutine["routine"]
            callvalue = groutine["callvalue"]
            if groutine["callarg"]:
                glet.switch(callvalue)
            else:
                glet.switch()
                
            if glet.dead == True:
                self.routines.remove(groutine)
        self.tickCount += 1


    def getTickCount(self):
        return self.tickCount
        
