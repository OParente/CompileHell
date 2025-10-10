import os, sys, time, threading
from pycompilehell import engine, entity, camera

print("Iniciando engine...")
# Inicializar engine
if not engine.init("CompileHell Demo", 900, 600):
    raise SystemExit("Falha ao iniciar engine")
print("Engine iniciada.")

print("Criando player...")
# Cria player
player = entity.Entity("examples/assets/player.png", 100, 100, 64, 64)
wall = entity.Entity("examples/assets/player.png", 300, 500, 64, 64)
print("Player criado.")

camera_x= 0
camera_y= 0
class CameraControl:
    camera_x= 0
    camera_y= 0
    def on_update(self, e, dt):
        global camera_x
        camera_x = 0
        e.camx = camera_x
        e.camy = camera_y
        e.move(e.x+e.camx, e.y+e.camy)
# Script para controlar player via WASD
class PlayerControl:
    SC_W = 26
    SC_A = 4
    SC_S = 22
    SC_D = 7
    SC_SHOW_INFO = 56

    VEL = 200
    def __init__(self):
        None

    def on_update(self, e, dt):
        engine.update_fps()

        dx = 0
        dy = 0
        if e.is_key_down(self.SC_A) and not (e.would_collide(wall, -self.VEL * dt, e.y)):
            dx -= self.VEL * dt
            player.flip_h = True
        if e.is_key_down(self.SC_D) and not (e.would_collide(wall, self.VEL * dt, e.y)):
            dx += self.VEL * dt
            player.flip_h = False
        if e.is_key_down(self.SC_S) and not (e.would_collide(wall, e.x, self.VEL * dt)):
            dy += self.VEL * dt
        if e.is_key_down(self.SC_W) and not (e.would_collide(wall, e.x, -self.VEL * dt)):
            dy -= self.VEL * dt
        e.move(dx, dy)


player.add_script(PlayerControl())
player.add_script(CameraControl())

# Loop principal
last_time = time.time()
try:
    while engine.is_running():
        now = time.time()
        dt = now - last_time
        last_time = now

        engine.poll_events()
        engine.set_draw_color(30,30,30,255)
        engine.clear()
        player.update(dt)
        player.draw()
        wall.update(dt)
        wall.draw()
        engine.present()

finally:
    engine.shutdown()
