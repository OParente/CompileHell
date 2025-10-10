from pycompilehell.resource_lib import save_resxx, load_resxx

# Criar dados
scene_data = {
    "Object_Player": {
        "name": "Player",
        "x": "120",
        "y": "300",
        "flip_h": "false",
        "flip_v": "true",
        "texture": "assets/player.png"
    },
    "Engine_Info": {
        "version": "1.2.0",
        "author": "CompileHell"
    }
}

# Salvar .resxx
save_resxx("scene.resxx", scene_data)

# Carregar
data = load_resxx("scene.resxx")
print("Conteúdo decodificado:", data)
