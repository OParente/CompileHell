// main.cpp
#include <SDL2/SDL.h>
#include "imgui.h"
#include "imgui_impl_sdl.h"
#include "imgui_impl_sdlrenderer.h"
#include <vector>
#include <string>

struct Object {
    std::string name;
    float x, y, w, h;
    ImVec4 color;
};

int main(int, char**) {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* window = SDL_CreateWindow("Scene Editor", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1200, 700, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    ImGui_ImplSDL2_InitForSDLRenderer(window, renderer);
    ImGui_ImplSDLRenderer_Init(renderer);

    std::vector<Object> objects;
    int selected = -1;
    bool running = true;

    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            ImGui_ImplSDL2_ProcessEvent(&event);
            if (event.type == SDL_QUIT) running = false;
        }

        ImGui_ImplSDLRenderer_NewFrame();
        ImGui_ImplSDL2_NewFrame();
        ImGui::NewFrame();

        // --- Painel lateral ---
        ImGui::Begin("Painel Lateral", nullptr, ImGuiWindowFlags_AlwaysAutoResize);
        if (ImGui::Button("Novo Objeto")) {
            objects.push_back({"Novo", 100, 100, 64, 64, ImVec4(0.2f, 0.7f, 0.9f, 1.0f)});
        }
        if (ImGui::Button("Excluir Selecionado") && selected >= 0 && selected < (int)objects.size()) {
            objects.erase(objects.begin() + selected);
            selected = -1;
        }
        if (ImGui::Button("Salvar Cena")) {
            // Implemente a lógica de salvar
        }
        if (ImGui::Button("Abrir Cena")) {
            // Implemente a lógica de abrir
        }
        if (ImGui::Button("Play")) {
            // Implemente lógica de play
        }
        if (ImGui::Button("Stop")) {
            // Implemente lógica de stop
        }
        ImGui::End();

        // --- Propriedades do objeto selecionado ---
        if (selected >= 0 && selected < (int)objects.size()) {
            ImGui::Begin("Propriedades", nullptr, ImGuiWindowFlags_AlwaysAutoResize);
            Object& obj = objects[selected];
            ImGui::InputText("Nome", &obj.name);
            ImGui::DragFloat("X", &obj.x, 1.0f);
            ImGui::DragFloat("Y", &obj.y, 1.0f);
            ImGui::DragFloat("Largura", &obj.w, 1.0f, 1.0f, 500.0f);
            ImGui::DragFloat("Altura", &obj.h, 1.0f, 1.0f, 500.0f);
            ImGui::ColorEdit4("Cor", (float*)&obj.color);
            ImGui::End();
        }

        // --- Lista de objetos ---
        ImGui::Begin("Objetos", nullptr, ImGuiWindowFlags_AlwaysAutoResize);
        for (int i = 0; i < (int)objects.size(); ++i) {
            if (ImGui::Selectable(objects[i].name.c_str(), selected == i)) {
                selected = i;
            }
        }
        ImGui::End();

        // --- Renderização da cena ---
        SDL_SetRenderDrawColor(renderer, 30, 30, 30, 255);
        SDL_RenderClear(renderer);

        for (const auto& obj : objects) {
            SDL_Rect rect = { (int)obj.x, (int)obj.y, (int)obj.w, (int)obj.h };
            SDL_SetRenderDrawColor(renderer,
                (Uint8)(obj.color.x * 255),
                (Uint8)(obj.color.y * 255),
                (Uint8)(obj.color.z * 255),
                (Uint8)(obj.color.w * 255));
            SDL_RenderFillRect(renderer, &rect);
        }

        ImGui::Render();
        ImGui_ImplSDLRenderer_RenderDrawData(ImGui::GetDrawData());
        SDL_RenderPresent(renderer);
    }

    ImGui_ImplSDLRenderer_Shutdown();
    ImGui_ImplSDL2_Shutdown();
    ImGui::DestroyContext();
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}