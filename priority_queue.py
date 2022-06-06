#!/usr/bin/python

import queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      print(f"I | init: {name} | q: {q}")
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("R | Starting", self.name)
      process_data(self.name, self.q)
      print ("R | Exiting", self.name)

def process_data(threadName, q):
   print(f"P | process data | {threadName} | {q}")
   while not exitFlag:
      print(f"P | {threadName} | call queueLock.acquire")
      queueLock.acquire()
      if not workQueue.empty():
         print(f"P | queue not empty | {threadName}")
         print("P | one thread at a time gets to grab something from front of the queue")
         data = q.get()
         print(f"P | {threadName} | get data {data} from q {q}")
         print(f"P | {threadName} | queueLock.release")
         queueLock.release()
         print ("%s processing %s" % (threadName, data))
      else:
         print(f"P | queue empty, so release queueLock | {threadName}")
         queueLock.release()
      print(f"P | {threadName} | thread goes to sleep for 1 second after deqeuue/release")
      time.sleep(1)

print("----------------------------------------")
threadList = ["Thread-1", "Thread-2", "Thread-3"]
print(f"L | threadlist: {threadList}")
nameList = ["One", "Two", "Three", "Four", "Five"]
print(f"L | namelist: {nameList}")
print("L | initialize threading.Lock() object queueLock")
queueLock = threading.Lock()
print("L | create queue of 10")
workQueue = queue.Queue(10)
threads = []
threadID = 1

# Create new threads
print("T | create new threads")
for tName in threadList:
   print("T | for each thread in threadlist:")
   print(f"T | create new thread w/ queue | ID {threadID} name | {tName}")
   thread = myThread(threadID, tName, workQueue)
   print(f"T | start thread {tName}")
   thread.start()
   print(f"T | threads: {threads}")
   print(f"T | append {thread.name} to threads")
   threads.append(thread)
   threadID += 1
   print(f"T | increment threadID to {threadID}")

# Fill the queue
print("Q | fill the queue (locked so only one thread can execute at a time)")
print("Q | this lock is for the main thread")
print("Q | acquire Lock")
queueLock.acquire()
print("Q | for each item in list:")
for word in nameList:
   workQueue.put(word)
   print(f"Q | put {word} in queue")
print("Q | release Lock")
queueLock.release()

# Wait for queue to empty
print("N | wait for queue to empty (part of main loop, waiting for threads to complete)")
while not workQueue.empty():
   pass
# Notify threads it's time to exit
print("N | notify threads it's time to exit, make sure they're done")
exitFlag = 1
# Wait for all threads to complete
print("N | wait for all threads to complete")
print("N | makes sure main thread doesn't complete before other threads complete")
print("N | JOIN blocks the calling thread until the time the thread whose join method is called terminates")
print("N | for each thread in threads: JOIN")
for t in threads:
   print(f"{t.name}. JOIN")
   t.join()
print ("N | Exiting Main Thread")