import os
import subprocess
import shutil

# Paths
script_path = "app.py"
icon_path = "" # Optional
exe_name = "Alpha_Centauri_Tradutor_UI"

cmd = [
    "uv", "run", "pyinstaller",
    "--noconfirm",
    "--windowed",
    "--onefile", "--noupx",
    "--name", exe_name,
    "--hidden-import", "deep_translator",
    "--hidden-import", "translate_phase2",
    "--hidden-import", "translate_game",
    "--add-data", "translate_game.py;.",
    "--add-data", "translate_phase2.py;.",
    "--add-data", "translation_cache.json;.",
    "--add-data", "translation_cache.backup.json;.",
    script_path
]

print("Running PyInstaller...")
subprocess.run(cmd, check=True)

# Copy the executable to the Tools directory instead of keeping it buried in dist
exe_path = os.path.join("dist", f"{exe_name}.exe")
if os.path.exists(exe_path):
    shutil.copy2(exe_path, f"{exe_name}.exe")
    print(f"Build complete! Executable is at: {exe_name}.exe")
else:
    print("Build failed.")

