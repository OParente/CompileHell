import customtkinter as ctk
import os
import subprocess
import re

PROJECTS_ROOT = "./projects"

def get_scene_id_from_file(scene_path):
    try:
        with open(scene_path, "r") as f:
            for line in f:
                if "scene_id" in line:
                    m = re.search(r'scene_id[=: ]+(\d+)', line)
                    if m:
                        return int(m.group(1))
        m = re.search(r'(\d+)\.resxx$', scene_path)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 0

class ProjectLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Launcher")
        self.geometry("420x400")
        self.project_path = ""
        self.scene_files = []

        ctk.CTkButton(self, text="Open Project", command=self.open_project).pack(pady=10)
        self.scene_list = ctk.CTkListbox(self, width=320, height=180)
        self.scene_list.pack(pady=10)
        ctk.CTkButton(self, text="Edit Scene", command=self.edit_scene).pack(pady=5)
        ctk.CTkButton(self, text="Play Game", command=self.play_game).pack(pady=5)

    def open_project(self):
        path = ctk.filedialog.askdirectory(initialdir=PROJECTS_ROOT, title="Select Project Folder")
        if not path:
            return
        self.project_path = path
        self.refresh_scene_list()

    def refresh_scene_list(self):
        self.scene_list.delete(0, "end")
        self.scene_files = []
        for fname in os.listdir(self.project_path):
            if fname.endswith(".resxx") or fname.endswith(".json"):
                self.scene_files.append(fname)
                self.scene_list.insert("end", fname)
        if self.scene_files:
            self.scene_list.select_set(0)

    def edit_scene(self):
        if not self.project_path or not self.scene_files:
            ctk.CTkMessagebox.show_error("No project or scene selected.")
            return
        idx = self.scene_list.curselection()
        if not idx:
            idx = (0,)
        scene_file = self.scene_files[idx[0]]
        scene_path = os.path.join(self.project_path, scene_file)
        subprocess.Popen(["python3", "object_builder.py", scene_path])

    def play_game(self):
        if not self.project_path or not self.scene_files:
            ctk.CTkMessagebox.show_error("No project or scene selected.")
            return
        idx = self.scene_list.curselection()
        if not idx:
            idx = (0,)
        scene_file = self.scene_files[idx[0]]
        scene_path = os.path.join(self.project_path, scene_file)
        scene_id = get_scene_id_from_file(scene_path)
        game_py = f"game.py{scene_id}"
        game_path = os.path.join(self.project_path, game_py)
        if not os.path.exists(game_path):
            ctk.CTkMessagebox.show_error(f"{game_py} not found in project.")
            return
        subprocess.Popen(["python3", game_path])

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ProjectLauncher()
    app.mainloop()