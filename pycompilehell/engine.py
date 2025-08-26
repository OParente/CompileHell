import os
import sys
import ctypes

if sys.platform.startswith("linux"):
    libfile = os.path.join(os.path.dirname(__file__), "..", "engine", "libcompilehell.so")
elif sys.platform == "darwin":
    libfile = os.path.join(os.path.dirname(__file__), "..", "engine", "libcompilehell.dylib")
else:
    libfile = os.path.join(os.path.dirname(__file__), "..", "engine", "compilehell.dll")

_ch = ctypes.CDLL(libfile)

# Inicialização
_ch.compilehell_init.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_ch.compilehell_init.restype = ctypes.c_int
def init(title, w, h):
    return _ch.compilehell_init(title.encode(), w, h)

# Loop
_ch.compilehell_is_running.restype = ctypes.c_int
def is_running():
    return bool(_ch.compilehell_is_running())

_ch.compilehell_poll_events.restype = None
def poll_events():
    _ch.compilehell_poll_events()

# Render
_ch.compilehell_set_draw_color.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_ch.compilehell_set_draw_color.restype = None
def set_draw_color(r, g, b, a):
    _ch.compilehell_set_draw_color(r, g, b, a)

_ch.compilehell_clear.restype = None
def clear():
    _ch.compilehell_clear()

_ch.compilehell_present.restype = None
def present():
    _ch.compilehell_present()

# Shutdown
_ch.compilehell_shutdown.restype = None
def shutdown():
    _ch.compilehell_shutdown()

_ch.compilehell_update_fps.restype = None
def update_fps():
    _ch.compilehell_update_fps()

# Exponha o tipo Entity* para outros módulos
EntityPtr = ctypes.c_void_p

# Expor _ch para outros módulos se necessário
lib = _ch