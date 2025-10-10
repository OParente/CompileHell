import ctypes
from .engine import lib as _ch
from . import camera as c

class EntityStruct(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("w", ctypes.c_float),
        ("h", ctypes.c_float),
        ("camx", ctypes.c_float),
        ("camy", ctypes.c_float),
        ("texture", ctypes.c_void_p),
        ("flip_h", ctypes.c_int),
        ("flip_v", ctypes.c_int),
    ]

class Entity:
    def __init__(self, texture_path, x, y, camx, camy, w=64, h=64):
        _ch.compilehell_create_entity.argtypes = [ctypes.c_char_p, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        _ch.compilehell_create_entity.restype = ctypes.c_void_p
        self._native = _ch.compilehell_create_entity(texture_path.encode(), float(x), float(y), float(w), float(h), float(camx), float(camy))
        if not self._native:
            raise RuntimeError(f"Falha ao criar entidade: {texture_path}")
        self._struct = EntityStruct.from_address(self._native)
        self._scripts = []

    @property
    def x(self):
        return self._struct.x
    @x.setter
    def x(self, value):
        self._struct.x = value

    @property
    def camx(self):
        return self._struct.camx
    @x.setter
    def camx(self, value):
        self._struct.camx = value

    @property
    def y(self):
        return self._struct.y
    @y.setter
    def y(self, value):
        self._struct.y = value

    @property
    def camy(self):
        return self._struct.camy
    @y.setter
    def camy(self, value):
        self._struct.camy = value

    @property
    def w(self):
        return self._struct.w
    @w.setter
    def w(self, value):
        self._struct.w = value

    @property
    def h(self):
        return self._struct.h
    @h.setter
    def h(self, value):
        self._struct.h = value

    @property
    def flip_h(self):
        return bool(self._struct.flip_h)
    @flip_h.setter
    def flip_h(self, value):
        self._struct.flip_h = int(bool(value))

    @property
    def flip_v(self):
        return bool(self._struct.flip_v)
    @flip_v.setter
    def flip_v(self, value):
        self._struct.flip_v = int(bool(value))

    def add_script(self, script_obj):
        self._scripts.append(script_obj)

    def update(self, dt):
        for script in self._scripts:
            if hasattr(script, "on_update"):
                script.on_update(self, dt)

    def draw(self):
        _ch.compilehell_draw_entity.argtypes = [ctypes.c_void_p]
        _ch.compilehell_draw_entity.restype = None
        _ch.compilehell_draw_entity(self._native)

    def move(self, dx, dy):
        _ch.compilehell_move_entity.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
        _ch.compilehell_move_entity.restype = None
        _ch.compilehell_move_entity(self._native, float(dx), float(dy))

    def destroy(self):
        _ch.compilehell_destroy_entity.argtypes = [ctypes.c_void_p]
        _ch.compilehell_destroy_entity.restype = None
        if self._native:
            _ch.compilehell_destroy_entity(self._native)
            self._native = None

    def collides_with(self, other):
        _ch.compilehell_check_collision.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        _ch.compilehell_check_collision.restype = ctypes.c_int
        return bool(_ch.compilehell_check_collision(self._native, other._native))

    def would_collide(self, other, dx, dy):
        _ch.compilehell_would_collide.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
        _ch.compilehell_would_collide.restype = ctypes.c_int
        return bool(_ch.compilehell_would_collide(self._native, other._native, dx, dy))

    def is_key_down(self, scancode):
        return bool(_ch.compilehell_is_key_down(scancode))
    def get_mouse(self):
        return _ch.compilehell_get_mouse()
    def is_mouse_down(self, button: int):
        return _ch.compilehell_is_mouse_down(button)
