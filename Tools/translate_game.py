# /// script
# dependencies = [
#   "deep-translator",
# ]
# ///
import os
import re
import json
import time
import shutil
try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

# Configurações do Jogo
import sys

if len(sys.argv) > 1:
    GAME_DIR = sys.argv[1]
else:
    GAME_DIR = r"C:\Program Files (x86)\GOG Galaxy\Games\Sid Meier's Alpha Centauri Planetary Pack"
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
os.makedirs(BUILD_DIR, exist_ok=True)

BACKUP_DIR = os.path.join(GAME_DIR, "backup_en")
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translation_cache.json")

# Dicionário de tradução estático para termos específicos que não devem ser traduzidos de forma literal ou que precisam ser mantidos
GLOSSARY = {
    "Formers": "Formadores",
    "Former": "Formador",
    "Sea Formers": "Formadores Marítimos",
    "Mind Worms": "Vermes Mentais",
    "Mind Worm": "Verme Mental",
    "Datalinks": "Datalinks",
    "Civilopedia": "Civilopedia",
    "Probe Team": "Equipe de Sonda",
    "Probe Teams": "Equipes de Sonda",
    "Planet Buster": "Destruidor de Planetas",
    "Planet Busters": "Destruidores de Planetas",
    "Xenofungus": "Xenofungus",
    "Fungus": "Fungus",
    "Recycling Tanks": "Tanques de Reciclagem",
    "Perimeter Defense": "Defesa Perimetral",
    "Tachyon Field": "Campo de Táquions",
    "Recreation Commons": "Área de Recreação",
    "Energy Bank": "Banco de Energia",
    "Network Node": "Nó de Rede",
    "Biology Lab": "Lab de Biologia",
    "Skunkworks": "Skunkworks",
    "Hologram Theatre": "Teatro de Hologramas",
    "Paradise Garden": "Jardim do Paraíso",
    "Tree Farm": "Fazenda de Árvores",
    "Hybrid Forest": "Floresta Híbrida",
    "Fusion Lab": "Lab de Fusão",
    "Quantum Lab": "Lab Quântico",
    "Research Hospital": "Hospital de Pesquisa",
    "Nanohospital": "Nanohospital",
    "Robotic Assembly Plant": "Fábrica de Montagem Robótica",
    "Nanoreplicator": "Nanoreplicador",
    "Quantum Converter": "Conversor Quântico",
    "Genejack Factory": "Fábrica Genejack",
    "Punishment Sphere": "Esfera de Punição",
    "Hab Complex": "Complexo Habitacional",
    "Habitation Dome": "Domo Habitacional",
    "Pressure Dome": "Domo de Pressão",
    "Command Center": "Centro de Comando",
    "Naval Yard": "Estaleiro Naval",
    "Aerospace Complex": "Complexo Aeroespacial",
    "Bioenhancement Center": "Centro de Bio-otimização",
    "Centauri Preserve": "Preserva de Centauri",
    "Temple of Planet": "Templo de Planeta",
    "Psi Gate": "Portal Psi",
    "Sky Hydroponics Lab": "Lab Hidropônico Celestial",
    "Nessus Mining Station": "Estação de Mineração Nessus",
    "Orbital Power Transmitter": "Transmissor de Energia Orbital",
    "Orbital Defense Pod": "Cápsula de Defesa Orbital",
    "Stockpile Energy": "Estocar Energia",
    "Ascent to Transcendence": "Ascensão à Transcendência"
}

# Inicializar Tradutor e Cache
if GoogleTranslator:
    translator = GoogleTranslator(source='en', target='pt')
else:
    translator = None

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)
    except Exception:
        translation_cache = {}
else:
    translation_cache = {}

def load_cache():
    global translation_cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                new_cache = json.load(f)
                translation_cache.clear()
                translation_cache.update(new_cache)
        except Exception:
            pass


def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

