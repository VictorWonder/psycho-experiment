import os

import yaml
from PyQt5.QtWidgets import QDialog, QWidget, \
        QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, \
        QPushButton, QLabel, QLineEdit, QSpinBox

from utils import AttrDict, report_error_info, \
        clean_upper_and_bottom_margins
from dialog import DialogBase


class ConfigDialog(DialogBase):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options

        self.main_layout.insertLayout(0, self.create_options())

        self.setFixedSize(self.main_layout.sizeHint())
        self.setWindowTitle('Configure')

    def create_options(self):
        layout = QVBoxLayout()

        related_widgets = {}
        for key, value in self.options.items():
            label = QLabel(key)

            if isinstance(value, int):
                item = QSpinBox()
                item.setFixedWidth(100)
                item.setValue(value)
                item.setRange(1, 50)
            else:
                raise Exception("unavailable option type" 
                                " '{}'".format(type(value)))

            label.setBuddy(item)
            sub_layout = QHBoxLayout()
            sub_layout.addWidget(label)
            sub_layout.addWidget(item)
            clean_upper_and_bottom_margins(sub_layout)
            layout.addLayout(sub_layout)
            related_widgets[key] = item

        self.related_widgets = related_widgets

        clean_upper_and_bottom_margins(layout)
        return layout

    def accept_func(self):
        for key, item in self.related_widgets.items():
            if isinstance(self.options[key], int):
                self.options[key] = item.value()
        self.accept()


def load_options(path: str,
                 modify: bool = False,
                ):
    assert os.path.exists(path)

    options = yaml.safe_load(open(path))
    if modify:
        config_dialog = ConfigDialog(options)
        config_dialog.exec()
        yaml.safe_dump(options, open(path, 'w'), sort_keys=False)

    return AttrDict(options)
