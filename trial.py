import random
from typing import Tuple
from dataclasses import dataclass

import numpy as np
from psychopy import event, core
from psychopy.visual import Rect


all_modes = ['constant', 'random']

class Point(object):
    def __init__(self,
                 window,
                 pos,
                 shape_type = 'rectangle',
                 size = None,
                 color = 'black',
                ):
        self.window = window
        self.x, self.y = pos[0], pos[1]

        if shape_type == 'rectangle':
            if size is None:
                self.size = (10, 10)
            else:
                self.size = size
            self.stim = Rect(win=window,
                             units='pix',
                             size=self.size,
                             pos=(self.x, self.y),
                             lineColor=color,
                             fillColor=color)
        else:
            raise Exception('unavilable shape of point')

    def draw(self):
        self.stim.draw()
        self.window.flip(True)

    def change(self, change_x, change_time):
        self.x += change_x
        self.stim.setPos((self.x, self.y))
        core.wait(change_time / 1000)
        self.draw()


class Trial(object):
    @dataclass
    class TrialOptions(object):
        point_type = 'rect'
        rect_size = (8.0, 8.0)
        average_hitnum: int = 5
        adjust_hitnum: int = 2

    def __init__(self,
                 window,
                 options,
                 view_distance,
                 px_size,
                 mode = 'constant'
                ):
        self.window = window
        self.options = options
        self.mode = mode
        self.view_distance = view_distance
        self.px_size = px_size

        assert mode in all_modes

        self.space_seq = []
        self.time_seq_plan = []
        self.time_seq = []
        self.resp = []
        self.resp_time = []
        self.rate_val = []

        # TODO: change value in trial options
        self.space_mean = round(np.tan(np.pi * 2 / 180) * \
                                view_distance / \
                                px_size / 2)
        self.space_var = round(np.tan(np.pi * 2.5 / 180) * \
                               view_distance / \
                               px_size / 2)
        self.time_mean = 400
        self.time_var = 300

        start_pos, hitnum, change_x, change_time = \
                self.generate_sequences()
        self.point = Point(window, start_pos)

        self.window.show_message('请按“空格键”开始。')
        flag = False
        while True:
            keys = event.waitKeys()
            for key in keys:
                if key == 'space':
                    flag = True
                    break
            if flag:
                break
        self.window.flip(True)

        core.wait(0.5)
        self.point.draw()

        for i in range(hitnum):
            keys = event.waitKeys(keyList=['left', 'right'])
            if keys[0] == 'left':
                hit_direction = -1
            elif keys[0] == 'right':
                hit_direction = 1
            self.point.change(change_x[i] * hit_direction, change_time[i])


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

        hitnum = self.options.average_hitnum + \
                random.randint(-self.options.adjust_hitnum,
                               self.options.adjust_hitnum)
        change_x = [random.uniform(self.space_mean - self.space_var,
                                   self.space_mean + self.space_var)
                    for i in range(hitnum)]
        change_time = [random.uniform(self.time_mean - self.time_var,
                                      self.time_mean + self.time_var)
                       for i in range(hitnum)]

        return (x0, y0), hitnum, change_x, change_time

    def score(self):
        pass
