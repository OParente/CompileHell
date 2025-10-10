#ifndef COMPILEHELL_H
#define COMPILEHELL_H

/**
 * Biblioteca CompileHell - Engine 2D mínima em C
 * ------------------------------------------------
 * Responsável por inicialização da janela, renderização de sprites
 * e manipulação básica de entidades. A lógica de jogo é controlada
 * dinamicamente via scripts Python.
 */
typedef struct CompileHell_Entity {
    float x, y, w, h, camx, camy;
    void* texture;
    int flip_h;
    int flip_v;
} Entity;

/**
 * Inicializa a engine.
 * @param title Título da janela
 * @param w     Largura
 * @param h     Altura
 * @return 1 em caso de sucesso, 0 em erro
 */
int compilehell_init(const char *title, int w, int h);

/**
 * Finaliza a engine e libera memória/recursos.
 */
void compilehell_shutdown();

/**
 * Verifica se a janela ainda está ativa.
 * @return 1 se rodando, 0 se o usuário fechou
 */
int compilehell_is_running();

/**
 * Processa eventos (teclado, fechar janela etc).
 */
void compilehell_poll_events();

/**
 * Define a cor de fundo/draw.
 */
void compilehell_set_draw_color(int r, int g, int b, int a);

/**
 * Limpa a tela para desenhar novamente.
 */
void compilehell_clear();

/**
 * Apresenta o frame atual na janela.
 */
void compilehell_present();

/**
 * Desenha um retângulo preenchido.
 */
void compilehell_fill_rect(int x, int y, int w, int h);

/**
 * Cria uma entidade com sprite.
 */
Entity* compilehell_create_entity(const char *texture_path, float x, float y, float w, float h, float camx, float camy);

/**
 * Desenha entidade.
 */
void compilehell_draw_entity(Entity* e);

/**
 * Destroi uma entidade e libera recursos.
 */
void compilehell_destroy_entity(Entity* e);

/**
 * Verifica colisão entre duas entidades.
 * @param a Entidade 1
 * @param b Entidade 2
 * @return 1 se colidindo, 0 caso contrário
 */
int compilehell_check_collision(Entity* a, Entity* b);

int compilehell_would_collide(Entity* a, Entity* b, float dx, float dy);
/*
 * Obtém a posição atual do mouse.
 * @param x Ponteiro para coordenada X
 * @param y Ponteiro para coordenada Y
 */
void compilehell_get_mouse(int* x, int* y);

/**
 * Verifica se um botão do mouse está pressionado.
 * @param button O botão do mouse (1 = esquerdo, 2 = direito, etc.)
 * @return 1 se pressionado, 0 caso contrário
 */
int compilehell_is_mouse_down(int button);

/**
 * Atualiza a taxa de quadros por segundo (FPS).
 */
void compilehell_update_fps();

void compilehell_move_entity(Entity* e, float dx, float dy);

#endif
