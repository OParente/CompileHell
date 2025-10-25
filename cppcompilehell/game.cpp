#include "engine.hpp"
#include "entity.hpp"
#include "resource_lib.hpp"
#include <vector>
#include <string>
#include <iostream>

int main() {
    Engine engine;
    if (!engine.init("CompileHell C++ Game", 900, 600)) {
        std::cerr << "Failed to initialize engine\n";
        return 1;
    }

    // Load scene from .resxx
    auto scene = ResourceLib::load_resxx("scene.resxx");
    std::vector<Entity*> entities;

    for (const auto& [section, props] : scene) {
        std::string texture = props.count("texture") ? props.at("texture") : "";
        float x = props.count("x") ? std::stof(props.at("x")) : 0.0f;
        float y = props.count("y") ? std::stof(props.at("y")) : 0.0f;
        float w = props.count("w") ? std::stof(props.at("w")) : (props.count("size") ? std::stof(props.at("size")) : 64.0f);
        float h = props.count("h") ? std::stof(props.at("h")) : (props.count("size") ? std::stof(props.at("size")) : 64.0f);
        int flip_h = props.count("flip_h") ? (props.at("flip_h") == "True" ? 1 : 0) : 0;
        int flip_v = props.count("flip_v") ? (props.at("flip_v") == "True" ? 1 : 0) : 0;

        entities.push_back(new Entity(engine.renderer, texture, x, y, w, h, flip_h, flip_v));
    }

    // Main loop
    while (engine.is_running()) {
        engine.poll_events();
        engine.set_draw_color(30, 30, 30, 255);
        engine.clear();

        for (auto* ent : entities) {
            ent->draw(engine.renderer);
        }

        engine.present();
        SDL_Delay(16); // ~60 FPS
    }

    // Cleanup
    for (auto* ent : entities) delete ent;
    engine.shutdown();
    return 0;
}