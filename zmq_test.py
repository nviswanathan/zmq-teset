import zmq
import time
import sys

from zmq.eventloop import ioloop, zmqstream
ioloop.install()


def subscribe(backend, port="5559"):  
    context = zmq.Context()  
    frontend = context.socket(zmq.SUB)
    frontend.bind("epgm://eth0;239.192.1.1:5555")
    frontend.setsockopt(zmq.SUBSCRIBE, "".encode('utf-8'))
    zmq.device(zmq.FORWARDER, frontend, backend)


def server_pub(port="5558"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("epgm://eth0;239.192.1.1:5555")
    print("Running server on port: ", port)
    subscribe(socket)
    return socket


if __name__ == "__main__":
    server_pub()