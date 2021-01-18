import os
import time
import random
from typing import Dict

from psychopy import visual, core, event
from psychopy.event import Mouse
from psychopy.monitors import Monitor
from psychopy.visual import Window, TextStim, ShapeStim, Rect, \
        RatingScale, Slider

from trial.trial import Trial, all_trial_modes


class MainWindow(Window):
    def __init__(self,
                 options,
                 pixel_size,
                 physical_size,
                 user_info,
                ):
        monitor = Monitor('currentMonitor',
                          width=physical_size[0],
                          distance=user_info['view_distance'],
                          gamma=1.0,
                          notes='')

        super().__init__(
            size=pixel_size,
            waitBlanking=False,
            monitor='testMonitor',
            fullscr=True,
            units='deg',
        )

        self.options = options
        self.user_info = user_info

        self.pixel_size = pixel_size
        self.physical_size = physical_size
        # px_size is cm per pixel
        self.px_size = physical_size[0] / pixel_size[0]
        self.view_distance = user_info['view_distance']

        self.scale = RatingScale(self,
                                 scale='选择分数之后请按“空格键”确认',
                                 low=0,
                                 high=1000,
                                 tickMarks=[0, 1000],
                                 labels=('无法控制', '完全控制'),
                                 leftKeys=None,
                                 rightKeys=None,
                                 acceptKeys='space',
                                 showAccept=False,
                                 pos=(0.0, 0.0))

        self.mouse = Mouse(visible=False, win=self)
        self.mouseVisible = False

        event.globalKeys.clear()
        event.globalKeys.add(key='escape', func=core.quit)

        self.show_message(
            '现在是练习部分。\n'
            '请您按照自己舒适的节奏随机按左键或右键，\n'
            '每次仅按一下，两次之间的间隔不要少于一秒。\n'
            '于此同时，请观察屏幕上黑色方块的运动，\n'
            '在其消失之后判断你对其运动的控制成都，\n'
            '并在相应的标尺上点击确认您的判断。\n'
            '请按“空格键”开始，或按“退出键”跳出练习。'
        )

    # print message in the center of screen
    def show_message(self, text):
        printer = TextStim(self, text=text)
        printer.draw()
        self.flip(True)

    def start_trials(self):
        all_trials = []
        mode_num = len(all_trial_modes)
        for trial_round in range(self.options.total_trials):
            mode_idx = random.randint(0, mode_num - 1)
            trial = Trial(self,
                          self.view_distance,
                          self.px_size,
                          self.options,
                          mode=all_trial_modes[mode_idx])
            trial.start()
            score = self.get_score()
            all_trials.append((trial, score))
        self.all_trials = all_trials

    def get_score(self):
        self.mouse.setVisible(True)
        self.mouse.setPos((0, 0))
        self.scale.reset()
        while self.scale.noResponse:
            self.scale.draw()
            self.flip(True)
        self.mouse.setVisible(False)
        return self.scale.getRating()

    def finish(self):
        self.show_message(
            '实验到此结束\n'
            '非常感谢您的参与。'
        )
        keys = event.waitKeys(keyList=['space'])
        self.save_data()
        del self.scale
        core.quit()

    def run(self):
        keys = event.waitKeys(keyList=['space'])
        for key in keys:
            if key == 'space':
                self.flip(True)
                self.start_trials()

        self.finish()

    def save_data(self):
        data_dir = '../data/'
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        filename = '{} {}'.format(self.user_info['name'], date)
        fout = open(os.path.join(data_dir, filename), 'w')
        fout.write('姓名：{}\n'.format(self.user_info['name']))
        fout.write('年龄：{}\n'.format(self.user_info['age']))
        fout.write('性别：{}\n'.format('男' if self.user_info['sex'] == 0 \
                                          else '女'))
        fout.write('惯用手：{}\n'.format('左手' if self.user_info['hand'] == 0 \
                                             else '右手'))
        fout.write('视距 (cm): {}\n'.format(self.user_info['view_distance']))
        fout.write('\n')

        for idx, (trial, score) in enumerate(self.all_trials):
            fout.write('trial {}\n'.format(idx + 1))
            fout.write(trial.dumps() + '\n')

