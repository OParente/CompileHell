import os, sys, time, threading
from pycompilehell import engine, entity

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

# Script para controlar player via WASD
class PlayerControl:
    SC_W = 26
    SC_A = 4
    SC_S = 22
    SC_D = 7
    SC_SHOW_INFO = 56

    VEL = 200
    def __init__(self):
        self.vy = 0  # velocidade vertical

    def on_update(self, e, dt):
        engine.update_fps()

        GRAVITY = 800
        CHAO_Y = 500

        self.vy += GRAVITY * dt

        dx = 0
        if e.is_key_down(self.SC_A):
            if not e.would_collide_with(e.x- (self.VEL * dt * 0.01), e.y, wall):
                dx -= self.VEL * dt
            player.flip_h= True
        if e.is_key_down(self.SC_D):
            if not e.collides_with(wall):
                dx += self.VEL * dt
            else:
                dx -= self.VEL * dt
            player.flip_h= False
        
        if e.is_key_down(self.SC_SHOW_INFO):
            print(self.h)

        # Só pula se estiver no chão
        if e.is_key_down(self.SC_W) and e.y >= CHAO_Y:
            self.vy = -400

        dy = self.vy * dt

        e.move(dx, dy)

        # Simples chão
        if (e.y > CHAO_Y):
            e.y = CHAO_Y
            self.vy = 0

player.add_script(PlayerControl())

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
