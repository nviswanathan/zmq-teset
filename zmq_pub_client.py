import zmq
import random
import sys
import time

def publish(port="5559"):
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.connect("tcp://localhost:%s" % port)
	return socket