#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import threading
import time


class PadController(object):

    '''
    module to controll nxt-robot using gamepad
    '''

    def __init__(self, robo):

        self.robo = robo
        self.initialize_pad()
        self.curdir = 0

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


    def run_gamepad(self):
        '''
        run robot in gamepad-mode. controll robot using generic x-box gamepad
        if u wanna use another gamepad, buttons and axes have to be reconfigured
        depending on your device
        '''

        done = False

        # main-loop to acquire joystick-events and react to them
        while not done:

            # get pygame-events first
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print('buttton pressed')
                if event.type == pygame.JOYBUTTONUP:
                    print('buttton released')

            if self.robo.calibrating:
                continue

            # self.robo.self_calibrate()

            # main buttons
            button_a = self.pad.get_button(0)
            button_b = self.pad.get_button(1)
            button_x = self.pad.get_button(2)
            button_y = self.pad.get_button(3)

            # check buttons
            if button_a:
                if not self.robo.player.playing_song:
                    thread.start_new_thread(self.robo.player.play_song,())
            if button_b:
                if not self.robo.player.playing_song:
                    thread.start_new_thread(self.robo.player.play_song, ('schland',))
            if button_x:
                self.robo.calibrate()

            # initialize axes for movement
            front = self.pad.get_axis(4)
            turn = self.pad.get_axis(0)  # 1,2,3
            turn = round(turn, 2)  # no need to be exact here...
            front = round(front, 2)

            self.robo.move(forward=front, turn=turn)
