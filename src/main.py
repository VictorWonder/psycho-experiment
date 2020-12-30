import sys
import argparse

from PyQt5.QtWidgets import QApplication, QStyleFactory

from config import load_options
from user import obtain_user_info
from window import MainWindow

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str,
                        default='./config.yml',
                        help='path to config file')
    parser.add_argument('-m', '--modify',
                        action='store_true',
                        help='change config')
    args = parser.parse_args()

    # initialize PyQt5 window style
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    # load options
    options = load_options(args.config, args.modify)

    # obtain user info
    user_info = obtain_user_info()

    main_window = MainWindow(options=options,
                             user_info=user_info)
    main_window.run()