def backup_files(files):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Diretório de backup criado em: {BACKUP_DIR}")
    
    for f_name in files:
        src = os.path.join(GAME_DIR, f_name)
        dst = os.path.join(BACKUP_DIR, f_name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Backup realizado: {f_name}")

# Expressões Regulares para Proteção de Variáveis e Sintaxe
RE_LINK = re.compile(r"\$LINK<([^=>]+)=([0-9]+)>")
RE_BRACE = re.compile(r"\{([^\}]+)\}")
RE_VAR = re.compile(r"\$[A-Za-z0-9_]+")
RE_GENDER = re.compile(r"\$<[^>]+>")

def translate_string(text):
    if not text or text.strip() == "":
        return text
    
    # Extrai o espaçamento original para restaurá-lo depois
    leading_space = text[:len(text) - len(text.lstrip())]
    trailing_space = text[len(text.rstrip()):]
    stripped_text = text.strip()
    
    # 1. Verificar cache
    if stripped_text in translation_cache:
        return leading_space + translation_cache[stripped_text] + trailing_space
    
    # O restante do código opera sobre stripped_text
    original = stripped_text
    text = stripped_text
    
    # 2. Verificar glossário estático para traduções rápidas
    if text.strip() in GLOSSARY:
        val = text.replace(text.strip(), GLOSSARY[text.strip()])
        translation_cache[original] = val
        return val

    # 3. Proteger links $LINK<text=id>
    links = []
    def sub_link(match):
        label = match.group(1)
        link_id = match.group(2)
        placeholder = f"__LINK_{len(links)}__"
        links.append((label, link_id))
        return placeholder
    text_protected = RE_LINK.sub(sub_link, text)
    
    # 4. Proteger chaves {word}
    braces = []
    def sub_brace(match):
        content = match.group(1)
        placeholder = f"__BRACE_{len(braces)}__"
        braces.append(content)
        return placeholder
    text_protected = RE_BRACE.sub(sub_brace, text_protected)
    
    # 5. Proteger variáveis $VAR0
    vars_found = []
    def sub_var(match):
        var_str = match.group(0)
        placeholder = f"__VAR_{len(vars_found)}__"
        vars_found.append(var_str)
        return placeholder
    text_protected = RE_VAR.sub(sub_var, text_protected)

    # 5.1 Proteger sequencias de pluralidade/genero $<...>
    genders_found = []
    def sub_gender(match):
        gen_str = match.group(0)
        placeholder = f"__GEN_{len(genders_found)}__"
        genders_found.append(gen_str)
        return placeholder
    text_protected = RE_GENDER.sub(sub_gender, text_protected)
    
    # 6. Realizar a tradução da parte textual
    # Traduzir apenas se houver letras
    if any(c.isalpha() for c in text_protected):
        # Substituições de palavras no glossário na string protegida antes de enviar
        for key, val in GLOSSARY.items():
            # Fazer correspondência de palavras inteiras
            text_protected = re.sub(r'\b' + re.escape(key) + r'\b', val, text_protected, flags=re.IGNORECASE)
        
        retries = 3
        for attempt in range(retries):
            try:
                translated_part = translator.translate(text_protected)
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"Erro ao traduzir (tentativa {attempt+1}): '{text_protected}'. Erro: {e}")
                time.sleep(2)
        else:
            print(f"Falha definitiva ao traduzir: '{text_protected}'. Mantendo original.")
            translated_part = text_protected
    else:
        translated_part = text_protected
        
    # 7. Restaurar variáveis protegidas (na ordem inversa ou direta)
    for i, var_str in enumerate(vars_found):
        placeholder = f"__VAR_{i}__"
        # O tradutor pode alterar maiúsculas/minúsculas do placeholder, então usamos regex case-insensitive
        translated_part = re.sub(re.escape(placeholder), lambda m, v=var_str: v, translated_part, flags=re.IGNORECASE)

    for i, gen_str in enumerate(genders_found):
        placeholder = f"__GEN_{i}__"
        translated_part = re.sub(re.escape(placeholder), lambda m, v=gen_str: v, translated_part, flags=re.IGNORECASE)
        
    # 8. Restaurar chaves {word} (traduzindo o conteúdo da chave se necessário)
    for i, content in enumerate(braces):
        placeholder = f"__BRACE_{i}__"
        translated_content = translate_string(content)
        translated_part = re.sub(re.escape(placeholder), lambda m, v=f"{{{translated_content}}}": v, translated_part, flags=re.IGNORECASE)
        
    # 9. Restaurar links $LINK<text=id> (traduzindo o label do link)
    for i, (label, link_id) in enumerate(links):
        placeholder = f"__LINK_{i}__"
        translated_label = translate_string(label)
        translated_part = re.sub(re.escape(placeholder), lambda m, v=f"$LINK<{translated_label}={link_id}>": v, translated_part, flags=re.IGNORECASE)

    # 10. Correções estéticas comuns pós-tradução
    # Ex: o tradutor pode inserir espaços antes/depois de símbolos como ^ ou |
    translated_part = translated_part.replace(" ^ ", "^").replace("^ ", "^").replace(" ^", "^")
    translated_part = translated_part.replace(" | ", "|").replace("| ", "|").replace(" |", "|")
    
    translation_cache[original] = translated_part
    return leading_space + translated_part + trailing_space

