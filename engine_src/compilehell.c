#include "compilehell.h"
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdlib.h>
#include <string.h>
#include <SDL2/SDL_ttf.h>

#define COMPILEHELL_DEBUG 1

static SDL_Window* gWindow = NULL;
static SDL_Renderer* gRenderer = NULL;
static int gRunning = 0;

// Array de teclas
#define KEY_COUNT 512
static int gKeys[KEY_COUNT];

// ------------------------
// Inicialização
// ------------------------
int compilehell_init(const char* title, int w, int h) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) return 0;
    if (!(IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG)) return 0;

    gWindow = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, w, h, 0);
    if (!gWindow) return 0;

    gRenderer = SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!gRenderer) return 0;

    memset(gKeys, 0, sizeof(gKeys));
    gRunning = 1;
    return 1;
}

void compilehell_set_fullscreen(int enable) {
    if (gWindow) {
        if (enable) {
            SDL_SetWindowFullscreen(gWindow, SDL_WINDOW_FULLSCREEN_DESKTOP);
        } else {
            SDL_SetWindowFullscreen(gWindow, 0);
        }
    }
}

// ------------------------
// Loop rodando
// ------------------------
int compilehell_is_running() {
    return gRunning;
}

// Poll events
void compilehell_poll_events() {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {

        if (e.type == SDL_QUIT) gRunning = 0;

        if (e.type == SDL_KEYDOWN && e.key.keysym.scancode < KEY_COUNT)
            gKeys[e.key.keysym.scancode] = 1;
        if (e.type == SDL_KEYUP && e.key.keysym.scancode < KEY_COUNT)
            gKeys[e.key.keysym.scancode] = 0;
    }
}

// Verifica se uma tecla está pressionada
int compilehell_is_key_down(int scancode) {
    if (scancode < 0 || scancode >= KEY_COUNT) return 0;
    return gKeys[scancode];
}

// ------------------------
// Limpeza
// ------------------------
void compilehell_shutdown() {
    SDL_DestroyRenderer(gRenderer);
    SDL_DestroyWindow(gWindow);
    IMG_Quit();
    SDL_Quit();
}

// ------------------------
// Renderização
// ------------------------
void compilehell_set_draw_color(int r, int g, int b, int a) {
    SDL_SetRenderDrawColor(gRenderer, r, g, b, a);
}

void compilehell_clear() {
    SDL_RenderClear(gRenderer);
}

void compilehell_present() {
    SDL_RenderPresent(gRenderer);
}

// ------------------------
// Entidades
// ------------------------
Entity* compilehell_create_entity(const char* path, float x, float y, float w, float h, float camx, float camy) {
    printf("Tentando criar entidade com textura: %s\n", path);
    Entity* e = (Entity*)malloc(sizeof(Entity));
    if (!e) {
        printf("Falha ao alocar entidade!\n");
        return NULL;
    }
    e->x = x; e->y = y; e->w = w; e->h = h;

    SDL_Surface* surf = IMG_Load(path);
    if (!surf) {
        printf("Falha ao carregar textura: %s\n", path);
        free(e);
        return NULL;
    }

    e->texture = SDL_CreateTextureFromSurface(gRenderer, surf);
    SDL_FreeSurface(surf);

    if (!e->texture) {
        printf("Falha ao criar textura SDL: %s\n", path);
        free(e);
        return NULL;
    }
    printf("Entidade criada com sucesso!\n");
    return e;
}

void compilehell_draw_entity(Entity* e) {
    if (!e || !e->texture) {
        printf("Entidade ou textura nula!\n");
        return;
    }
    SDL_Rect dst = { (int)e->x, (int)e->y, (int)e->w, (int)e->h };
    SDL_RenderCopy(gRenderer, e->texture, NULL, &dst);
}

// Move a entidade manualmente
void compilehell_move_entity(Entity* e, float dx, float dy) {
    if (!e) return;
    e->x += dx;
    e->y += dy;
}

/**
 * Destroi uma entidade e libera recursos.
 */
void compilehell_destroy_entity(Entity* e) {
    if (!e) return;
    if (e->texture) SDL_DestroyTexture(e->texture);
    free(e);
}

int compilehell_check_collision(Entity* a, Entity* b) {
    if (!a || !b) return 0;
    return !(a->x + a->w < b->x || a->x > b->x + b->w ||
             a->y + a->h < b->y || a->y > b->y + b->h);
}

/// Checa colisão futura entre duas entidades (considerando movimento dx, dy de 'a')
int compilehell_would_collide(Entity* a, Entity* b, float dx, float dy) {
    if (!a || !b) return 0;

    float ax = a->x + dx;
    float ay = a->y + dy;

    return !(ax + a->w < b->x || ax > b->x + b->w ||
             ay + a->h < b->y || ay > b->y + b->h);
}

void compilehell_get_mouse(int* x, int* y) {
    int mx, my;
    SDL_GetMouseState(&mx, &my);
    if (x) *x = mx;
    if (y) *y = my;
}

int compilehell_is_mouse_down(int button) {
    return (SDL_GetMouseState(NULL, NULL) & SDL_BUTTON(button)) != 0;
}

#if COMPILEHELL_DEBUG
static Uint32 lastFPSTime = 0;
static int frameCount = 0;
static float currentFPS = 0.0f;

void compilehell_update_fps() {
    frameCount++;
    Uint32 now = SDL_GetTicks();
    if (now - lastFPSTime >= 1000) {
        currentFPS = frameCount * 1000.0f / (now - lastFPSTime);
        frameCount = 0;
        lastFPSTime = now;

        char title[128];
        snprintf(title, sizeof(title), "CompileHell [FPS: %.1f]", currentFPS);
        SDL_SetWindowTitle(gWindow, title);
    }
}
#endif