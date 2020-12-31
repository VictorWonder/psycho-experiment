from PyQt5.QtWidgets import QDialog, QWidget, \
        QVBoxLayout, QHBoxLayout, \
        QLabel, QComboBox, QLineEdit, QSpinBox

from utils.common import report_error_info
from base.dialog import DialogBase


class UserDialog(DialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.collected_info = None
        self.widgets = {}
        self.main_layout.insertLayout(0, self.create_items())

        self.setFixedSize(self.main_layout.sizeHint())
        self.setWindowTitle('被试信息采集')

    def new_item(self,
                 key: str,
                 text: str,
                 default = None,
                 choices = None,
                 value_range = None,
                ):
        label = QLabel(text)
        if choices is not None:
            item = QComboBox()
            item.addItems(choices)
            if default is not None:
                assert default in choices
                item.setCurrentText(default)
        elif value_range is not None:
            assert len(value_range) == 2
            min_value = value_range[0]
            max_value = value_range[1]
            if min_value > max_value:
                min_value, max_value = max_value, min_value
            item = QSpinBox()
            item.setRange(min_value, max_value)
            if default is not None:
                if default < min_value:
                    default = min_value
                elif default > max_value:
                    default = max_value
                item.setValue(default)
        else:
            item = QLineEdit()

        label.setBuddy(item)
        item.setFixedWidth(100)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(item)

        self.widgets[key] = item
        return layout

    def create_items(self):
        layout = QVBoxLayout()
        layout.addLayout(self.new_item('name',
                                       '姓名：'))
        layout.addLayout(self.new_item('age',
                                       '年龄：',
                                       default=20,
                                       value_range=[10, 60]))
        layout.addLayout(self.new_item('sex',
                                       '性别：',
                                       choices=['男', '女']))
        layout.addLayout(self.new_item('hand',
                                       '惯用手：',
                                       default='右手',
                                       choices=['左手', '右手']))
        return layout

    def accept_func(self):
        info = {}
        for key, item in self.widgets.items():
            if isinstance(item, QLineEdit):
                info[key] = item.text()
                if len(info[key]) <= 0:
                    report_error_info('请完整填写信息')
                    return
            elif isinstance(item, QComboBox):
                info[key] = item.currentIndex()
            elif isinstance(item, QSpinBox):
                info[key] = item.value()

        self.collected_info = info
        self.accept()


def obtain_user_info():
    user_dialog = UserDialog()
    user_dialog.exec()
    if user_dialog.collected_info is None:
        report_error_info('信息采集失败', end=True)
    else:
        return user_dialog.collected_info
