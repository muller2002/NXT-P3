#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nxt. motor import *
from nxt.sensor import *
from nxt.bluesock import BlueSock
from nxt.locator import Method, find_one_brick

import time

from pf_nxt.nxt_player import Nxt_Player
from pf_nxt.nxt_pad import PadController
from pf_nxt.nxt_autopilot import AutoPilot
from pf_nxt.nxt_pair import Pair


# TODO: make base class from this to implement mechanical specifics in subclasses
# OR by composition (Motor Behaviours)
# favor composition ;-)
class ScoutRobo(object):
    '''
    ScoutRobo is a python class to control a lego-nxt robot by using bluetooth
    or usb connection.
    '''

    def __init__(self, baddr, pin, direct=False, method='bluetooth'):
        '''
        initialize robot. by default robot is found using bluetooth,
        remember to install bluetooth lib before usage!
        :param baddr: The bluetooth mac address
        :param pin: The pin to ensure the connection
        '''

        if method == 'bluetooth':
            # Pair with nxt via bluetooth before connecting
            self.stable_connection = Pair(baddr, pin)
            self.brick = BlueSock(baddr).connect()
        elif method == 'usb':
            # explicitly deactivate bluetooth
            usb_only = Method(usb=True, bluetooth=False, fantomusb=True)
            self.brick = find_one_brick(method=usb_only, debug=True)

        # initialize basic functions
        self.init_motors()
        self.init_sensors()

        # initialize some useful vars
        self.touch_right = False
        self.touch_left = False

        # locked is used to stop robo from moving when it has collided
        # getting orders from http-server
        self.locked = False

        self.calibrating = False

        # player for beeps and stuff
        self.player = Nxt_Player(self.brick)

        # Initialize pad and autopilot modules
        # TODO: do not start padmode if server
        if direct:
            self.pad_controller = PadController(self)
        self.autopilot = AutoPilot(self)

        self.calibrate()

    def init_motors(self):
        '''
        find and initialize motors from ports of brick
        '''

        self.motors = [
            Motor(self.brick, PORT_A),
            # Motor(self.brick, PORT_B)
        ]

        self.steering_motor = Motor(self.brick, PORT_C)
        self.steering_motor.brake()

        self.tower_motor = Motor(self.brick, PORT_B)
        self.tower_motor.brake()

    def calibrate(self):
        '''
        turn steering motor to extreme positions and calculate middle position
        from both end positions
        '''

        self.calibrating = True
        print('calibrating...')
        direction = 1
        self.steering_motor.run(power=direction * 60)

        # time.sleep(5)
        self.touch_right = self.sensors["touch_right"].get_sample()
        while not self.touch_right:
            time.sleep(.01)
            self.touch_right = self.sensors["touch_right"].get_sample()
            print(self.touch_right)

        self.steering_motor.brake()
        self.max_right = self.steering_motor.get_tacho().tacho_count
        print('max right', self.max_right)
        direction = -1
        self.steering_motor.run(power=direction * 60)
        time.sleep(1)
        # time.sleep(10)

        self.touch_left = self.sensors["touch_left"].get_sample()
        while not self.touch_left:
            time.sleep(.01)
            self.touch_left = self.sensors["touch_left"].get_sample()
            print(self.touch_left)

        self.steering_motor.brake()
        self.max_left = self.steering_motor.get_tacho().tacho_count
        print('max left', self.max_left)
        self.steering_interval = (self.max_right - self.max_left) / 2
        self.tacho_middle = self.max_left + self.steering_interval

        for i in range(5):
            tacho = self.steering_motor.get_tacho()
            tacho_cur = tacho.tacho_count
            tacho_diff = self.tacho_middle - tacho_cur
            if tacho_diff > 0:
                self.steering_motor.turn(power=120, tacho_units=tacho_diff)
                time.sleep(1)
            elif tacho_diff < 0:
                self.steering_motor.turn(power=-120, tacho_units=-tacho_diff)
                time.sleep(1)

        tacho = self.steering_motor.get_tacho()
        tacho_middle_now = tacho.tacho_count
        self.steering_motor.idle()
        self.calibrating = False
        print('calibration done', self.max_left, self.max_right, self.tacho_middle, tacho_middle_now)
        '''
        tacho = self.steering_motor.get_tacho()
        self.tacho_middle = tacho.tacho_count
        self.steering_interval = 7200
        '''


    def init_sensors(self):
        '''
        find and initialize sensors from ports of brick
        useful sensors: 'touch_left', 'touch_right', 'light_color', 'ultrasonic'
        '''

        # map sensor names against driver class and port plugged in robot for
        # safe initialization
        SENSOR_MAP = {
            "touch_left": (Touch, PORT_4),
            "touch_right": (Touch, PORT_3),
            #"light_color": (Color20, PORT_3),  # unable to false-detect this one
            #"ultrasonic": (Ultrasonic, PORT_4),
        }

        self.sensors = {}
        print('Initializing sensors')
        for sensor_name, sensor in SENSOR_MAP.items():
            sensor_class, port = sensor
            try:
                sensor_instance = sensor_class(self.brick, port)
                sensor_instance.get_sample()
            except Exception:
                print('Init sensor %s on port %s failed.' % (sensor_name, port))
                print('Are you sure its plugged in?')  # Have u tried turning it off and on again?
                continue
            self.sensors[sensor_name] = sensor_instance
        print('Sensors: %s' % self.sensors)


    def move(self, forward, turn, tower=0):
        print(forward, turn)
        '''
        move robot based on forward and turn values which should be between -1
        and 1
        '''

        # abort if values out of range
        if abs(forward) > 1 or abs(turn) > 1:
            return

        # do not react to forward/turn values smaller than...
        STEERING_MARGIN = 0.1
        # fraction of steering interval used, 1 means full (not recommended!)
        STEERING_DAMPENING = 0.9
        # power used on steering motor, between ~60 and 127
        STEERING_POWER = 120

        # TODO: find a better way for this
        # alter direction, needed after mechanical changes
        forward *= -1
        turn *= -1
        # check if forward/backward has to be performed
        # 60 is minimum power and maximum is 127
        if forward < -STEERING_MARGIN:
            self.go_forward(power= int(-60 + 67 * forward))
        if forward > STEERING_MARGIN:
            self.go_forward(power= int(60 + 67 * forward))

        tacho_cur = self.steering_motor.get_tacho().tacho_count

        # stop robot if nothing is found
        if abs(forward) < STEERING_MARGIN:
            self.stop()
        if abs(turn) < STEERING_MARGIN:
            # go to middle position
            print('To middle')
            tacho_diff = self.tacho_middle - tacho_cur
            tacho_steer = not abs(tacho_diff) < 25
            if tacho_diff > 0 and tacho_steer:
                self.steering_motor.turn(
                    power=STEERING_POWER,
                    tacho_units=tacho_diff
                )
            elif tacho_diff < 0 and tacho_steer:
                self.steering_motor.turn(
                    power=-STEERING_POWER,
                    tacho_units=-tacho_diff
                )
        else:  # ...or perform steering by
            # calculating difference to middle position based on turn value
            # avoid oversteering, only use fraction of steering_interval
            tacho_desired = self.tacho_middle + -turn * abs(self.steering_interval) * STEERING_DAMPENING
            tacho_diff = tacho_cur - tacho_desired
            if tacho_diff < 0 and not self.sensors["touch_left"].get_sample():
                self.steering_motor.turn(
                    power=STEERING_POWER,
                    tacho_units=-tacho_diff
                )
            elif tacho_diff > 0 and not self.sensors["touch_right"].get_sample():
                self.steering_motor.turn(
                    power=-STEERING_POWER,
                    tacho_units=tacho_diff
                )

        if tower > 0:
            self.turn_tower(power=60)
        elif tower < 0:
            self.turn_tower(power=-60)
        elif tower == 0:
            self.tower_motor.brake()

        # lock steering_motor
        self.steering_motor.brake()

    def turn_tower(self, power=80):
        self.tower_motor.run(power=power)

    def keep_alive(self):
        '''
        Keeps robot connection alive so it won't turn off automatically after
        time. It will come to weird errors if the robot turns off while the
        server is running. Only option is to terminate the process then.
        Don't even know if this is working, just a theory
        '''
        self.brick.sock.send("DD!")

    def get_telemetry(self):
        '''
        method to acquire sensor data, called e.g. by external modules
        '''

        # Fancy oneliner to create a new dictionary with old keys but new values
        telemetry = {k: v.get_sample() for k, v in self.sensors.items()}

        return telemetry

    def check_color(self):
        '''
        check if underground has white color (= 6)
        '''
        # TODO: check docs and write / use dictionary mapping color codes
        if self.sensors.get("light_color"):
            val = self.sensors["light_color"].get_sample()
            if val == 5:
                return True
            else:
                return False
        else:
            return False

    def self_calibrate(self):
        self.touch_left = self.sensors["touch_left"].get_sample()
        self.touch_right = self.sensors["touch_right"].get_sample()

        if self.touch_left:
            self.max_left = self.steering_motor.get_tacho().tacho_count
            self.steering_interval = (self.max_right - self.max_left) / 2
            self.tacho_middle = self.max_left + self.steering_interval

        if self.touch_right:
            self.max_right = self.steering_motor.get_tacho().tacho_count
            self.steering_interval = (self.max_right - self.max_left) / 2
            self.tacho_middle = self.max_right - self.steering_interval

        '''
        if self.touch_left or self.touch_right:
            self.steering_interval = (self.max_right - self.max_left) / 2
            self.tacho_middle = self.max_left + self.steering_interval
        '''
        print('New calication done, tacho_middle: %s' % self.tacho_middle)

    def check_collision(self):
        '''
        check touch and ultrasonic sensors to detect collisions
        '''
        if self.sensors.get("touch_left") and self.sensors.get("touch_right"):
            self.touch_left = self.sensors["touch_left"].get_sample()
            self.touch_right = self.sensors["touch_right"].get_sample()

            if self.touch_left or self.touch_right:
                return True

        # also check ultrasonic here, its useful if robo drives straight
        # forward towards a wall, so touch sensors cant detect collision
        if self.sensors.get("ultrasonic"):
            self.distance = self.sensors["ultrasonic"].get_sample()
            # TODO: magic number --> config file!
            if self.distance < 6:
                return True

        return False

    def timed_checks(self, ftime):
        '''
        timed collision and color checks done while robo is moving
        '''

        # count times color sensor detects goal color
        color_times = 0

        # color sensor can be a little fuzzy, so one detection does not
        # necessarily mean "goal reached"
        color_times_limit = 3

        # TODO: reset counter after certain amount of time!

        start = time.time()
        while True:
            now = time.time()
            if (now - start) > ftime:
                break
            if self.check_collision():
                self.stop()
                if not self.player.playing_song:
                    self.player.play_song('fail')
                # self.locked = True
                break
            if self.check_color():
                color_times += 1
                if color_times > color_times_limit:
                    self.stop()
                    if not self.player.playing_song:
                        self.player.play_song('success')
                    # self.locked = True
                    break
        return

    def unlock(self):
        '''
        robo is locked when it collides. unlock is called by nxt-control app
        '''
        self.locked = False

    def go_forward(self, power=80):
        for motor in self.motors:
            motor.run(power)

    def stop(self):
        for motor in self.motors:
            motor.idle()