def process_line_by_rules(line):
    # Trata atalhos com barra |
    if "|" in line:
        parts = line.split("|")
        # Traduz a primeira parte, mantém o atalho (segunda parte) intacto
        translated_parts = [translate_string(parts[0])] + parts[1:]
        return "|".join(translated_parts)
    
    # Trata quebras de linha com ^
    if "^" in line and len(line.strip()) > 1:
        # Mas não attributions como "^        -- "
        if line.startswith("^") and "--" in line:
            prefix = line[:line.find("--") + 2]
            rest = line[line.find("--") + 2:]
            return prefix + translate_string(rest)
        
        parts = line.split("^")
        translated_parts = [translate_string(p) for p in parts]
        return "^".join(translated_parts)
        
    return translate_string(line)

# Tradutores específicos para cada tipo de arquivo
def translate_labels_txt():
    src = os.path.join(BACKUP_DIR, "labels.txt")
    dst = os.path.join(BUILD_DIR, "labels.txt")
    
    print("\n--- Traduzindo labels.txt ---")
    with open(src, "r", encoding="cp1252", errors="ignore") as f:
        lines = f.readlines()
        
    out_lines = []
    is_labels_section = False
    labels_count = 0
    labels_processed = 0
    
    for i, line in enumerate(lines):
        clean = line.strip()
        
        # Manter comentários e cabeçalhos intactos
        if clean.startswith(";") or clean == "":
            out_lines.append(line)
            continue
            
        if clean == "#LABELS":
            is_labels_section = True
            out_lines.append(line)
            continue
            
        if is_labels_section and labels_count == 0:
            labels_count = int(clean)
            out_lines.append(line)
            continue
            
        if is_labels_section and labels_processed < labels_count:
            # Preserva a quebra de linha original (\n ou \r\n)
            ending = line[len(line.rstrip('\r\n')):]
            translated = process_line_by_rules(line.rstrip('\r\n'))
            out_lines.append(translated + ending)
            labels_processed += 1
            if labels_processed % 100 == 0:
                print(f"  Labels processados: {labels_processed}/{labels_count}")
                save_cache()
            continue
            
        out_lines.append(line)
        
    with open(dst, "w", encoding="cp1252", errors="ignore") as f:
        f.writelines(out_lines)
    print("labels.txt traduzido e salvo!")
    save_cache()

def translate_blurbs_txt(filename):
    src = os.path.join(BACKUP_DIR, filename)
    dst = os.path.join(BUILD_DIR, filename)
    
    print(f"\n--- Traduzindo {filename} ---")
    with open(src, "r", encoding="cp1252", errors="ignore") as f:
        lines = f.readlines()
        
    out_lines = []
    
    for i, line in enumerate(lines):
        clean = line.strip()
        
        # Manter comentários, cabeçalhos e marcadores estruturais intactos
        if clean.startswith(";") or clean.startswith("#") or clean == "":
            out_lines.append(line)
            continue
            
        ending = line[len(line.rstrip('\r\n')):]
        translated = process_line_by_rules(line.rstrip('\r\n'))
        out_lines.append(translated + ending)
        
        if i % 100 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            save_cache()
            
    with open(dst, "w", encoding="cp1252", errors="ignore") as f:
        f.writelines(out_lines)
    print(f"{filename} traduzido e salvo!")
    save_cache()

