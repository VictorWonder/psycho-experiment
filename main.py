from psychopy import visual, core, event
from window import MyWindow

if __name__ == '__main__':
    main_window = MyWindow()
    main_window.initialize()

    keys = event.waitKeys(keyList=['space'])
    for key in keys:
        if key == 'space':
            main_window.flip(True)
            main_window.start_trial()

    main_window.finish()
