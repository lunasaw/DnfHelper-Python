import keyboard

from common import globle, mem
from game.func import FullScreen


def main():
    globle.process_id = 5080
    mem.set_process_id(globle.process_id)

    fullScreen = FullScreen()
    keyboard.add_hotkey('END', fullScreen.SkillSwitch)
    keyboard.wait()

    while 1:
        keyboard.wait('')


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err.args)