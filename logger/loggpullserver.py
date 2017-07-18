#!/usr/bin/python2.7 
#-*- coding: utf-8 -*- 
import time
import zmq
import random
from twisted.internet import reactor, task
from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
client = MongoClient()
db = client['logs'] # database
collection = db['logg'] # collection

context = zmq.Context()
results_receiver = context.socket(zmq.PULL)

# Todo: Point this address to the real server
#results_receiver.bind("tcp://127.0.0.1:3804")
results_receiver.bind("tcp://172.16.20.97:3804")
collecter_data = {}

def receive_logg():
   result = results_receiver.recv_json()
   if result:
       print ('The server got..:', result)
       response = collection.insert_one(result)


if __name__ == "__main__":

   # This block is called only when testing. In production use the 'loggserver' CLI command 
   loop = task.LoopingCall(receive_logg)
   loop.start(0)

   reactor.run()
