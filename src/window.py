import random
from typing import Dict

from psychopy import visual, core, event
from psychopy.gui import Dlg
from psychopy.visual import Window, TextStim, ShapeStim, Rect

from trial import Trial, all_trial_modes


class MyDialog(Dlg):
    def __init__(self, title: str = None):
        super().__init__(title=title)

        # return of addField is a QtObject
        self.name: 'QLineEdit' = self.addField('姓名：')
        self.age: 'QLineEdit' = self.addField('年龄：')
        self.sex: 'QComboBox' = self.addField('性别：', choices=['男', '女'])
        self.hand: 'QComboBox' = self.addField('惯用手：',
                                               initial='右手',
                                               choices=['左手', '右手'])

    def collect_info(self):
        while True:
            self.show()
            if self.OK:
                ret = {}
                ret['name'] = self.name.text()
                try:
                    ret['age'] = int(self.age.text().strip())
                    if ret['age'] <= 10 or ret['age'] >= 80:
                        raise Exception('error')
                except:
                    self.report_error('年龄填写出错，请重新填写')
                    continue
                ret['sex'] = self.sex.currentIndex()
                ret['hand'] = self.hand.currentIndex()
                break
            else:
                self.report_error('信息收集失败', end=True)

    def report_error(self, message: str, end=False):
        message_dialog = Dlg(title='Error')
        message_dialog.addText(message)
        message_dialog.show()
        if end:
            exit(-1)


class MainWindow(Window):
    def __init__(self,
                 total_trials: int = 10,
                 hitnum_mean: int = 10,
                 hitnum_adjust: int = 5,
                 user_info: Dict[str, int] = None
                ):
        super().__init__(
            size=(1920, 1080),
            waitBlanking=False,
            fullscr=True,
            monitor='testMonitor',
            units='deg',
        )

        self.total_trials = total_trials
        self.hitnum_mean = hitnum_mean
        self.hitnum_adjust = hitnum_adjust

        self.px_size = self.scrWidthCM / self.scrWidthPIX
        self.view_distance = 40

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

    def quit(self):
        pass

    def start_trials(self):
        mode_num = len(all_trial_modes)
        for trial_round in range(self.total_trials):
            mode_idx = random.randint(0, mode_num - 1)
            trial = Trial(self,
                          self.view_distance,
                          self.px_size,
                          self.hitnum_mean,
                          self.hitnum_adjust,
                          mode=all_trial_modes[mode_idx])
            trial.start()

    def finish(self):
        self.show_message(
            '实验到此结束\n'
            '非常感谢您的参与。'
        )
        keys = event.waitKeys(keyList=['space'])

    def run(self):
        keys = event.waitKeys(keyList=['space'])
        for key in keys:
            if key == 'space':
                self.flip(True)
                self.start_trials()

        self.finish()
