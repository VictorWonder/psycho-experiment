import random
from typing import Tuple
from dataclasses import dataclass

import numpy as np
from psychopy import event, core, visual
from psychopy.visual import Rect, RatingScale
from psychopy.core import Clock


all_trial_modes = ['constant', 'random']
all_scorer_types = ['line']


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
                 options: dict,
                 mode: str = 'constant'
                ):
        if mode not in all_trial_modes:
            raise Exception("unavailable trial mode '{}'".format(mode))

        self.win = win
        self.mode = mode
        self.hitnum_mean = options['hitnum_mean']
        self.hitnum_adjust = options['hitnum_adjust']
        self.angle_mean = options['angle_mean']
        self.angle_var = options['angle_var']
        self.angle_init = options['angle_init']
        self.view_distance = view_distance
        self.px_size = px_size

        self.space_seq = []
        self.time_seq_plan = []
        self.time_seq = []
        self.resp = []
        self.resp_time = []
        self.rate_val = []

        # TODO: change value according to options
        self.space_mean = round(np.tan(np.pi * self.angle_mean / 180) * \
                                self.view_distance / \
                                self.px_size)
        self.space_var = round(np.tan(np.pi * self.angle_var / 180) * \
                               self.view_distance / \
                               self.px_size)

        self.time_mean = options['time_mean']
        self.time_var = options['time_var']
        # TODO: predict user reaction if time_var < time_mean
        if self.time_var > self.time_mean:
            self.time_var = self.time_mean

        start_pos = \
                self.generate_sequences()
        self.point = Point(win, start_pos)

        self.win.show_message('请按“空格键”开始。')
        keys = event.waitKeys(keyList=['space'])
        self.win.flip(True)

        self.point.draw()

    def generate_sequences(self,
                           pos = None,
                          ):
        if pos is None:
            x0, y0 = 0, 0
            if random.randint(0, 1) == 1:
                x0 += round(np.tan(np.pi * self.angle_init / 180) * \
                            self.view_distance / \
                            self.px_size)
            else:
                x0 -= round(np.tan(np.pi * self.angle_init / 180) * \
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
        timer = Clock()
        timer.reset()
        for i in range(self.hitnum):
            keys = event.waitKeys(keyList=['left', 'right'],
                                  timeStamped=timer)
            key = keys[0][0]
            key_time = keys[0][1]
            if key == 'left':
                hit_direction = -1
            elif key == 'right':
                hit_direction = 1
            # TODO: control the point not exceed boundry
            self.point.change(self.change_x[i] * hit_direction,
                              self.change_time[i])
            flip_time = timer.getTime()

            # record
            self.space_seq.append(self.change_x[i] * hit_direction)
            self.time_seq_plan.append(self.change_time[i])
            self.time_seq.append(1000 * (flip_time - key_time))
            self.resp.append(hit_direction)
            self.resp_time.append(1000 * key_time)

    def dumps(self):
        space_seq = ' '.join(str(x) for x in self.space_seq)
        time_seq_plan = ' '.join(str(x) for x in self.time_seq_plan)
        time_seq = ' '.join(str(x) for x in self.time_seq)
        resp = ' '.join(str(x) for x in self.resp)
        resp_time = ' '.join(str(x) for x in self.resp_time)

        ret = 'mode: {}\n' \
              'space_seq: {}\n' \
              'time_seq_plan: {}\n' \
              'time_seq: {}\n' \
              'resp: {}\n' \
              'resp_time: {}\n'.format(self.mode,
                                       space_seq,
                                       time_seq_plan,
                                       time_seq,
                                       resp,
                                       resp_time)
        return ret
