from getch import _Getch

class Keyboard:
    def __init__(self):
        self.bindings = {}

    def bind(self, key, callback):
        self.bindings[key] = callback
    
    def run(self, exit_key):
        getch = _Getch()
        while True:
            key = ord(getch())
            if key in self.bindings.keys():
                self.bindings[key]()
            if key == exit_key:
                break