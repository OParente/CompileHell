// engine.hpp
#pragma once
#include <SDL2/SDL.h>
#include <string>

class Engine {
public:
    SDL_Window* window;
    SDL_Renderer* renderer;
    bool running;

    Engine() : window(nullptr), renderer(nullptr), running(false) {}

    bool init(const std::string& title, int width, int height) {
        if (SDL_Init(SDL_INIT_VIDEO) != 0) return false;
        window = SDL_CreateWindow(title.c_str(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, 0);
        if (!window) return false;
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
        if (!renderer) return false;
        running = true;
        return true;
    }

    void poll_events() {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) running = false;
        }
    }

    void set_draw_color(int r, int g, int b, int a) {
        SDL_SetRenderDrawColor(renderer, r, g, b, a);
    }

    void clear() {
        SDL_RenderClear(renderer);
    }

    void present() {
        SDL_RenderPresent(renderer);
    }

    void shutdown() {
        if (renderer) SDL_DestroyRenderer(renderer);
        if (window) SDL_DestroyWindow(window);
        SDL_Quit();
    }

    bool is_running() const { return running; }
};