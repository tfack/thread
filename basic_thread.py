#!/usr/bin/python

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      # print("I | myThread inherits from Thread")
      print(f"I | init arguments: threadID={threadID}, name={name}, counter={counter}")
      # print("I | thread init (override of Thread init())")
      # print("I | it's important to call the Thread class from itself so it can do basic initialization")
      threading.Thread.__init__(self)
      # print("I | init calls parent Thread init")
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      # print("R | thread run (override of Thread run())")
      # print("R | can either put code here or a pass function/parameters specified at construction time")
      print(time.ctime(time.time()), self.name)
      print ("R | Starting", self.name)
      print("R | calling time delay of 5", self.name)
      print_time(self.name, 5, self.counter)
      print ("R | Exiting", self.name)
      print(time.ctime(time.time()), self.name)

def print_time(threadName, counter, delay):
   # print("P | print_time (standalone method called from within run(); could have been passed in as init param")
   # print("P | both threads have opportunity to access print_time() at same time but likely won't overlap due to second delays")   
   print("P | print_time")
   while counter:
      print(f"P | while loop | thread={threadName} | counter={counter} | delay={delay}")
      print(f"bd {time.ctime(time.time())} {threadName}")
      if exitFlag:
         threadName.exit()
      print(f"P | delay execution for {delay} seconds | thread: {threadName}")
      time.sleep(delay)
      print(f"ad {time.ctime(time.time())} {threadName}")
      print ("P | %s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1
      print(f"P | new counter value: {counter} | thread: {threadName}")

# Create new threads
print("----------------------------------------------------------------")
print("E | Main Thread")
print("C | create thread1 (counter arg 1 => 1 second delay)")
thread1 = myThread(1, "Thread-1", 1)
print("C | create thread2 (counter arg 2 => 2 second delay)")
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
print("S | start thread1")
print(f"st1 {time.ctime(time.time())}")
thread1.start()
print("S | start() calls run()? [thread1]")
print("S | start thread2")
print(f"st2 {time.ctime(time.time())}")
thread2.start()
print("S | start() calls run()? [thread2]")

print ("E | Exiting Main Thread")