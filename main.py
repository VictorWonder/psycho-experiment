import argparse

from psychopy.gui import Dlg

from window import MyDialog, MyWindow

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hitnum_mean', type=int,
                        default=10,
                        help='average number of hits')
    parser.add_argument('--hitnum_adjust', type=int,
                        default=5,
                        help='adjust number of hits')
    parser.add_argument('--trials', type=int,
                        default=10,
                        help='rounds of trials')
    args = parser.parse_args()

    info_dialog = MyDialog(title='被试信息采集')
    user_info = info_dialog.collect_info()

    main_window = MyWindow(total_trials=args.trials,
                           hitnum_mean=args.hitnum_mean,
                           hitnum_adjust=args.hitnum_adjust,
                           user_info=user_info)
    main_window.run()
