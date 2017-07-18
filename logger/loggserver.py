#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
import zmq
import random
import time
from helpers.pygtail import Pygtail
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
         
context = zmq.Context()
push_sender = context.socket(zmq.PUSH)
push_sender.connect("tcp://127.0.0.0:0000")

#DIRECTORIES_TO_WATCH = ["/home/caixa/dev/tty1"]
DIRECTORIES_TO_WATCH = ["/usr/local/share/logg"]
class Watcher: 
   #FILE_TO_WATCH = "/home/caixa/dev/tty1/logg.text" 

   def __init__(self): 
       self.observer = Observer() 

   def run(self): 
       event_handler = Handler(self.observer) 
       for _dir in DIRECTORIES_TO_WATCH:
           self.observer.schedule(event_handler, _dir, recursive=True) 
       #self.observer.schedule(event_handler, self.FILE_TO_WATCH, recursive=True) 
       self.observer.start() 
       try: 
           while True: 
               time.sleep(2) 
       except Exception as e: 
           self.observer.stop() 
           print "Error", e

       self.observer.join() 


class Handler(FileSystemEventHandler): 

   def __init__(self, observer):
       super(Handler, self).__init__()
       # This will be used to add more observer at runtime
       self.observer = observer

   #@staticmethod 
   def on_any_event(self, event): 
       if event.is_directory: 
           pass

       elif event.event_type == 'created': 
           # Take any action here when a file is first created. 
           pass

       elif event.event_type == 'modified' and event.src_path == '/usr/local/share/logg/register.logg':
           # Register a new directory for monitoring
           # Todo: Although it's not causing any problems, refactor this logic so as not to registering 
           # the same directory multiple times
           for line in Pygtail(event.src_path):
               self.observer.schedule(self, line.strip(), recursive=True) 

       elif event.event_type == 'modified' and event.src_path.find('.logg') > -1 and  \
            event.src_path.find('.offset') < 0 and event.src_path.find('.logg.') < 0:
           # Loggs are sent to the server when events happens 
           # Todo: Create an option to recover full log if necessary. This will solve the following problem: 
           # Loggs are lost from memory if connection takes too long to restablish.
           for line in Pygtail(event.src_path):

               _pairs = [spl for spl in  line.split('|') if len(spl) > 0]
               payload = {}
               for _pair in _pairs:
                   print _pair
                   key, value = _pair.split(':')
                   payload[key] = value.strip()

               print 'payload'
               push_sender.send_json(payload)


if __name__ == "__main__":

    # This block is called only when testing. In production use the 'loggserver' CLI command
    w = Watcher() 
    w.run()

    # Todo: A file monitored by Pygtail may be restart from scratch again, this will cause pygtail 
    # to lose the current offsett for the file. It's necessary to find a workaround to this problem.
    # Todo: Create another survice to do helper activities... This service could also trigger some
    # events from time to time
    # Todo: Handle log files if they getting too big; You could remove/move them or rename them
    # Todo: When restarting loggserver do a touch to file /usr/local/share/loggs/register.logg

