import json

import websocket
import json
from datetime import datetime
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()


def on_message(ws, message):
    print(message)


_time = 0


def on_ping(ws, data):
    global _time
    _time += 10
    print("Ping: ", data, "Secs: ", _time)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('### opened ###')
    ws.send(json.dumps({"event": "VerifyGateway", "event_data":{ "mac":  "12:93:A5:67:38:91"}}))

def callback(data):
    global ws
    ws.send(data)

if __name__ == "__main__":
    # websocket.enableTrace(True)
    live_url = "ws://172.17.0.4:10001/channel/TestService/"
    ws = websocket.WebSocketApp(live_url, on_open=on_open, on_message=on_message,
                                on_error=on_error, on_close=on_close,
                                on_ping=on_ping)
    # context = zmq.Context()
    # sub_socket = context.socket(zmq.SUB)
    # sub_socket.connect('epgm://239.192.1.1:5555')
    # sub_stream = ZMQStream(sub_socket)
    # sub_stream.on_recv(callback)
    ws.run_forever()