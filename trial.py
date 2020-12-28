import random
from typing import Tuple
from dataclasses import dataclass

import numpy as np
from psychopy import event, core, visual
from psychopy.visual import Rect


all_trial_modes = ['constant', 'random']

class Point(object):
    def __init__(self,
                 win,
                 pos,
                 shape_type = 'rectangle',
                 size = None,
                 color = 'black',
                ):
        self.win = win
        self.x, self.y = pos[0], pos[1]

        if shape_type == 'rectangle':
            if size is None:
                self.size = (10, 10)
            else:
                self.size = size
            self.stim = Rect(win=win,
                             units='pix',
                             size=self.size,
                             pos=(self.x, self.y),
                             lineColor=color,
                             fillColor=color)
        else:
            raise Exception('unavilable shape of point')

    def draw(self):
        self.stim.draw()
        self.win.flip(True)

    def change(self, change_x, change_time):
        self.x += change_x
        self.stim.setPos((self.x, self.y))
        core.wait(change_time / 1000)
        self.draw()


class Trial(object):
    def __init__(self,
                 win: visual.Window,
                 view_distance: float,
                 px_size: float,
                 hitnum_mean: int,
                 hitnum_adjust: int,
                 mode: str = 'constant'
                ):
        if mode not in all_trial_modes:
            raise Exception("unavailable trial mode '{}'".format(mode))

        self.win = win
        self.mode = mode
        self.hitnum_mean = hitnum_mean
        self.hitnum_adjust = hitnum_adjust
        self.view_distance = view_distance
        self.px_size = px_size

        self.space_seq = []
        self.time_seq_plan = []
        self.time_seq = []
        self.resp = []
        self.resp_time = []
        self.rate_val = []

        # TODO: change value according to options
        self.space_mean = round(np.tan(np.pi * 2 / 180) * \
                                view_distance / \
                                px_size / 2)
        self.space_var = round(np.tan(np.pi * 2.5 / 180) * \
                               view_distance / \
                               px_size / 2)
        self.time_mean = 400
        self.time_var = 300

        start_pos = \
                self.generate_sequences()
        self.point = Point(win, start_pos)

        self.win.show_message('请按“空格键”开始。')
        flag = False
        while True:
            keys = event.waitKeys()
            for key in keys:
                if key == 'space':
                    flag = True
                    break
            if flag:
                break
        self.win.flip(True)

        core.wait(0.5)
        self.point.draw()

    def generate_sequences(self,
                           pos = None,
                          ):
        if pos is None:
            x0, y0 = 0, 0
            if random.randint(0, 1) == 1:
                x0 += round(np.tan(np.pi * 5 / 180) * \
                            self.view_distance / \
                            self.px_size / 2)
            else:
                x0 -= round(np.tan(np.pi * 5 / 180) * \
                            self.view_distance / \
                            self.px_size / 2)
        else:
            assert len(pos) == 2
            x0, y0 = pos[0], pos[1]

        self.hitnum = self.hitnum_mean + \
                random.randint(-self.hitnum_adjust, self.hitnum_adjust)
        self.change_x = [random.uniform(self.space_mean - self.space_var,
                                        self.space_mean + self.space_var)
                         for i in range(self.hitnum)]
        self.change_time = [random.uniform(self.time_mean - self.time_var,
                                           self.time_mean + self.time_var)
                            for i in range(self.hitnum)]

        return (x0, y0)

    def start(self):
        for i in range(self.hitnum):
            keys = event.waitKeys(keyList=['left', 'right'])
            if keys[0] == 'left':
                hit_direction = -1
            elif keys[0] == 'right':
                hit_direction = 1
            self.point.change(self.change_x[i] * hit_direction,
                              self.change_time[i])

    def score(self):
        pass
