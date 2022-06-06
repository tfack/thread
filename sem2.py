from threading import Semaphore, BoundedSemaphore

# Usually, you create a Semaphore that will allow a certain number of threads
# into a section of code. This one starts at 5.
s1 = Semaphore(5)

# When you want to enter the section of code, you acquire it first.
# That lowers it to 4. (Four more threads could enter this section.)
s1.acquire()

# Then you do whatever sensitive thing needed to be restricted to five threads.

# When you're finished, you release the semaphore, and it goes back to 5.
s1.release()


# That's all fine, but you can also release it without acquiring it first.
s1.release()

# The counter is now 6! That might make sense in some situations, but not in most.
print(s1._value)  # => 6

# If that doesn't make sense in your situation, use a BoundedSemaphore.

s2 = BoundedSemaphore(5)  # Start at 5.

s2.acquire()  # Lower to 4.

s2.release()  # Go back to 5.

try:
    s2.release()  # Try to raise to 6, above starting value.
except ValueError:
    print('As expected, it complained.')    
