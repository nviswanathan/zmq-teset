import zmq
import time
import sys
import random
import json

from  multiprocessing import Process

from zmq.eventloop import ioloop, zmqstream
ioloop.install()

def getcommand(msg):
    print("Received control command: %s" % msg.decode('utf-8'))
    #if msg[0] == "Exit":
    #    print "Received exit command, client will stop receiving messages"
    #    should_continue = False
    #    ioloop.IOLoop.instance().stop()


def process_message(msg):
    print("Processing ... %s" % msg[0].decode('utf-8'))
    str_data = str(msg[0].decode('utf-8')).lstrip('TestService')
    print(json.loads(str_data))

def client(port_push, port_sub):    
    context = zmq.Context()
    # socket_pull = context.socket(zmq.PULL)
    # socket_pull.connect ("tcp://localhost:%s" % port_push)
    # stream_pull = zmqstream.ZMQStream(socket_pull)
    # stream_pull.on_recv(getcommand)
    # print ("Connected to server with port %s" % port_push)

    # context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect ("ws://localhost:%s" % port_sub)
    socket_sub.setsockopt(zmq.SUBSCRIBE, "TestService".encode('utf-8'))
    stream_sub = zmqstream.ZMQStream(socket_sub)
    stream_sub.on_recv(process_message)
    print("Connected to publisher with port %s" % port_sub)
    ioloop.IOLoop.instance().start()
    print("Worker has stopped processing messages.")


if __name__ == "__main__":
    server_push_port = "5556"
    server_pub_port = "5558"
    Process(target=client, args=(server_push_port,server_pub_port,)).start()