import csv
import os
import time
from datetime import datetime
import threading
import pandas as pd

os.system('cls||clear')
lock = threading.Lock()
instock = []
output = []
templist = []
threadnm = {}

class myThread (threading.Thread):
    def __init__(self, threadID, name, target, args):
        super(myThread, self).__init__(target=target)
        self.threadID = threadID
        self.name = name
        self.job = target
        self.nm = args
        # print(f"{name} INIT")
    def run(self):
        # print(f"{self.name} RUN")
        crosscheck(self, self.name)

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
    
def crosscheck(self, name):
    # print(f"{name} | compare in-stock pantry item list with recipe ingredient list")
    # print(f"{name} | add to new list of recipe name + missing items + missing items count")
    # print(f"{name} | then delete recipe row from temp list")
    for r in templist:
        lock.acquire()        
        # print(f"{name} | templist item: {r[0]}")
        rname = r[0]
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
        line.append(rname)
        line.append(count)
        line.append(missing)
        line.append({name})
        output.append(line)
        # print(f" | append : {line}")
        # print(f" | remove: {r}") 
        templist.remove(r)
        lock.release()

def threadtest(num_threads):
    threads = []

    # Create new threads
    # print("----------------------------------")
    # print("WhatCanIMake object initialized with csv file locations")
    wc = WhatCanIMake('smoothie.csv', 'smoothierecipes.csv', 'smoothieonly.csv')
    # res = pd.read_csv(wc.pantrylist)
    # numitems = len(res)

    numthreads = num_threads
            
    print(f"number of threads: {numthreads}")
    
    # print("call instock() to get list of pantry items in stock")
    instock = wc.instock_y()
    # print("call getfile() to convert recipe csv into temporary list")
    templist = wc.getfile()
    
    start_time = datetime.now()
    # print(f"file overhead complete: threading timer starts NOW [{start_time}]")
            
    for i in range(1, numthreads+1):
        # print("...for each thread....")
        threadname = "Thread-" + str(i)
        thread = myThread(i, threadname, target=crosscheck, args=(threadname,))
        thread.start()
        threads.append(thread)

    wc.finalsort(output)
    wc.save_file(output)

    for t in threads:
        t.join()
       
    end_time = datetime.now()
    time_diff = (end_time - start_time)
    print(f"elapsed time: {time_diff}")

if __name__ == "__main__":
    threadtest(1)
    # threadtest(2)
    # threadtest(10)
    




