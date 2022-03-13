from pynput import keyboard
import sys


class KeyDetector:

    def __init__(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.active_key = []

    def start(self):
        self.listener.start()

    def clear(self):
        self.active_key = []

    def on_press(self, key):
        try:
            # print('alphanumeric key {0} pressed'.format(key.char))
            if key.char not in self.active_key:
                self.active_key.append(key.char)
                # print(type(key.char))
        except AttributeError:
            pass
            # print('special key {0} pressed'.format(key))
            # print(type(key))
        # print("!!", self.active_key)

    def on_release(self, key):
        # print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            sys.exit()
            # return False
