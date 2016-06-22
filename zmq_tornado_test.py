import json
from datetime import datetime
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop, PeriodicCallback
ioloop = IOLoop.instance()

class ZMQPubSub(object):

    def __init__(self, callback):
        self.callback = callback

    def connect(self):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect('tcp://54.66.239.36:5558')
        self.sub_stream = ZMQStream(self.sub_socket)
        self.sub_stream.on_recv(self.callback)
        print('subscribe connected:')
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect("tcp://54.66.239.36:5559")
        print('publisher connected')

    def subscribe(self, channel_id):
        print('subscribe channel %s' % channel_id)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, channel_id.encode('utf-8'))

    def send_message(self, channel_id, message):
        print('publish: %s' % datetime.now(), channel_id)
        global message_count
        message_count += 1
        self.pub_socket.send(('%s %s %d' % (channel_id, json.dumps(message), message_count)).encode('utf-8'))

    def close(self):
        self.sub_socket.close()
        self.pub_socket.close()

counter = 0
message_count = 0

class MyWebSocket(WebSocketHandler):

    def open(self, channel_type):
        global counter
        counter += 1
        self.channel_type = channel_type
        self.id = counter
        self.pubsub = ZMQPubSub(self.on_data)
        self.pubsub.connect()
        self.pubsub.subscribe(channel_type)
        self.send_data()
        print('ws opened')

    def on_message(self, message):
        print('Message Resived')
        self.pubsub.send_message(self.channel_type, json.loads(message))
    
    def on_close(self):
        self.periodic.stop()
        self.pubsub.close()
        print('ws closed')

    def on_data(self, data):
        print('socket data: %s' % datetime.now(), data)
        self.write_message(data[0].decode('utf-8'))

    def pub_data(self):
        print('send data:')
        self.pubsub.send_message(self.channel_type, dict(id=self.id, message='Test Client'))

    def send_data(self):
        self.periodic = PeriodicCallback(self.pub_data, 10000)
        self.periodic.start()

def main():
    application = Application([(r'/channel/(?P<channel_type>\w+)/', MyWebSocket)])
    application.listen(10001)
    print('starting ws on port 10001')
    ioloop.start()

if __name__ == '__main__':
    main()