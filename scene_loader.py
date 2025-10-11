from pycompilehell.resource_lib import *
from pycompilehell import entity

def get_scene(scene_name: str):
    raw_info = load_resxx(f"{scene_name}.resxx")
    obj_list = []
    for obj_str in raw_info:
        print(obj_str)
        # Tente converter a string para dict
        # Exemplo: se for JSON
        import json
        obj = json.loads(obj_str)
        ent = entity.Entity(
            obj['texture'],
            float(obj['x']),
            float(obj['y']),
            float(obj.get('w', 64)),
            float(obj.get('h', 64))
        )
        obj_list.append(ent)
        print(obj_list)
    return obj_list

get_scene("scene")
# Example usage:
# scene_entities = get_scene("scene")