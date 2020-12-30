import sys
import argparse

from PyQt5.QtWidgets import QApplication, QStyleFactory

from config import load_options
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

    info_dialog = MyDialog(title='被试信息采集')
    user_info = info_dialog.collect_info()

    main_window = MainWindow(options=options,
                             user_info=user_info)
    main_window.run()
