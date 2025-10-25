import os, sys, time, threading
from pycompilehell import engine, entity

print("Iniciando engine...")
# Inicializar engine
if not engine.init("CompileHell Demo", 900, 600):
    raise SystemExit("Falha ao iniciar engine")
print("Engine iniciada.")

print("Criando player...")
# Cria player
player = entity.Entity("examples/assets/player.png", 100, 100, 64, 64, False, False)
wall = entity.Entity("examples/assets/player.png", 300, 500, 64, 64, False, False)
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

        GRAVITY = 1200   # gravidade mais forte para cair rápido
        JUMP_FORCE = -500  # força fixa do pulo
        CHAO_Y = 500

        # aplica gravidade
        self.vy += GRAVITY * dt  

        dx = 0
        if e.is_key_down(self.SC_A) and not (e.would_collide(wall, -self.VEL * dt, -5)):
            dx -= self.VEL * dt
            player.flip_h = True
        if e.is_key_down(self.SC_D) and not (e.would_collide(wall, self.VEL * dt, -5)):
            dx += self.VEL * dt
            player.flip_h = False

        # verificação simples se está no chão
        no_chao = bool((e.y >= CHAO_Y) + (e.would_collide(wall, 0, +1)))
        if no_chao:
            self.vy = 0
        # só pula se estiver no chão
        if e.is_key_down(self.SC_W) and no_chao:
            self.vy = JUMP_FORCE  

        # aplica movimento vertical
        dy = self.vy * dt

        e.move(dx, dy)

        # trava no chão
        if e.y >= CHAO_Y:
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
