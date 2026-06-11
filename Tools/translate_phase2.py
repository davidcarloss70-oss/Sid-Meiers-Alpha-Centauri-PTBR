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

BACKUP_DIR = os.path.join(GAME_DIR, "backup_en")
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translation_cache.json")

# Factions to translate
FACTION_FILES = [
    "GAIANS.TXT", "HIVE.TXT", "MORGAN.TXT", "SPARTANS.TXT", "BELIEVE.TXT", "PEACE.TXT", "UNIV.TXT",
    "cyborg.txt", "drone.txt", "angels.txt", "fungboy.txt", "caretake.txt", "usurper.txt", "pirates.txt",
    "FACTION.TXT"
]

SCRIPT_FILES = ["Script.txt", "xscript.txt", "Interlude.txt", "interludea.txt", "interludex.txt"]
MENU_FILES = ["menu.txt"]

# Carregar cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        translation_cache = json.load(f)
else:
    translation_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

def backup_file(filename):
    src = os.path.join(GAME_DIR, filename)
    dst = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)

def translate_string(text):
    text = text.strip()
    if not text:
        return text
        
    if text in translation_cache:
        return translation_cache[text]
        
    # Translate only if there are letters
    if not any(c.isalpha() for c in text):
        return text

    # Handle {} links by replacing them with placeholders
    links = re.findall(r"\{\$[\w\s]+\}|\{[A-Z_]+\}", text)
    temp_text = text
    for i, link in enumerate(links):
        temp_text = temp_text.replace(link, f"__LINK{i}__")

    # Retry loop
    max_retries = 3
    for attempt in range(max_retries):
        try:
            translated = GoogleTranslator(source='en', target='pt').translate(temp_text)
            
            # Clean up smart quotes and dashes for cp1252
            translated = translated.replace("“", '"').replace("”", '"').replace("—", "-").replace("‘", "'").replace("’", "'").replace("…", "...")
            
            # Restore links
            for i, link in enumerate(links):
                translated = translated.replace(f"__LINK{i}__", link)
                
            translation_cache[text] = translated
            save_cache()
            time.sleep(1) # delay to avoid rate limit
            return translated
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error translating '{text}': {e}")
                return text
            time.sleep(2)

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

    with open(dst_path, "w", encoding="cp1252", errors="replace") as f:
        f.writelines(lines)

def main():
    global translation_cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)

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

