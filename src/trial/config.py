import os

import yaml
from PyQt5.QtWidgets import QDialog, QWidget, \
        QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, \
        QPushButton, QLabel, QLineEdit, QSpinBox, QPlainTextEdit

from utils.common import AttrDict, report_error_info, \
        clean_upper_and_bottom_margins
from base.dialog import DialogBase


class ConfigDialog(DialogBase):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        self.main_layout.insertLayout(0, self.create_config())

        self.setFixedSize(self.main_layout.sizeHint())
        self.setWindowTitle('Configure')

    def create_config(self):
        layout = QVBoxLayout()

        related_widgets = {}
        for key, config_item in self.config.items():
            name = config_item['name']
            value = config_item['value']
            unit = config_item['unit']

            label = QLabel(name)
            if isinstance(value, int):
                widget = QSpinBox()
                widget.setFixedWidth(100)
                widget.setValue(value)
                if 'range' in config_item:
                    min_value = min(config_item['range'])
                    max_value = max(config_item['range'])
                else:
                    min_value = 1
                    max_value = 50
                widget.setRange(min_value, max_value)
            elif isinstance(value, float):
                widget = QLineEdit()
                widget.setFixedWidth(100)
                widget.setText(str(value))
            else:
                raise Exception("unavailable option type" 
                                " '{}'".format(type(value)))
            if unit is not None:
                unit_text = QLabel(unit)
            else:
                unit_text = QLabel('')
            unit_text.setFixedWidth(50)

            label.setBuddy(widget)
            sub_layout = QHBoxLayout()
            sub_layout.addWidget(label)
            sub_layout.addWidget(widget)
            sub_layout.addWidget(unit_text)
            clean_upper_and_bottom_margins(sub_layout)
            layout.addLayout(sub_layout)
            related_widgets[key] = widget

        self.related_widgets = related_widgets

        clean_upper_and_bottom_margins(layout)
        return layout

    def accept_func(self):
        for key, widget in self.related_widgets.items():
            if isinstance(self.config[key]['value'], int):
                self.config[key]['value'] = widget.value()
            elif isinstance(self.config[key]['value'], float):
                self.config[key]['value'] = float(widget.text())
        self.accept()


def load_options(path: str,
                 modify: bool = False,
                ):
    assert os.path.exists(path)

    config = yaml.safe_load(open(path))
    if modify:
        config_dialog = ConfigDialog(config)
        config_dialog.exec()
        yaml.safe_dump(config,
                       open(path, 'w'),
                       sort_keys=False,
                       indent=4,
                       allow_unicode=True)

    options = {}
    for key, item in config.items():
        options[key] = item['value']

    return AttrDict(options)
