#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class AutoPilot(object):
    '''
    simple autopilot module for scoutrobo to drive arround autonomously
    '''

    def __init__(self, robo):
        self.robo = robo
        self.transitions = []
        self.curr_time = time.time()
        self.running = False

        # limits used by check_transitions
        self.transition_count = 3
        self.transition_time = 10

    def run(self, init_state='normal'):
        '''
        auto-pilot mode, driving arround, scouting area
        TODO: implement navigation-voodoo
        '''
        self.state = init_state

        # main loop
        while self.running:

            # get sensor data
            telemetry = self.robo.get_telemetry()
            self.touch_left = telemetry['touch_left']
            self.touch_right = telemetry['touch_right']
            self.distance = telemetry['distance']

            self.curr_time = time.time()
            self.check_transitions()

            # TODO: reimplement random-playing of imperial march...

            # basic FSM from here...
            if self.state == 'normal':

                self.robo.go_forward_forever()

                if self.distance < 8:
                    self.state = 'front'
                if self.touch_left:
                    self.state = 'touch_left'
                if self.touch_right:
                    self.state = 'touch_right'

            elif self.state == 'front':
                self.robo.stop()
                self.transitions.append(('front', time.time()))
                self.robo.go_backward(ftime=1.5)
                # turn randomly if front sensor was triggered
                if random.randint(0, 1):
                    self.turn_right(ftime=0.4)
                else:
                    self.turn_left(ftime=0.4)
                self.state = 'normal'

            elif self.state == 'touch_left':
                self.stop()
                self.transitions.append(('touch_left', time.time()))
                self.go_backward(ftime=1)
                self.turn_right(ftime=0.4)
                self.state = 'normal'

            elif self.state == 'touch_right':
                self.stop()
                self.transitions.append(('touch_right', time.time()))
                self.go_backward(ftime=1)
                self.turn_left(ftime=0.4)
                self.state = 'normal'

        self.stop()

    def check_transitions(self):
        '''
        transition = change of state in run-mode
        lots of transitions in a short time indicate the robo is stuck
        '''
        counter = 0

        # count transitions in last 10 seconds
        for trans in self.transitions:
            trans_time = trans[1]
            diff = self.curr_time - trans_time
            if diff < self.transition_time:
                counter += 1

        # lots of transitions found, cry for help...
        if counter > self.transition_count:
            print('CRYING FOR HELP NOW!!!')
            self.transitions = []
            self.running = False
