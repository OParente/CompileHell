import ctypes, os
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_lib = os.path.join(_root, 'engine', 'libcompilehell.so')
_lib = os.path.abspath(_lib)

_h = ctypes.CDLL(_lib)

_h.engine_init.restype = None
_h.engine_draw_sprite.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_h.engine_draw_sprite.restype = None
_h.engine_update.restype = None

def init():
    _h.engine_init()

def draw_sprite(name, x, y):
    _h.engine_draw_sprite(name.encode('utf-8'), int(x), int(y))

def update():
    _h.engine_update()
