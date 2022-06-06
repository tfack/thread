# importing the modules
from threading import *         
import time        
  
# creating thread instance where count = 3
# print("creating semaphore instance where count = 3")
obj = Semaphore(3)        
  
# creating instance
def display(name):    
    
    # calling acquire method
    # print("obj.acquire(): like Lock but only allows entry if thread threshold of 3 hasn't been reached")
    # print(f"display called for thread {name}")
    # a semaphor manages an internal counter which is decremented by each acquire() call and incremented
    # by each release() call. The counter can never go below zero; when acquire() finds that it is zero,
    # it blocks, waiting until some other thread calls release()
    obj.acquire()                
    for i in range(5):
        print('Hello, ', end = '')
        time.sleep(1)
        print(name)
          
        # calling release method
        obj.release()    
          
# creating multiple thread 
t1 = Thread(target = display , args = ('Thread-1',))
t2 = Thread(target = display , args = ('Thread-2',))
t3 = Thread(target = display , args = ('Thread-3',))
t4 = Thread(target = display , args = ('Thread-4',))
t5 = Thread(target = display , args = ('Thread-5',))
  
# calling the threads 
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
