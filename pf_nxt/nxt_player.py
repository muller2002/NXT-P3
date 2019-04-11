#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Nxt_Player(object):

    '''
    music player for nxt-robots
    '''

    songs = {}

    # playable notes
    freqs = {
        'A0': 220,
        'B0': 233,
        'H0': 247,
        'C0': 262,
        'CIS0': 277,
        'D0': 294,
        'DIS0': 311,
        'E0': 330,
        'F0': 349,
        'FIS0': 370,
        'G0': 392,
        'GIS0': 415,
        'A1': 440,
        'B1': 466,
        'H1': 494,
        'C1': 523,
        'CIS1': 554,
        'D1': 587,
        'DIS1': 622,
        'E1': 659,
        'F1': 698,
        'FIS1': 740,
        'G1': 784,
        'GIS1': 831,
        'A2': 880,
        'B2': 932,
        'H2': 988,
        'C2': 1047,
        'CIS2': 1109,
        'D2': 1175,
        'DIS2': 1245,
        'E2': 1319,
        'F2': 1397,
        'FIS2': 1480,
        'G2': 1568,
        'GIS2': 1661,
        'A3': 1760,
        'B3': 1865,
        'H3': 1976,
        'C3': 2093,
        'CIS3': 2217,
        'D3': 2349,
        'DIS3': 2489,
        'E3': 2637,
        'F3': 2794,
        'FIS3': 2960,
        'G3': 3136,
        'GIS3': 3322
    }

    songs['success'] = {
        'title': 'Success',
        'tacts': [
            {
                'number': 1,
                'notes': [
                    ('C1', 1),
                    ('C1', 1),
                    ('C1', 1),
                    ('E1', 2),
                    ('C1', 1),
                    ('E1', 3)
                ]
            }
        ]
    }

    songs['fail'] = {
        'title': 'Fail',
        'tacts': [
            {
                'number': 1,
                'notes': [
                    ('E0', 1),
                    ('E0', 1),
                    ('E0', 1),
                    ('C0', 3)
                ]
            }
        ]
    }

    songs['march'] = {
        'title': "Imperial March",
        'tacts': [
            {
                'number': 1,
                'notes': [
                    ('G0', 4),
                    ('G0', 4),
                    ('G0', 4),
                    ('DIS0', 3),
                    ('B1', 1)
                ]
            },
            {
                'number': 2,
                'notes': [
                    ('G0', 4),
                    ('DIS0', 3),
                    ('B1', 1),
                    ('G0', 8)
                ]
            },
            {
                'number': 3,
                'notes': [
                    ('D1', 4),
                    ('D1', 4),
                    ('D1', 4),
                    ('DIS1', 3),
                    ('H1', 1)
                ]
            },
            {
                'number': 4,
                'notes': [
                    ('FIS0', 4),
                    ('DIS0', 3),
                    ('H1', 1),
                    ('G0', 8)
                ]
            },
            {
                'number': 5,
                'notes': [
                    ('G1', 4),
                    ('G0', 3),
                    ('G0', 1),
                    ('G1', 4),
                    ('FIS1', 3),
                    ('F1', 1)
                ]
            },
            {
                'number': 6,
                'notes': [
                    ('E1', 1),
                    ('DIS1', 1),
                    ('E1', 4),
                    ('GIS0', 2),
                    ('CIS1', 4),
                    ('C1', 3),
                    ('H1', 1)
                ]
            },
            {
                'number': 7,
                'notes': [
                    ('B1', 1),
                    ('A1', 1),
                    ('B1', 4),
                    ('DIS0', 2),
                    ('FIS0', 4),
                    ('DIS0', 3),
                    ('FIS0', 1)
                ]
            },
            {
                'number': 8,
                'notes': [
                    ('B1', 4),
                    ('G0', 3),
                    ('B1', 1),
                    ('D1', 8)
                ]
            },
            {
                'number': 9,
                'notes': [
                    ('G1', 4),
                    ('G0', 3),
                    ('G0', 1),
                    ('G1', 4),
                    ('FIS1', 3),
                    ('F1', 1)
                ]
            },
            {
                'number': 10,
                'notes': [
                    ('E1', 1),
                    ('DIS1', 1),
                    ('E1', 4),
                    ('GIS0', 2),
                    ('CIS1', 4),
                    ('C1', 3),
                    ('H1', 1)
                ]
            },
            {
                'number': 11,
                'notes': [
                    ('B1', 1),
                    ('A1', 1),
                    ('B1', 4),
                    ('DIS0', 2),
                    ('FIS0', 4),
                    ('DIS0', 3),
                    ('B1', 1)
                ]
            },
            {
                'number': 12,
                'notes': [
                    ('G0', 4),
                    ('DIS0', 3),
                    ('B1', 1),
                    ('G0', 8)
                ]
            }
        ]
    }

    songs['schland'] = {
        'title': "Deutschland-Lied",
        'tacts': [
            {
                'number': 1,
                'notes': [
                    ('F1', 6),
                    ('G1', 2),
                    ('A2', 4),
                    ('G1', 4)
                ]
            },
            {
                'number': 2,
                'notes': [
                    ('B2', 4),
                    ('A2', 4),
                    ('G1', 2),
                    ('E1', 2),
                    ('F1', 4)
                ]
            },
            {
                'number': 3,
                'notes': [
                    ('D2', 4),
                    ('C2', 4),
                    ('B2', 4),
                    ('A2', 4),
                    ('H1', 1)
                ]
            },
            {
                'number': 4,
                'notes': [
                    ('G1', 4),
                    ('A2', 2),
                    ('F1', 2),
                    ('C2', 8),
                ]
            },
            {
                'number': 5,
                'notes': [
                    ('F1', 6),
                    ('G1', 2),
                    ('A2', 4),
                    ('G1', 4)
                ]
            },
            {
                'number': 6,
                'notes': [
                    ('B2', 4),
                    ('A2', 4),
                    ('G1', 2),
                    ('E1', 2),
                    ('F1', 4)
                ]
            },
            {
                'number': 7,
                'notes': [
                    ('D2', 4),
                    ('C2', 4),
                    ('B2', 4),
                    ('A2', 4)
                ]
            },
            {
                'number': 8,
                'notes': [
                    ('G1', 4),
                    ('A2', 2),
                    ('F1', 2),
                    ('C2', 8)
                ]
            },
            {
                'number': 9,
                'notes': [
                    ('G1', 4),
                    ('A2', 4),
                    ('G1', 2),
                    ('E1', 2),
                    ('C1', 4)
                ]
            },
            {
                'number': 10,
                'notes': [
                    ('B2', 4),
                    ('A2', 4),
                    ('G1', 2),
                    ('E1', 2),
                    ('C1', 4)
                ]
            },
            # CONTINUE HERE!!
            {
                'number': 11,
                'notes': [
                    ('B1', 1),
                    ('A1', 1),
                    ('B1', 4),
                    ('DIS0', 2),
                    ('FIS0', 4),
                    ('DIS0', 3),
                    ('B1', 1)
                ]
            },
            {
                'number': 12,
                'notes': [
                    ('G0', 4),
                    ('DIS0', 3),
                    ('B1', 1),
                    ('G0', 8)
                ]
            }
        ]
    }

    '''
    def play_schland(self, v = 150, times = 1):
        #schland
        for i in range(times):
            self.brick.play_tone_and_wait(self.freqs['F1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['D2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)

            self.brick.play_tone_and_wait(self.freqs['F1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['D2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)

            self.brick.play_tone_and_wait(self.freqs['G1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C1'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)

            self.brick.play_tone_and_wait(self.freqs['H2'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['H2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 8*v)

            self.brick.play_tone_and_wait(self.freqs['G2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['E2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['E2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['D2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['D2'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 4*v)

            self.brick.play_tone_and_wait(self.freqs['G1'], 6*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], v)
            self.brick.play_tone_and_wait(self.freqs['B2'], v)
            self.brick.play_tone_and_wait(self.freqs['C2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['D2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['B2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)

            self.brick.play_tone_and_wait(self.freqs['F1'], 4*v)
            self.brick.play_tone_and_wait(self.freqs['A2'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['G1'], 2*v)
            self.brick.play_tone_and_wait(self.freqs['F1'], 8*v)
    '''

    def __init__(self, brick):
        self.brick = brick
        self.playing_song = False
        self.stopped = False
        self.curr_tact = 0

    def play_song(self, song_name='march', v=150, times=1):
        song = self.songs.get(song_name)
        if not self.playing_song:
            self.playing_song = True
            print('playing {} now...'.format(song['title']))
            tones = self.freqs
            for i in range(times):
                tact_count = len(song['tacts'])
                tact_start = self.curr_tact
                for i in range(tact_start, tact_count):
                    tact = song['tacts'][i]
                    notes = tact['notes']
                    self.curr_tact = tact['number'] - 1
                    for note in notes:
                        if not self.stopped:
                            freq = tones[note[0]]
                            length = note[1]
                            self.brick.play_tone_and_wait(freq, length * v)
                        else:
                            print('got interrupt, stopped playing...')
                            self.playing_song = False
                            return

            self.playing_song = False
            self.curr_tact = 0
            print('done playing...')
            return
        else:
            print('Error: Already playing...')
            return


if __name__ == '__main__':
    test_player = Nxt_Player('foo')
