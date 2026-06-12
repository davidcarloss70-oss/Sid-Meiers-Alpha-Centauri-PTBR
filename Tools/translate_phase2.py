import os
import re
import json
import time
import shutil
import sys
try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

if len(sys.argv) > 1:
    GAME_DIR = sys.argv[1]
else:
    GAME_DIR = r"C:\Program Files (x86)\GOG Galaxy\Games\Sid Meier's Alpha Centauri Planetary Pack"
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
os.makedirs(BUILD_DIR, exist_ok=True)

BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup_test")
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translation_cache.json")

# Factions to translate
FACTION_FILES = [
    "GAIANS.TXT", "HIVE.TXT", "MORGAN.TXT", "SPARTANS.TXT", "BELIEVE.TXT", "PEACE.TXT", "UNIV.TXT",
    "cyborg.txt", "drone.txt", "angels.txt", "fungboy.txt", "caretake.txt", "usurper.txt", "pirates.txt",
    "FACTION.TXT"
]

SCRIPT_FILES = ["Script.txt", "xscript.txt", "Interlude.txt", "interludea.txt", "interludex.txt"]
MENU_FILES = ["menu.txt"]

import translate_game

# Use o cache do translate_game
translation_cache = translate_game.translation_cache

def save_cache():
    translate_game.save_cache()

def backup_file(filename):
    src = os.path.join(GAME_DIR, filename)
    dst = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)

def translate_string(text):
    return translate_game.translate_string(text)

def patch_ini():
    print("Patching Alpha Centauri.ini...")
    ini_path = os.path.join(GAME_DIR, "Alpha Centauri.ini")
    if not os.path.exists(ini_path):
        return
        
    with open(ini_path, "r", encoding="cp1252") as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        if lines[i].strip() == "DirectDraw=1":
            lines[i] = "DirectDraw=0\n"
        elif lines[i].strip() == "DisableOpeningMovie=0":
            lines[i] = "DisableOpeningMovie=1\n"
            
    with open(ini_path, "w", encoding="cp1252") as f:
        f.writelines(lines)

def process_menu(filename):
    print(f"Processing {filename}...")
    backup_file(filename)
    src_path = os.path.join(BACKUP_DIR, filename)
    dst_path = os.path.join(BUILD_DIR, filename)
    if not os.path.exists(src_path):
        return
        
    with open(src_path, "r", encoding="cp1252") as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(";") or line.startswith("#") or not line.strip():
            continue
            
        # Menu lines can have shortcuts like "&Game" or "Switch To Detailed &Menus|F11"
        parts = line.split("|")
        text_part = parts[0]
        
        # Need to protect the "&" character which indicates keyboard shortcut
        has_ampersand = "&" in text_part
        if has_ampersand:
            clean_text = text_part.replace("&", "")
            translated = translate_string(clean_text)
            # Re-insert & at the beginning (simplest approach for hotkeys)
            translated = "&" + translated
        else:
            translated = translate_string(text_part)
            
        if len(parts) > 1:
            lines[i] = translated + "|" + "|".join(parts[1:])
        else:
            if line.endswith("\n"):
                lines[i] = translated + "\n"
            else:
                lines[i] = translated
                
    with open(dst_path, "w", encoding="cp1252", errors="replace") as f:
        f.writelines(lines)

def process_script(filename):
    print(f"Processing {filename}...")
    backup_file(filename)
    src_path = os.path.join(BACKUP_DIR, filename)
    dst_path = os.path.join(BUILD_DIR, filename)
    if not os.path.exists(src_path):
        return
        
    with open(src_path, "r", encoding="cp1252") as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            continue
            
        if stripped.startswith("#caption "):
            caption_text = stripped[9:]
            translated = translate_string(caption_text)
            lines[i] = "#caption " + translated + "\n"
            continue
            
        if stripped.startswith("#"):
            continue
            
        # Normal text line
        translated = translate_string(stripped)
        lines[i] = translated + "\n"
        
        if i % 100 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            translate_game.save_cache()
        
    with open(dst_path, "w", encoding="cp1252", errors="replace") as f:
        f.writelines(lines)

def process_faction(filename):
    print(f"Processing {filename}...")
    backup_file(filename)
    src_path = os.path.join(BACKUP_DIR, filename)
    dst_path = os.path.join(BUILD_DIR, filename)
    if not os.path.exists(src_path):
        return
        
    with open(src_path, "r", encoding="cp1252") as f:
        lines = f.readlines()
        
    translate_mode = False
    for i in range(len(lines)):
        line = lines[i]
        stripped = line.strip()
        
        # We only translate lines inside specific text blocks
        if stripped.startswith("#BLURB") or stripped.startswith("#DATALINKS") or stripped.startswith("#INTERLUDE"):
            translate_mode = True
            continue
        elif stripped.startswith("#") and not stripped.startswith("#caption"):
            # A new section like #BASES, stop translating
            translate_mode = False
            continue
            
        if translate_mode and stripped and not stripped.startswith(";"):
            # Alpha Centauri dialog lines often start with ^
            if stripped.startswith("^"):
                text_to_translate = stripped[1:].strip()
                if text_to_translate:
                    translated = translate_string(text_to_translate)
                    # preserve indentation
                    prefix = line[:line.find("^")+1]
                    lines[i] = prefix + translated + "\n"
            else:
                translated = translate_string(stripped)
                lines[i] = translated + "\n"
                
        if i % 50 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            translate_game.save_cache()

    with open(dst_path, "w", encoding="cp1252", errors="replace") as f:
        f.writelines(lines)

def main():
    print("Patching Alpha Centauri.ini...")
    
    for f in MENU_FILES:
        process_menu(f)
        
    for f in SCRIPT_FILES:
        process_script(f)
        
    for f in FACTION_FILES:
        process_faction(f)
        
    save_cache()
    print("Fase 2 concluída!")

if __name__ == "__main__":
    main()

