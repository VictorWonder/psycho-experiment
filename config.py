import os

import yaml
from PyQt5.QtWidgets import QDialog, QWidget, \
        QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, \
        QPushButton, QLabel, QLineEdit, QSpinBox

from utils import AttrDict, report_error_info, \
        clean_upper_and_bottom_margins


class ConfigWindow(QDialog):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_options())
        main_layout.addWidget(self.create_buttons())

        self.setLayout(main_layout)
        self.setFixedSize(main_layout.sizeHint())
        self.setWindowTitle('Configure')

    def create_options(self):
        layout = QVBoxLayout()

        related_widgets = {}
        for key, value in self.options.items():
            label = QLabel(key)

            if type(value) is int:
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
            layout.addLayout(sub_layout)
            related_widgets[key] = item

        clean_upper_and_bottom_margins(layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.related_widgets = related_widgets
        return widget

    def create_buttons(self):
        accept_button = QPushButton('OK', self)
        accept_button.setFixedWidth(100)
        accept_button.clicked.connect(self.accept_modify)

        layout = QHBoxLayout()
        layout.addWidget(accept_button)
        clean_upper_and_bottom_margins(layout)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def accept_modify(self):
        for key, item in self.related_widgets.items():
            if type(self.options[key]) is int:
                self.options[key] = item.value()
        self.accept()


def load_options(path: str,
                 modify: bool = False,
                ):
    assert os.path.exists(path)

    options = yaml.safe_load(open(path))
    if modify:
        config_window = ConfigWindow(options)
        config_window.exec()
        yaml.safe_dump(options, open(path, 'w'), sort_keys=False)

    return AttrDict(options)
