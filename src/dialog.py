from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, \
        QVBoxLayout, \
        QPushButton


class DialogBase(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.create_button(),
                                   alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def create_button(self):
        accept_button = QPushButton('OK', self)
        accept_button.setFixedWidth(100)
        accept_button.clicked.connect(self.accept_func)
        return accept_button

    def accept_func(self):
        self.accept()
