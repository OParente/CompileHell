import json
import tkinter as tk
import os
import subprocess
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk
from pycompilehell.resource_lib import save_resxx, load_resxx

path= ""

class ObjectBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("CompileHell Object Builder v4")

        self.objects = []
        self.images = {}
        self.selected = None

        # --- Câmera ---
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.grid_size = 32

        # --- Arrastar objeto ---
        self.dragging_obj = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.playing = False

        self._build_ui()
        self._bind_controls()
        self.draw_scene()

    # -------------------------------------------------------
    def _build_ui(self):
        # --- Canvas principal ---
        self.canvas = tk.Canvas(self.root, bg="gray15", width=900, height=600)
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Painel lateral ---
        sidebar = ctk.CTkFrame(self.root, width=250)
        sidebar.pack(side="right", fill="y")

        ctk.CTkLabel(sidebar, text="Object Builder", font=("Arial", 14, "bold")).pack(pady=10)

        ctk.CTkButton(sidebar, text="Novo Objeto", command=self.add_object).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Propriedades", command=self.open_properties_window).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Salvar .resxx", command=self.save_resxx_file).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Abrir .resxx", command=self.load_resxx_file).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Salvar .json", command=self.save_json).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Abrir .json", command=self.load_json).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Excluir Selecionado", command=self.delete_selected).pack(fill="x", pady=4)
        ctk.CTkButton(sidebar, text="Limpar Cena", command=self.clear_scene).pack(fill="x", pady=4)

        # --- Zoom manual ---
        zoom_frame = ctk.CTkFrame(sidebar)
        zoom_frame.pack(pady=10)
        ctk.CTkButton(zoom_frame, text="-", width=4, command=lambda: self.change_zoom(0.9)).pack(side="left", padx=5)
        ctk.CTkButton(zoom_frame, text="=", width=4, command=lambda: self.change_zoom(1.1)).pack(side="right", padx=5)

        # --- Info ---
        self.coord_label = ctk.CTkLabel(sidebar, text="x: 0  y: 0")
        self.coord_label.pack(side="bottom", pady=5)
        ctk.CTkLabel(sidebar, text="Scroll = Zoom\nBotão do meio = Mover").pack(side="bottom", pady=5)

        # --- Botões Play/Stop ---
        btn_frame = ctk.CTkFrame(sidebar)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Play", command=self.start_play).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Stop", command=self.stop_play).pack(side="left", padx=5)

    # -------------------------------------------------------
    def _bind_controls(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("-", lambda e: self.change_zoom(0.9))
        self.root.bind("=", lambda e: self.change_zoom(1.1))

    # -------------------------------------------------------
    def world_to_screen(self, x, y):
        sx = (x + self.offset_x) * self.zoom
        sy = (y + self.offset_y) * self.zoom
        return sx, sy

    def screen_to_world(self, sx, sy):
        x = sx / self.zoom - self.offset_x
        y = sy / self.zoom - self.offset_y
        return x, y

    # -------------------------------------------------------
    def draw_grid(self):
        self.canvas.delete("grid")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        step = int(self.grid_size * self.zoom)
        for x in range(0, w, step):
            self.canvas.create_line(x, 0, x, h, fill="#2e2e2e", tags="grid")
        for y in range(0, h, step):
            self.canvas.create_line(0, y, w, y, fill="#2e2e2e", tags="grid")

    # -------------------------------------------------------
    def draw_scene(self):
        self.canvas.delete("all")
        self.draw_grid()
        for obj in self.objects:
            x, y = obj["x"], obj["y"]
            s = obj["size"] * self.zoom
            sx, sy = self.world_to_screen(x, y)
            tex = obj["texture"]
            scale_x = obj.get("scale_x", 1.0)
            scale_y = obj.get("scale_y", 1.0)

            draw_w = int(s * scale_x)
            draw_h = int(s * scale_y)

            if tex:
                if tex not in self.images:
                    try:
                        img = Image.open(tex).resize((draw_w, draw_h))
                        if obj["flip_h"]:
                            img = img.transpose(Image.FLIP_LEFT_RIGHT)
                        if obj["flip_v"]:
                            img = img.transpose(Image.FLIP_TOP_BOTTOM)
                        self.images[tex] = ImageTk.PhotoImage(img)
                    except Exception as e:
                        print(f"[Erro textura] {e}")
                        self.images[tex] = None

                image = self.images.get(tex)
                if image:
                    self.canvas.create_image(sx, sy, anchor="nw", image=image)
                else:
                    self.canvas.create_rectangle(sx, sy, sx + draw_w, sy + draw_h, fill=obj["color"])
            else:
                self.canvas.create_rectangle(sx, sy, sx + draw_w, sy + draw_h, fill=obj["color"])

            # Contorno do selecionado
            if obj == self.selected:
                self.canvas.create_rectangle(sx, sy, sx + draw_w, sy + draw_h, outline="yellow", width=2)

            # Nome
            self.canvas.create_text(sx + draw_w / 2, sy + draw_h / 2, text=obj["name"],
                                    fill="white", font=("Arial", int(10 * self.zoom), "bold"))

    # -------------------------------------------------------
    def add_object(self):
        name = simpledialog.askstring("Novo objeto", "Nome do objeto:")
        if not name:
            return

        color = colorchooser.askcolor()[1] or "#ffffff"
        obj = {
            "name": name,
            "x": 100,
            "y": 100,
            "size": 64,
            "color": color,
            "flip_h": False,
            "flip_v": False,
            "texture": "",
            "scale_x": 1.0,
            "scale_y": 1.0
        }
        self.objects.append(obj)
        self.selected = obj
        self.draw_scene()

    # -------------------------------------------------------
    def on_click(self, event):
        wx, wy = self.screen_to_world(event.x, event.y)
        for obj in self.objects:
            if obj["x"] <= wx <= obj["x"] + obj["size"] and obj["y"] <= wy <= obj["y"] + obj["size"]:
                self.selected = obj
                self.draw_scene()
                return
        self.selected = None
        self.draw_scene()

    def on_motion(self, event):
        wx, wy = self.screen_to_world(event.x, event.y)
        self.coord_label.config(text=f"x: {int(wx)}  y: {int(wy)}")

    # -------------------------------------------------------
    def start_pan(self, event):
        self.pan_start = (event.x, event.y)

    def do_pan(self, event):
        dx = (event.x - self.pan_start[0]) / self.zoom
        dy = (event.y - self.pan_start[1]) / self.zoom
        self.offset_x += dx
        self.offset_y += dy
        self.pan_start = (event.x, event.y)
        self.draw_scene()

    # -------------------------------------------------------
    def on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.change_zoom(factor)

    def change_zoom(self, factor):
        old_zoom = self.zoom
        self.zoom *= factor
        self.zoom = max(0.2, min(4.0, self.zoom))
        self.draw_scene()

    # -------------------------------------------------------
    def open_properties_window(self):
        if not self.selected:
            messagebox.showinfo("Aviso", "Selecione um objeto primeiro.")
            return

        obj = self.selected
        win = tk.Toplevel(self.root)
        win.title(f"Propriedades - {obj['name']}")
        win.geometry("300x380")
        win.resizable(False, False)

        def update_field(label, key, is_int=False):
            val = label.get()
            try:
                if key in ("scale_x", "scale_y"):
                    obj[key] = float(val)
                else:
                    obj[key] = int(val) if is_int else val
            except ValueError:
                pass
            self.draw_scene()

        # Entradas
        fields = {
            "x": tk.Entry(win), "y": tk.Entry(win),
            "size": tk.Entry(win), "color": tk.Entry(win),
            "texture": tk.Entry(win)
        }

        for i, (key, entry) in enumerate(fields.items()):
            tk.Label(win, text=key.upper()).pack()
            entry.insert(0, str(obj[key]))
            entry.pack(fill="x", padx=10, pady=3)
            entry.bind("<Return>", lambda e, k=key, ent=entry: update_field(ent, k, k in ("x", "y", "size")))

        # Flip buttons
        flip_frame = tk.Frame(win)
        flip_frame.pack(pady=10)
        tk.Label(flip_frame, text="Flip: ").pack(side="left")
        tk.Checkbutton(flip_frame, text="H", variable=tk.BooleanVar(value=obj["flip_h"]),
                       command=lambda: self.toggle_flip("flip_h")).pack(side="left", padx=5)
        tk.Checkbutton(flip_frame, text="V", variable=tk.BooleanVar(value=obj["flip_v"]),
                       command=lambda: self.toggle_flip("flip_v")).pack(side="left", padx=5)

        # Botão cor
        tk.Button(win, text="Escolher Cor", command=lambda: self.pick_color(obj)).pack(pady=5)
        tk.Button(win, text="Selecionar Textura", command=lambda: self.pick_texture(obj, fields["texture"])).pack(pady=5)
        tk.Button(win, text="Aplicar", command=lambda: self.draw_scene()).pack(pady=10)

    # -------------------------------------------------------
    def pick_color(self, obj):
        c = colorchooser.askcolor()[1]
        if c:
            obj["color"] = c
            self.draw_scene()

    def pick_texture(self, obj, field):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if path:
            obj["texture"] = path
            field.delete(0, "end")
            field.insert(0, path)
            self.draw_scene()

    def toggle_flip(self, axis):
        if self.selected:
            self.selected[axis] = not self.selected[axis]
            self.draw_scene()

    # -------------------------------------------------------
    def delete_selected(self):
        if not self.selected:
            return
        self.objects.remove(self.selected)
        self.selected = None
        self.draw_scene()

    def clear_scene(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar toda a cena?"):
            self.objects.clear()
            self.selected = None
            self.draw_scene()

    # -------------------------------------------------------
    def save_resxx_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".resxx", filetypes=[("Resource File", "*.resxx")])
        if not path:
            return
        # Pegue o id da cena do nome do arquivo (ex: scene1.resxx → id=1)
        import re
        m = re.search(r'(\d+)\.resxx$', path)
        scene_id = int(m.group(1)) if m else 0
        data = {f"Object_{i}_{o['name']}": {k: str(v) for k, v in o.items()} for i, o in enumerate(self.objects)}
        data["SceneInfo"] = {"scene_id": str(scene_id)}
        save_resxx(path, data)
        messagebox.showinfo("Salvo", f"Arquivo salvo em {path}")

    def load_resxx_file(self):
        path = filedialog.askopenfilename(filetypes=[("Resource File", "*.resxx")])
        if not path:
            return
        data = load_resxx(path)
        self.objects.clear()
        self.scene_id = 0
        for section, props in data.items():
            if section == "SceneInfo":
                self.scene_id = int(props.get("scene_id", 0))
                continue
            obj = {
                "name": props.get("name", section),
                "x": int(props.get("x", 0)),
                "y": int(props.get("y", 0)),
                "size": int(props.get("size", 64)),
                "color": props.get("color", "#ffffff"),
                "flip_h": props.get("flip_h", "False") == "True",
                "flip_v": props.get("flip_v", "False") == "True",
                "texture": props.get("texture", ""),
                "scale_x": float(props.get("scale_x", 1.0)),
                "scale_y": float(props.get("scale_y", 1.0))
            }
            self.objects.append(obj)
        self.draw_scene()
        messagebox.showinfo("Carregado", f"{path} carregado com sucesso.")

    # -------------------------------------------------------
    def save_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w") as f:
            json.dump(self.objects, f, indent=4)
        messagebox.showinfo("Salvo", f"JSON salvo em {path}")

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path) as f:
            self.objects = json.load(f)
        self.draw_scene()
        messagebox.showinfo("Carregado", f"JSON carregado de {path}")

    def start_drag(self, event):
        wx, wy = self.screen_to_world(event.x, event.y)
        for obj in reversed(self.objects):  # Prioriza objetos desenhados por cima
            s = obj["size"] * obj.get("scale_x", 1.0)
            if obj["x"] <= wx <= obj["x"] + s and obj["y"] <= wy <= obj["y"] + s:
                self.selected = obj
                self.dragging_obj = obj
                self.drag_offset_x = wx - obj["x"]
                self.drag_offset_y = wy - obj["y"]
                self.draw_scene()
                return
        self.selected = None
        self.dragging_obj = None
        self.draw_scene()

    def do_drag(self, event):
        if self.dragging_obj and not self.playing:
            wx, wy = event.x, event.y
            self.dragging_obj["x"] = int(wx - self.drag_offset_x)
            self.dragging_obj["y"] = int(wy - self.drag_offset_y)
            self.draw_scene()

    def stop_drag(self, event):
        self.dragging_obj = None

    def start_play(self):
        self.playing = True
        # Use o id da cena para escolher o game.py
        game_path = f"game.py{self.scene_id}"
        if not os.path.exists(game_path):
            messagebox.showerror("Erro", f"{game_path} não encontrado.")
            return
        subprocess.Popen(["python3", game_path])

    def stop_play(self):
        self.playing = False

    def play_loop(self):
        game_path= f"{path}.py"#gets the scene python
        if not self.playing:
            return
        subprocess.Popen(["python3", game_path])

# -------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectBuilder(root)
    root.mainloop()
