#!/usr/bin/python


import threading
import time

exitFlag = 1

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      print("Starting " + self.name)
      print_time(self.name, 5, self.counter)
      print("Exiting " + self.name)

def print_time(threadName, counter, delay):
    global exitFlag
    while counter >= 0:
        if exitFlag == 0:
            print("Exiting", threadName, "..")
            return "k"
        print(threadName)
        counter -= 1
    exitFlag -= 1
    return "s"

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")