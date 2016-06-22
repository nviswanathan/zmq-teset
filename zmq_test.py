import zmq
import time
import sys

from zmq.eventloop import ioloop, zmqstream
ioloop.install()


def subscribe(backend, port="5559"):  
    context = zmq.Context()  
    frontend = context.socket(zmq.SUB)
    frontend.bind("tcp://*:5559")
    frontend.setsockopt(zmq.SUBSCRIBE, "".encode('utf-8'))
    zmq.device(zmq.FORWARDER, frontend, backend)


def server_pub(port="5558"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    print("Running server on port: ", port)
    subscribe(socket)
    return socket


if __name__ == "__main__":
    server_pub()