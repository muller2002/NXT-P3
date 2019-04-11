import pygame
import time
import socket
import json
import argparse

class PadController(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self, UDP_IP, UDP_PORT):
        self.UDP_IP=UDP_IP
        self.UDP_PORT=UDP_PORT
        
        self.initialize_pad()

        self.sock = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM   # UDP
        )

    def initialize_pad(self):
        '''
        find gamepad using pygame and initialize the first one found
        '''

        # ask pygame for joystick-stuff
        pygame.init()
        pygame.joystick.init()

        # find pads / joysticks
        pad_count = pygame.joystick.get_count()
        if pad_count != 1:
            raise StandardError('More or less than one pad / joystick found. Dying...')
        pad_index = pad_count - 1 # this will be 0...always...

        # initialize pad
        self.pad = pygame.joystick.Joystick(pad_index)
        self.pad.init()
        print('pad initialized')

    def run_gamepad(self):
        '''
        run robot in gamepad-mode. controll robot using generic x-box gamepad
        if u wanna use another gamepad, buttons and axes have to be reconfigured
        depending on your device
        '''

        done = False

        calibrated = False

        # main-loop to acquire joystick-events and react to them
        while not done:

            # get pygame-events first, this loop is mandatory for pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print('buttton pressed')
                if event.type == pygame.JOYBUTTONUP:
                    print('buttton released')

            # initialize shoulder axes which may return wrong values at start
            # without this
            if not calibrated:
                print('Please press down both shoulder axes to continue')
                tower_left = self.pad.get_axis(2)
                tower_right = self.pad.get_axis(5)
                print(tower_left, tower_right)
                if round(tower_left) == 1 and round(tower_right) == 1:
                    calibrated = True
                else:
                    continue

            # main buttons
            button_a = self.pad.get_button(0)
            button_b = self.pad.get_button(1)
            button_x = self.pad.get_button(2)
            button_y = self.pad.get_button(3)

            # initialize axes for movement
            # LOGITECH CONTROLLER LB:
            # axis 0 : left stick left/right [-1,1] default 0
            # axis 1 : left stick up/down [-1,1] default 0
            # axis 2 : left shoulder [-1,1] default -1
            # axis 3 : right stick left/right [-1,1] default 0
            # axis 4 : right stick up/down [-1,1] default 0
            # axis 5 : right shoulder [-1,1] default -1
            front = self.pad.get_axis(4)
            turn = self.pad.get_axis(0)  # 1,2,3
            turn = round(turn, 2)  # no need to be exact here...
            front = round(front, 2)

            tower = 0
            tower_left = self.pad.get_axis(2)
            tower_right = self.pad.get_axis(5)

            if tower_left > -1:
                tower = -1
            elif tower_right > -1:
                tower = 1

            message = json.dumps({
                'forward': front,
                'turn': turn,
                'tower': tower,
            })

            # UDP_IP = "127.0.0.1"
            # UDP_PORT = 14242
            # MESSAGE = "Hello, World!"

            self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))

            time.sleep(.5)
            print(turn, front, tower)
