from pycompilehell.resource_lib import *
from pycompilehell import entity

def get_scene(scene_name: str):
        path = f"{scene_name}.resxx"
        if not path:
            return
        data = load_resxx(path)
        objects= []
        for section, props in data.items():
            obj = {
                "texture": props.get("texture", ""),

                "name": props.get("name", section),

                "x": int(props.get("x", 0)),
                "y": int(props.get("y", 0)),

                "scale_x": float(props.get("scale_x", 1.0)),
                "scale_y": float(props.get("scale_y", 1.0)),

                "size": int(props.get("size", 64)),

                "color": props.get("color", "#ffffff"),

                "flip_h": props.get("flip_h", "False") == "True",
                "flip_v": props.get("flip_v", "False") == "True"

            }
            entityn = {
                obj['name']: entity.Entity(
                    obj['texture'],
                    obj['x'],
                    obj['y'],
                    obj['size'] * obj['scale_x'],  # w
                    obj['size'] * obj['scale_y'],  # h
                    obj['scale_x'],
                    obj['scale_y']
                )
            }
            if not obj['name']== 'Engine_Info': objects.append(entityn)
        return objects

print(get_scene("scene"))
# Example usage:
# scene_entities = get_scene("scene")