def translate_concepts_txt(filename):
    src = os.path.join(BACKUP_DIR, filename)
    dst = os.path.join(BUILD_DIR, filename)
    
    print(f"\n--- Traduzindo {filename} ---")
    with open(src, "r", encoding="cp1252", errors="ignore") as f:
        lines = f.readlines()
        
    out_lines = []
    current_section = ""
    
    for i, line in enumerate(lines):
        clean = line.strip()
        
        if clean.startswith(";"):
            out_lines.append(line)
            continue
            
        if clean.startswith("#"):
            current_section = clean
            out_lines.append(line)
            continue
            
        if clean == "":
            out_lines.append(line)
            continue
            
        ending = line[len(line.rstrip('\r\n')):]
        content = line.rstrip('\r\n')
        
        if current_section in ["#TITLES", "#ADVTITLES"]:
            translated = translate_string(content)
        else:
            translated = process_line_by_rules(content)
            
        out_lines.append(translated + ending)
        
        if i % 100 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            save_cache()
            
    with open(dst, "w", encoding="cp1252", errors="ignore") as f:
        f.writelines(out_lines)
    print(f"{filename} traduzido e salvo!")
    save_cache()

def translate_help_txt(filename):
    # Estrutura do help.txt e tutor.txt
    src = os.path.join(BACKUP_DIR, filename)
    dst = os.path.join(BUILD_DIR, filename)
    
    print(f"\n--- Traduzindo {filename} ---")
    with open(src, "r", encoding="cp1252", errors="ignore") as f:
        lines = f.readlines()
        
    out_lines = []
    
    for i, line in enumerate(lines):
        clean = line.strip()
        
        # Pular comentários técnicos
        if clean.startswith(";"):
            out_lines.append(line)
            continue
            
        # Pular marcadores de cabeçalho comuns, exceto #caption e #button
        if clean.startswith("#") and not (clean.startswith("#caption") or clean.startswith("#button")):
            out_lines.append(line)
            continue
            
        if clean == "":
            out_lines.append(line)
            continue
            
        ending = line[len(line.rstrip('\r\n')):]
        content = line.rstrip('\r\n')
        
        if content.startswith("#caption"):
            caption_text = content[8:].strip()
            translated = f"#caption {translate_string(caption_text)}"
        elif content.startswith("#button"):
            btn_text = content[7:].strip()
            translated = f"#button {translate_string(btn_text)}"
        else:
            translated = process_line_by_rules(content)
            
        out_lines.append(translated + ending)
        
        if i % 100 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            save_cache()
            
    with open(dst, "w", encoding="cp1252", errors="ignore") as f:
        f.writelines(out_lines)
    print(f"{filename} traduzido e salvo!")
    save_cache()

