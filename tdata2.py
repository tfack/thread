# Next, add protection to the data (a lock or something to synchronize) so that a thread that 
# wants to read the data cannot access that data while a thread that is modifying the data is active. 
# A possible task you might try and perform is to read from a file and write to that same file. 
# You could do the same thing with a data structure of some form.

import threading
import random

data = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]

class myThread (threading.Thread):
   def __init__(self, threadID, name, target):
      super(myThread, self).__init__(target=target)
      self.threadID = threadID
      self.name = name
      self.job = target
   def run(self):
       lock.acquire()
       self.job()
       lock.release()

def read():
    for i in data:
        print(i)

def write():
    for j in range(0, len(data)):
        data[j] = data[j].upper()
    random.shuffle(data)
    read()
        
lock = threading.Lock()
threads = []

# Create new threads
print("----------------------------------")
thread1 = myThread(1, "Thread-1", read)
threads.append(thread1)
thread2 = myThread(2, "Thread-2", write)
threads.append(thread2)

# Start new Threads
thread1.start()
thread2.start()

for t in threads:
   t.join()
