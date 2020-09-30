import time

class ThreadWatchdog(object):
    """watchdog of all program threads"""
    class wd:
        def __init__(self, name, intervalSec):
            self.interval = intervalSec
            self.name = name
            self.alive = True
            
    
    def __init__(self, logging):
        self.threads = list()
        self.logging = logging

    def subscribe (self,  name, intervalSec):
        self.threads.append(ThreadWatchdog.wd( name, intervalSec))
        return len(self.threads)-1

    def trigger (self, index):
        self.threads[index].avive = True

    def watchThreads(self):
        timestamp = 0
        while True:
            timestamp += 1
            for thread in self.threads:
                if 0 == (timestamp / thread.interval):
                    if thread.alive:
                        thread.alive = False
                    else:
                        logging.Error("Thread " + thread.name + " does not respond")
            if (100 == timestamp):
                timestamp = 0

            time.sleep(1)
                        