def translate_alpha_txt(filename):
    # Arquivo contendo dados tabulados importantes.
    # Vamos focar em traduzir os nomes e descrições das seções de texto.
    src = os.path.join(BACKUP_DIR, filename)
    dst = os.path.join(BUILD_DIR, filename)
    
    print(f"\n--- Traduzindo {filename} ---")
    with open(src, "r", encoding="cp1252", errors="ignore") as f:
        lines = f.readlines()
        
    out_lines = []
    current_section = ""
    
    for i, line in enumerate(lines):
        clean = line.strip()
        
        if clean.startswith(";"):
            out_lines.append(line)
            continue
            
        if clean.startswith("#"):
            current_section = clean
            out_lines.append(line)
            continue
            
        if clean == "":
            out_lines.append(line)
            continue
            
        ending = line[len(line.rstrip('\r\n')):]
        content = line.rstrip('\r\n')
        
        # Dividir a linha em campos usando a vírgula como delimitador
        # Mas preservando comentários após ponto e vírgula
        parts = content.split(";")
        data_part = parts[0]
        comment_part = ";".join(parts[1:]) if len(parts) > 1 else ""
        
        data_fields = [f.strip() for f in data_part.split(",")]
        
        # Traduzir dependendo da seção técnica
        # Nota: Só traduzimos os campos que contêm nomes legíveis, deixando IDs técnicos e números de pé.
        if current_section == "#TECHNOLOGY" and len(data_fields) > 0:
            data_fields[0] = translate_string(data_fields[0])
            
        # Removed #CHASSIS translation to avoid breaking internal engine references
                    
        elif current_section == "#DIFF" and len(data_fields) > 0:
            data_fields[0] = translate_string(data_fields[0])
            
        elif current_section == "#TERRAFORM" and len(data_fields) > 0:
            data_fields[0] = translate_string(data_fields[0])
            
        elif current_section == "#WEAPONS" and len(data_fields) > 1:
            data_fields[0] = translate_string(data_fields[0])
            
        elif current_section == "#DEFENSES" and len(data_fields) > 1:
            data_fields[0] = translate_string(data_fields[0])
            
        elif current_section == "#ABILITIES" and len(data_fields) > 5:
            data_fields[0] = translate_string(data_fields[0])
            data_fields[5] = translate_string(data_fields[5]) # Descrição breve
            
        elif current_section == "#MORALE" and len(data_fields) > 1:
            data_fields[0] = translate_string(data_fields[0])
            data_fields[1] = translate_string(data_fields[1])
            
        elif current_section in ["#DEFENSEMODES", "#OFFENSEMODES"] and len(data_fields) > 2:
            data_fields[0] = translate_string(data_fields[0])
            data_fields[1] = translate_string(data_fields[1])
            data_fields[2] = translate_string(data_fields[2])
            
        elif current_section == "#UNITS" and len(data_fields) > 0:
            data_fields[0] = translate_string(data_fields[0])
            
        elif current_section == "#FACILITIES" and len(data_fields) > 5:
            data_fields[0] = translate_string(data_fields[0])
            data_fields[5] = translate_string(data_fields[5]) # Descrição do efeito
            
        elif current_section in ["#ORDERS", "#COMPASS", "#PLANS", "#TRIAD", "#RESOURCES", "#ENERGY"] and len(data_fields) > 0:
            data_fields[0] = translate_string(data_fields[0])
                    
        elif current_section == "#CITIZENS" and len(data_fields) > 1:
            data_fields[0] = translate_string(data_fields[0])
            data_fields[1] = translate_string(data_fields[1])
            
        elif current_section == "#SOCIO" and len(data_fields) > 2:
            # Politics, Economics, etc.
            # E.g. Police State, ++POLICE, ++SUPPORT, --EFFIC
            data_fields[0] = translate_string(data_fields[0])
            if len(data_fields) > 2 and not data_fields[2].startswith("+") and not data_fields[2].startswith("-"):
                data_fields[2] = translate_string(data_fields[2])
                
        elif current_section in ["#SOCECONOMY", "#SOCEFFIC"] and len(data_fields) > 1:
            data_fields[1] = translate_string(data_fields[1])
            
        # Reconstruir a parte de dados (respeitando a formatação original básica)
        new_data_part = ", ".join(data_fields)
        if comment_part:
            new_line = new_data_part + " ; " + comment_part
        else:
            new_line = new_data_part
            
        out_lines.append(new_line + ending)
        
        if i % 100 == 0:
            print(f"  Linha {i}/{len(lines)} processada...")
            save_cache()
            
    with open(dst, "w", encoding="cp1252", errors="ignore") as f:
        f.writelines(out_lines)
    print(f"{filename} traduzido e salvo!")
    save_cache()

# Lista de todos os arquivos
TEXT_FILES = [
    "labels.txt",
    "blurbs.txt",
    "blurbsx.txt",
    "concepts.txt",
    "conceptsx.txt",
    "help.txt",
    "helpx.txt",
    "tutor.txt",
    "system.txt",
    "alpha.txt",
    "alphax.txt",
    "TECHLONGS.TXT",
    "TECHSHORTS.txt",
    "angels.txt",
    "drone.txt",
    "faction.txt",
    "gaians.txt",
    "hive.txt",
    "morgan.txt",
    "peace.txt",
    "pirates.txt",
    "script.txt",
    "spartans.txt",
    "univ.txt"
]

def main():
    load_cache()

    print("Iniciando tradutor automatizado de Alpha Centauri para PT-BR...\n")
    
    # 1. Backup
    backup_files(TEXT_FILES)
    
    # 2. Processar labels.txt (Interface)
    translate_labels_txt()
    
    # 3. Processar blurbs (Citações) e TECH files
    translate_blurbs_txt("blurbs.txt")
    translate_blurbs_txt("blurbsx.txt")
    translate_blurbs_txt("TECHLONGS.TXT")
    translate_blurbs_txt("TECHSHORTS.txt")
    
    # 4. Processar conceitos
    translate_concepts_txt("concepts.txt")
    translate_concepts_txt("conceptsx.txt")
    
    # 5. Processar ajuda e tutoriais
    translate_help_txt("help.txt")
    translate_help_txt("helpx.txt")
    translate_help_txt("tutor.txt")
    translate_help_txt("system.txt")
    
    # 6. Processar alpha.txt (Regras/Nomes)
    translate_alpha_txt("alpha.txt")
    translate_alpha_txt("alphax.txt")
    
    print("\nTradução concluída com sucesso!")
    save_cache()

if __name__ == "__main__":
    main()

