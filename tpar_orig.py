import csv
import os
import time
from datetime import datetime
from datetime import timedelta
import threading
import pandas as pd

os.system('cls||clear')
instock = []
output = []

class myThread (threading.Thread):
    def __init__(self, threadID, name, target):
      super(myThread, self).__init__(target=target)
      self.threadID = threadID
      self.name = name
      self.job = target
    def run(self):
       rl = self.job
       result = rl.rsort()

class WhatCanIMake():
    def __init__(self, pantrylist, recipelist, resultlist):
        self.pantrylist = pantrylist
        self.recipelist = recipelist
        self.resultlist = resultlist
    def rsort(self):
        with open(self.pantrylist, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[1] == 'y':
                    instock.append(row[0])

        with open(self.recipelist, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            for r in reader:
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
                output.append(line)
            output.sort(key=lambda row: (row[1], row[2]), reverse=False)

        with open(self.resultlist, 'w', newline='') as csvfile:
            write=csv.writer(csvfile)
            write.writerows(output)
        return output
    
lock = threading.Lock()
threads = []

# Create new threads
print("----------------------------------")
rl = WhatCanIMake('smoothie.csv', 'smoothierecipes.csv', 'smoothieonly.csv')
# res = pd.read_csv(rl.pantrylist)
# numitems = len(res)

numthreads = 1

# if numitems % numthreads == 0:
#     items_per_thread = numitems/numthreads
# else:
#     # for now ignore but add remainder later
#     items_per_thread = numitems/numthreads
        
print(f"number of threads: {numthreads}")
start_time = datetime.now()
        
for i in range(1, numthreads+1):
    name = "Thread-" + str(i)
    thread = myThread(i, name, rl)
    thread.start()
    threads.append(thread)

for t in threads:
       t.join()

end_time = datetime.now()
time_diff = (end_time - start_time)
print(f"elapsed time: {time_diff}")

