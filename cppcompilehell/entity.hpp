// entity.hpp
#pragma once
#include <string>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

class Entity {
public:
    float x, y, w, h;
    SDL_Texture* texture;
    int flip_h, flip_v;

    Entity(SDL_Renderer* renderer, const std::string& texture_path, float x, float y, float w, float h, int flip_h = 0, int flip_v = 0)
        : x(x), y(y), w(w), h(h), texture(nullptr), flip_h(flip_h), flip_v(flip_v)
    {
        SDL_Surface* surf = IMG_Load(texture_path.c_str());
        if (surf) {
            texture = SDL_CreateTextureFromSurface(renderer, surf);
            SDL_FreeSurface(surf);
        }
    }

    ~Entity() {
        if (texture) SDL_DestroyTexture(texture);
    }

    void draw(SDL_Renderer* renderer) {
        if (!texture) return;
        SDL_Rect dst = { (int)x, (int)y, (int)w, (int)h };
        SDL_RendererFlip flip = SDL_FLIP_NONE;
        if (flip_h) flip = (SDL_RendererFlip)(flip | SDL_FLIP_HORIZONTAL);
        if (flip_v) flip = (SDL_RendererFlip)(flip | SDL_FLIP_VERTICAL);
        SDL_RenderCopyEx(renderer, texture, nullptr, &dst, 0, nullptr, flip);
    }

    void move(float dx, float dy) {
        x += dx;
        y += dy;
    }
};