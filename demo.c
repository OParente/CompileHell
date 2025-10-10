#include "compilehell.h"
#include <stdio.h>
#include <time.h>

#define SC_W 26
#define SC_A 4
#define SC_S 22
#define SC_D 7
#define SC_SHOW_INFO 56

#define PLAYER_VEL 200
#define GRAVITY 1200
#define JUMP_FORCE -500
#define CHAO_Y 500

int main() {
    printf("Iniciando engine...\n");
    if (!compilehell_init("CompileHell Demo", 900, 600)) {
        printf("Falha ao iniciar engine\n");
        return 1;
    }
    printf("Engine iniciada.\n");

    printf("Criando player...\n");
    Entity* player = compilehell_create_entity("examples/assets/player.png", 100, 100, 64, 64);
    Entity* wall   = compilehell_create_entity("examples/assets/player.png", 300, 500, 64, 64);
    printf("Player criado.\n");

    float vy = 0.0f; // velocidade vertical

    double last_time = (double)clock() / CLOCKS_PER_SEC;

    while (compilehell_is_running()) {
        double now = (double)clock() / CLOCKS_PER_SEC;
        float dt = (float)(now - last_time);
        last_time = now;

        compilehell_poll_events();
        compilehell_update_fps();

        // aplica gravidade
        vy += GRAVITY * dt;

        float dx = 0;
        // movimento lateral
        if (compilehell_is_key_down(SC_A) && 
            !compilehell_would_collide(player, wall, -PLAYER_VEL * dt, -5)) {
            dx -= PLAYER_VEL * dt;
        }
        if (compilehell_is_key_down(SC_D) && 
            !compilehell_would_collide(player, wall, PLAYER_VEL * dt, -5)) {
            dx += PLAYER_VEL * dt;
        }

        // verificação simples se está no chão
        int no_chao = (player->y >= CHAO_Y) || compilehell_would_collide(player, wall, 0, +1);
        if (no_chao) {
            vy = 0;
        }

        // pulo
        if (compilehell_is_key_down(SC_W) && no_chao) {
            vy = JUMP_FORCE;
        }

        // aplica movimento vertical
        float dy = vy * dt;
        compilehell_move_entity(player, dx, dy);

        // trava no chão
        if (player->y >= CHAO_Y) {
            player->y = CHAO_Y;
            vy = 0;
        }

        // Renderização
        compilehell_set_draw_color(30, 30, 30, 255);
        compilehell_clear();
        compilehell_draw_entity(player);
        compilehell_draw_entity(wall);
        compilehell_present();
    }

    compilehell_destroy_entity(player);
    compilehell_destroy_entity(wall);
    compilehell_shutdown();
    return 0;
}
