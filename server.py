#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import BaseHTTPServer
import json
import cgi
import thread
import json
import sys

from robo import ScoutRobo
from lib.nxt_player import Nxt_Player
from nxt.telegram import InvalidOpcodeError

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 14242


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """
        Respond to a GET request.

        Example url: 'http://127.0.0.1:14242/nxt?command=go_forward&ftime=2'
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.args = {}
        idx = self.path.find('?')
        if idx >= 0:
            self.rpath = self.path[:idx]
            self.args = cgi.parse_qs(self.path[idx + 1:])
        else:
            self.rpath = self.path

        try:
            self.execute_command()
        except:  # Doesn't matter what happens, if the server is broke just shut it down
            print("Error while executing command")
            # Shutdowns the server without waiting (without deadlock)
            self.server._BaseServer__shutdown_request = True

    def execute_command(self):
        if 'nxt' in self.rpath:
            if 'command' in self.args.keys():
                command = self.args['command'][0]
                ftime = 1
                if 'ftime' in self.args.keys():
                    ftime = float(self.args['ftime'][0])
                # Use example: command=get_samples:json or command=get_samples:html or just command=get_samples
                if "get_samples" in command:
                    # keep_alive() # Because this if branch is ALWAYS called when we are in the web interface
                    if "json" in command:
                        samples = get_samples(json=True)
                    elif "html" in command:
                        samples = get_samples(html=True)
                    else:
                        samples = get_samples()
                    self.wfile.write(samples)
                elif command == 'go_forward':
                    go_forward(ftime)
                    self.wfile.write("Done")
                    return
                elif command == 'go_backward':
                    go_backward(ftime)
                    self.wfile.write("Done")
                    return
                elif command == 'turn_left':
                    turn_left(ftime)
                    self.wfile.write("Done")
                    return
                elif command == 'turn_right':
                    turn_right(ftime)
                    self.wfile.write("Done")
                    return
                elif command == 'stop':
                    stop()
                    self.wfile.write("Done")
                elif command == 'go_forward_forever':
                    go_forward_forever()
                    self.wfile.write("Done")
                elif command == 'go_backward_forever':
                    go_backward_forever()
                    self.wfile.write("Done")
                elif command == 'turn_left_forever':
                    turn_left_forever()
                    self.wfile.write("Done")
                elif command == 'turn_right_forever':
                    turn_right_forever()
                    self.wfile.write("Done")
                elif command == 'unlock':
                    unlock()
                    self.wfile.write("Done")
                else:
                    self.wfile.write("Command not found.")
                    return


# commands
def get_samples(**kwargs):
    '''
    Returns telemetry as text, json or html - default is text

    :param kwargs: json bool or html bool
    :return: Telemetry from the sensors
    '''
    js = kwargs.get("json", False)
    html = kwargs.get("html", False)

    telemetry = robo.get_telemetry()

    if js:
        return json.dumps(telemetry)
    elif html:
        joiner = "<br>"
    else:
        joiner = "\n"

    return joiner.join(sensor + ": " + str(sample) for sensor, sample in robo.get_telemetry().items())


def keep_alive():
    robo.keep_alive()


def go_forward(ftime):
    print("Go forward..")
    robo.go_forward(ftime=ftime)


def go_backward(ftime):
    print("Go back..")
    robo.go_backward(ftime=ftime)


def turn_left(ftime):
    print("Turn right..")
    robo.turn_left(ftime=ftime)


def turn_right(ftime):
    print("Turn left..")
    robo.turn_right(ftime=ftime)


def stop():
    print("Stopping...")
    robo.stop()


def go_forward_forever():
    print 'Going forward...'
    robo.go_forward_forever()


def go_backward_forever():
    print 'Going forward...'
    robo.go_backward_forever()


def turn_left_forever():
    print 'Turning right'
    robo.turn_left_forever()


def turn_right_forever():
    print 'Turning right'
    robo.turn_right_forever()


def unlock():
    print 'Unlocking...'
    if robo.locked:
        print 'unlocking...'
        robo.unlock()
    else:
        robo.locked = True
        print 'locking...'


def music():
    if not self.player.playing_song:
        number = random.randint(0, 400)
        if number == 88:
            thread.start_new_thread(self.player.play_song, ())


# Startpunkt
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    # Change baddr and pin for your robot
    robo = ScoutRobo(baddr="00:16:53:0D:14:AE", pin="1234")
    try:
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        httpd.serve_forever()
    except:  # Doesn't matter what happens, if the server is broke just shut it down
        print("Some general error in the server")

    print("Server shuts down...")
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
