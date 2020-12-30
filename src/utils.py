from PyQt5.QtWidgets import QMessageBox

def report_error_info(self, info='Error!', end=False):
    message_box = QMessageBox()
    message_box.setText(info)
    message_box.exec()

    if end:
        exit()

def clean_upper_and_bottom_margins(layout):
    left, top, right, bottom = layout.getContentsMargins()
    layout.setContentsMargins(left, 0, right, 0)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        self[key] = value

    @property
    def __dict__(self):
        return self
