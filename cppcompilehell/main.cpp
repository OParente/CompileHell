// main.cpp
#include "engine.hpp"
#include "entity.hpp"
#include <vector>
#include <chrono>
#include <thread>

int main() {
    Engine engine;
    if (!engine.init("CompileHell Demo", 900, 600)) {
        printf("Falha ao iniciar engine\n");
        return 1;
    }

    Entity player(engine.renderer, "examples/assets/player.png", 100, 100, 64, 64);

    while (engine.is_running()) {
        engine.poll_events();
        engine.set_draw_color(30, 30, 30, 255);
        engine.clear();

        player.draw(engine.renderer);

        engine.present();

        std::this_thread::sleep_for(std::chrono::milliseconds(16)); // ~60 FPS
    }

    engine.shutdown();
    return 0;
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            