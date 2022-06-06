import csv
import os
import time
from datetime import datetime
from datetime import timedelta
import threading
import pandas as pd

os.system('cls||clear')
lock = threading.Lock()
instock = []
output = []
templist = []

class myThread (threading.Thread):
    def __init__(self, threadID, name, target):
        super(myThread, self).__init__(target=target)
        self.threadID = threadID
        self.name = name
        self.job = target
    def run(self):
        # instock = wc.instock_y()
        # templist = wc.getfile()
        # lock.acquire()
        crosscheck(self)
        # lock.release()
        # wc.save_file(output)

class WhatCanIMake():
    def __init__(self, pantrylist, recipelist, resultlist):
        self.pantrylist = pantrylist
        self.recipelist = recipelist
        self.resultlist = resultlist
    def instock_y(self):
        with open(self.pantrylist, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[1] == 'y':
                    instock.append(row[0])
        return instock

    def getfile(self):
        with open(self.recipelist, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            for r in reader:
                 templist.append(r)
            return templist

    def finalsort(self, output):
        output.sort(key=lambda row: (row[1], row[2]), reverse=False)
        return output

    def save_file(self, output):     
        with open(self.resultlist, 'w', newline='') as csvfile:
            write=csv.writer(csvfile)
            write.writerows(output)
    
def crosscheck(self):
    # with open(self.recipelist, newline='') as csvfile:
    #     reader = csv.reader(csvfile, quotechar='"')
        # for r in reader:
    for r in templist:
        name = r[0]
        ingred_c = r[1]
        ingred = ingred_c.split(",")     
        missing = []
        line = []
        count = 0
        for ing in ingred:
            ing = ing.strip()
            if ing in instock:
                pass
            else:
                missing.append(ing)
                count = count + 1
        line.append(name)
        line.append(count)
        line.append(missing)
        line.append(threadname)
        output.append(line)
        templist.remove(r)

def threadtest(num_threads):
    threads = []

    # Create new threads
    print("----------------------------------")
    wc = WhatCanIMake('smoothie.csv', 'smoothierecipes.csv', 'smoothieonly.csv')
    res = pd.read_csv(wc.pantrylist)
    numitems = len(res)

    numthreads = num_threads

    # if numitems % numthreads == 0:
    #     items_per_thread = numitems/numthreads
    # else:
    #     # for now ignore but add remainder later
    #     items_per_thread = numitems/numthreads
            
    print(f"number of threads: {numthreads}")
    
    instock = wc.instock_y()
    templist = wc.getfile()
    
    start_time = datetime.now()
            
    for i in range(1, numthreads+1):
        global threadname
        threadname = "Thread-" + str(i)
        thread = myThread(i, threadname, crosscheck)
        thread.start()
        threads.append(thread)

    wc.finalsort(output)
    wc.save_file(output)

    end_time = datetime.now()
    time_diff = (end_time - start_time)
    print(f"elapsed time: {time_diff}")

    for t in threads:
        t.join()
       

if __name__ == "__main__":
    # threadtest(1)
    # threadtest(2)
    threadtest(10)
    







