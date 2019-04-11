import socket
import json
import time


class NxtServer(object):
    '''
    Simple server receiving JSON data to control robot via UDP
    '''
    def __init__(self, robo, ip='192.168.43.173', port=14242):
        self.ip = ip
        self.port = int(port)
        self.robo = robo
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM  # UDP
        )
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(.1)

    def run(self):
        print('Starting main loop')
        while True:
            try:
                data = self.sock.recv(128)  # buffer size is 1024 bytes
                print('received')
            except Exception as e:
                print(e)
                data = ''
            try:
                data_json = json.loads(data)
                forward = data_json['forward']
                turn = data_json['turn']
                tower = data_json['tower']
                print('Got valid data, moving...', data_json)
                self.robo.move(forward, turn, tower)
            except Exception as e:
                # print('bad data or something', data)
                print(e)
            time.sleep(.05)
