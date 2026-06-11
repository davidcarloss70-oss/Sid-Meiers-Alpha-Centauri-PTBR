import os
import sys
import json
import zipfile
import threading
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Configurations
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Get paths
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.dirname(BASE_DIR)

DEFAULT_GAME_DIR = r"C:\Program Files (x86)\GOG Galaxy\Games\Sid Meier's Alpha Centauri Planetary Pack"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alpha Centauri PT-BR - Ferramenta de Tradução")
        self.geometry("900x650")
        
        self.game_dir = tk.StringVar(value=DEFAULT_GAME_DIR)
        
        # UI Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.log_messages = []
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Alpha Centauri PT-BR", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.dir_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.dir_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10,0))
        self.dir_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.dir_frame, text="Local do Jogo:").grid(row=0, column=0, padx=(0,10))
        self.dir_entry = ctk.CTkEntry(self.dir_frame, textvariable=self.game_dir)
        self.dir_entry.grid(row=0, column=1, sticky="ew", padx=(0,10))
        self.dir_btn = ctk.CTkButton(self.dir_frame, text="Procurar...", width=100, command=self.browse_dir)
        self.dir_btn.grid(row=0, column=2)
        
        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        self.tab_install = self.tabview.add("Instalação & Jogo")
        self.tab_ini = self.tabview.add("Correção Tela Preta (.ini)")
        self.tab_cache = self.tabview.add("Editor de Textos (Avançado)")
        self.tab_logs = self.tabview.add("Logs")
        
        self.setup_install_tab()
        self.setup_ini_tab()
        self.setup_cache_tab()
        self.setup_logs_tab()

    def browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.game_dir.get(), title="Selecione a pasta do Alpha Centauri")
        if d:
            self.game_dir.set(d)

    def log(self, message):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}"
        self.log_messages.append(full_msg)
        if hasattr(self, 'log_textbox') and self.log_textbox.winfo_exists():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", full_msg + "\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")

    def setup_logs_tab(self):
        self.tab_logs.grid_columnconfigure(0, weight=1)
        self.tab_logs.grid_rowconfigure(0, weight=1)
        
        self.log_textbox = ctk.CTkTextbox(self.tab_logs, font=("Consolas", 12))
        self.log_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.log_textbox.configure(state="disabled")

    def setup_install_tab(self):
        self.tab_install.grid_columnconfigure(0, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_install, text="Bem-vindo ao Patch PT-BR de Alpha Centauri!", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.grid(row=0, column=0, pady=(30, 10))
        
        desc = ctk.CTkLabel(self.tab_install, text="Certifique-se de que o 'Local do Jogo' acima está correto antes de aplicar as modificações.\n"
                                                   "⚠ AVISO: O botão 'Aplicar Tradução' instala o Patch Original de segurança contido no ZIP.\n"
                                                   "Ele NÃO aplica alterações feitas no Editor. Para aplicar suas próprias edições, vá na aba Editor e clique em Recompilar.", text_color="gray")
        desc.grid(row=1, column=0, pady=(0, 40))
        
        btn_apply = ctk.CTkButton(self.tab_install, text="Aplicar Tradução PT-BR", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.apply_patch)
        btn_apply.grid(row=2, column=0, pady=10, padx=100, sticky="ew")
        
        btn_restore = ctk.CTkButton(self.tab_install, text="Restaurar Inglês Original", height=40, fg_color="#8B0000", hover_color="#5C0000", command=self.restore_english)
        btn_restore.grid(row=3, column=0, pady=20, padx=150, sticky="ew")

    def apply_patch(self):
        self.tabview.set("Logs")
        
        patch_zip = os.path.join(ROOT_DIR, "Alpha_Centauri_PTBR_Patch.zip")
        if getattr(sys, 'frozen', False):
            # If exe, assume zip is in the parent directory of Tools or next to it
            patch_zip = os.path.join(os.path.dirname(sys.executable), "..", "Alpha_Centauri_PTBR_Patch.zip")
            if not os.path.exists(patch_zip):
                patch_zip = os.path.join(os.path.dirname(sys.executable), "Alpha_Centauri_PTBR_Patch.zip")

        game_d = self.game_dir.get().strip()
        if not game_d or not os.path.isdir(game_d):
            messagebox.showerror("Erro", "Por favor, selecione a pasta correta do jogo.")
            return
        if not os.path.exists(patch_zip):
            messagebox.showerror("Erro", f"Patch zip não encontrado:\n{patch_zip}")
            return
            
        try:
            self.log(f"Iniciando extração do patch de tradução...")
            with zipfile.ZipFile(patch_zip, 'r') as zf:
                zf.extractall(game_d)
            self.log(f"Patch extraído com sucesso para: {game_d}")
            messagebox.showinfo("Sucesso", "Tradução aplicada com sucesso!")
        except Exception as e:
            self.log(f"Erro ao extrair patch: {str(e)}")
            messagebox.showerror("Erro", f"Falha ao extrair arquivos:\n{str(e)}")

    def restore_english(self):
        self.tabview.set("Logs")
        
        backup_zip = os.path.join(BASE_DIR, "backup_en.zip")
        if not os.path.exists(backup_zip):
            messagebox.showerror("Erro", f"Backup original não encontrado na pasta do programa:\n{backup_zip}")
            return
            
        game_d = self.game_dir.get().strip()
        if not game_d or not os.path.isdir(game_d):
            messagebox.showerror("Erro", "Por favor, selecione a pasta correta do jogo.")
            return
            
        if messagebox.askyesno("Confirmar", "Isso irá sobrescrever os arquivos traduzidos e retornar o jogo ao inglês original. Continuar?"):
            try:
                self.log(f"Iniciando restauração do backup original em inglês...")
                with zipfile.ZipFile(backup_zip, 'r') as zf:
                    zf.extractall(game_d)
                    
                self.log(f"Jogo restaurado para o original com sucesso!")
                messagebox.showinfo("Sucesso", "Jogo restaurado para o inglês original.")
            except Exception as e:
                self.log(f"Erro ao restaurar jogo: {str(e)}")
                messagebox.showerror("Erro", f"Falha ao restaurar arquivos:\n{str(e)}")

    def setup_ini_tab(self):
        self.tab_ini.grid_columnconfigure(0, weight=1)
        self.tab_ini.grid_rowconfigure(1, weight=1)
        
        info_frame = ctk.CTkFrame(self.tab_ini)
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_text = ("Configurações úteis para o Alpha Centauri.ini:\n\n"
                    "[Correção de Tela Preta/Problemas de Inicialização]\n"
                    "DirectDraw=0           -> (Recomendado) Desativa aceleração antiga, resolve tela preta no Windows 10/11\n"
                    "DisableOpeningMovie=1  -> (Recomendado) Desativa a intro que costuma travar o jogo\n\n"
                    "[Melhorias Gráficas e de UI]\n"
                    "eax=1                  -> Habilita efeitos de áudio 3D avançados (EAX) se sua placa suportar\n"
                    "FastFind=0             -> Corrige possíveis glitches ao localizar unidades na tela\n"
                    "ForceOldVoxelAlgorithm=1 -> Conserta artefatos visuais nos voxels de terreno em placas modernas\n"
                    "MainFontSize=16        -> Aumenta a fonte principal do jogo para telas de alta resolução\n\n"
                    "Para editar: carregue o arquivo, altere ou adicione as linhas acima na seção [Alpha Centauri] e clique em Salvar.")
        ctk.CTkLabel(info_frame, text=info_text, justify="left", font=ctk.CTkFont(size=12)).pack(padx=10, pady=10)
        
        self.ini_text = ctk.CTkTextbox(self.tab_ini, font=("Consolas", 12))
        self.ini_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(self.tab_ini, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Carregar Alpha Centauri.ini", command=self.load_ini).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self.save_ini).pack(side="right", padx=5)

    def load_ini(self):
        ini_path = os.path.join(self.game_dir.get(), "Alpha Centauri.ini")
        if not os.path.exists(ini_path):
            messagebox.showwarning("Aviso", "O arquivo Alpha Centauri.ini não foi encontrado. Você precisa iniciar o jogo pelo menos uma vez para que ele seja gerado.")
            return
            
        try:
            with open(ini_path, "r", encoding="cp1252", errors="replace") as f:
                content = f.read()
            self.ini_text.delete("1.0", "end")
            self.ini_text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler arquivo:\n{str(e)}")

    def save_ini(self):
        ini_path = os.path.join(self.game_dir.get(), "Alpha Centauri.ini")
        content = self.ini_text.get("1.0", "end-1c")
        if not content.strip():
            return
            
        try:
            with open(ini_path, "w", encoding="cp1252", errors="replace") as f:
                f.write(content)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso no Alpha Centauri.ini!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")

    def setup_cache_tab(self):
        self.tab_cache.grid_columnconfigure(0, weight=1)
        self.tab_cache.grid_rowconfigure(3, weight=1)
        
        self.cache_data = {}
        self.cache_keys = []
        
        # Info Warning
        warning_lbl = ctk.CTkLabel(self.tab_cache, text="⚠ AVISO: Não altere variáveis com cifrão (ex: $NUM0) ou tags entre chaves (ex: {TOUR}). O jogo precisa delas!\n"
                                                        "Suas edições aqui modificam o Cache com segurança. Para que elas apareçam no jogo,\n"
                                                        "clique em 'Recompilar' no final da tela. (O Patch Original na primeira aba não será afetado).", text_color="#FFD700")
        warning_lbl.grid(row=0, column=0, sticky="ew", pady=(5, 0))

        # Search
        search_frame = ctk.CTkFrame(self.tab_cache, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        search_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_frame, text="Pesquisar:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_cache)
        ctk.CTkEntry(search_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(search_frame, text="Carregar Cache", width=120, command=self.load_cache).grid(row=0, column=2, padx=5)
        ctk.CTkButton(search_frame, text="Restaurar Cache Original", width=150, fg_color="#8B0000", hover_color="#5C0000", command=self.restore_cache).grid(row=0, column=3, padx=5)
        
        self.search_count_lbl = ctk.CTkLabel(search_frame, text="Resultados: 0", text_color="#aaaaaa")
        self.search_count_lbl.grid(row=0, column=4, padx=10)
        
        # List
        self.cache_listbox = tk.Listbox(self.tab_cache, bg="#2b2b2b", fg="white", selectbackground="#1f538d", exportselection=False)
        self.cache_listbox.grid(row=2, column=0, rowspan=2, sticky="nsew", padx=10, pady=5)
        self.cache_listbox.bind("<<ListboxSelect>>", self.on_cache_select)
        
        # Editor
        editor_frame = ctk.CTkFrame(self.tab_cache)
        editor_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        editor_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(editor_frame, text="Original (Inglês):").grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.txt_original = ctk.CTkTextbox(editor_frame, height=60, state="disabled")
        self.txt_original.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(editor_frame, text="Tradução (PT-BR):").grid(row=1, column=0, sticky="nw", padx=10, pady=10)
        self.txt_translated = ctk.CTkTextbox(editor_frame, height=60)
        self.txt_translated.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(editor_frame, text="Salvar Alteração no Cache", command=self.save_cache_item).grid(row=2, column=1, sticky="e", padx=10, pady=10)
        
        # Recompile
        compile_frame = ctk.CTkFrame(self.tab_cache, fg_color="transparent")
        compile_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        
        self.compile_status = ctk.CTkLabel(compile_frame, text="")
        self.compile_status.pack(side="left", padx=10)
        
        ctk.CTkButton(compile_frame, text="Recompilar Arquivos do Jogo", fg_color="#228B22", hover_color="#006400", command=self.recompile_game).pack(side="right", padx=10)

    def restore_cache(self):
        backup_path = os.path.join(BASE_DIR, "translation_cache.backup.json")
        cache_path = os.path.join(BASE_DIR, "translation_cache.json")
        
        if not os.path.exists(backup_path):
            messagebox.showerror("Erro", "O arquivo de backup (translation_cache.backup.json) não foi encontrado.")
            return
            
        if messagebox.askyesno("Restaurar Cache Original", "Tem certeza que deseja restaurar o cache para o original? Todas as suas traduções personalizadas serão perdidas!"):
            try:
                shutil.copy2(backup_path, cache_path)
                self.load_cache()
                messagebox.showinfo("Sucesso", "Cache restaurado com sucesso para a versão original.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao restaurar cache:\n{str(e)}")

    def load_cache(self):
        cache_path = os.path.join(BASE_DIR, "translation_cache.json")
        if not os.path.exists(cache_path):
            messagebox.showwarning("Aviso", "translation_cache.json não encontrado.")
            return
            
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                self.cache_data = json.load(f)
            self.cache_keys = list(self.cache_data.keys())
            self.filter_cache()
            messagebox.showinfo("Sucesso", f"{len(self.cache_keys)} textos carregados do cache.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar cache:\n{str(e)}")

    def filter_cache(self, *args):
        search_term = self.search_var.get().lower()
        self.cache_listbox.delete(0, tk.END)
        
        count = 0
        total_count = 0
        for k in self.cache_keys:
            v = self.cache_data[k]
            if search_term in k.lower() or search_term in v.lower():
                self.cache_listbox.insert(tk.END, k)
                count += 1
                total_count += 1
                if count > 1000: # Limit display for performance
                    pass # Don't break, so we can get the total count
        
        if total_count > 1000:
            self.search_count_lbl.configure(text=f"Resultados: {total_count} (Exibindo 1000)")
            # Delete entries past 1000 to save UI performance
            self.cache_listbox.delete(1000, tk.END)
        else:
            self.search_count_lbl.configure(text=f"Resultados: {total_count}")

    def on_cache_select(self, event):
        selection = self.cache_listbox.curselection()
        if not selection:
            return
            
        key = self.cache_listbox.get(selection[0])
        val = self.cache_data.get(key, "")
        
        self.txt_original.configure(state="normal")
        self.txt_original.delete("1.0", "end")
        self.txt_original.insert("1.0", key)
        self.txt_original.configure(state="disabled")
        
        self.txt_translated.delete("1.0", "end")
        self.txt_translated.insert("1.0", val)

    def save_cache_item(self):
        self.txt_original.configure(state="normal")
        key = self.txt_original.get("1.0", "end-1c")
        self.txt_original.configure(state="disabled")
        
        if not key:
            return
            
        val = self.txt_translated.get("1.0", "end-1c")
        self.cache_data[key] = val
        
        # Save to file
        cache_path = os.path.join(BASE_DIR, "translation_cache.json")
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2)
            self.compile_status.configure(text=f"Tradução para '{key[:15]}...' salva no cache.", text_color="green")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cache:\n{str(e)}")

    def recompile_game(self):
        self.tabview.set("Logs")
        
        script1 = os.path.join(BASE_DIR, "translate_game.py")
        script2 = os.path.join(BASE_DIR, "translate_phase2.py")
        game_d = self.game_dir.get().strip()
        if not game_d or not os.path.isdir(game_d):
            messagebox.showerror("Erro", "Por favor, selecione a pasta correta do jogo.")
            return
        
        if not os.path.exists(script1) or not os.path.exists(script2):
            messagebox.showerror("Erro", "Scripts de tradução não encontrados na pasta Tools.")
            return
            
        if not os.path.exists(game_d):
            messagebox.showerror("Erro", "Pasta do jogo não encontrada.")
            return

        # Disable buttons
        self.compile_status.configure(text="Recompilando textos... Isso pode levar alguns minutos.", text_color="orange")
        
        def run_compilation():
            import sys
            import io
            
            class LogRedirector(io.StringIO):
                def write(self, string):
                    if string.strip():
                        self_app.log(string.strip())
            
            self_app = self
            old_stdout = sys.stdout
            sys.stdout = LogRedirector()
            
            try:
                import importlib
                import translate_phase2
                import translate_game
                
                importlib.reload(translate_phase2)
                importlib.reload(translate_game)
                
                build_dir = os.path.join(BASE_DIR, "build")
                
                # Update paths dynamically before running
                translate_phase2.GAME_DIR = game_d
                translate_phase2.BUILD_DIR = build_dir
                translate_phase2.BACKUP_DIR = os.path.join(game_d, "backup_en")
                translate_phase2.CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")
                
                translate_game.GAME_DIR = game_d
                translate_game.BUILD_DIR = build_dir
                translate_game.BACKUP_DIR = os.path.join(game_d, "backup_en")
                translate_game.CACHE_FILE = os.path.join(BASE_DIR, "translation_cache.json")
                
                self.log("Iniciando Fase 2 de Tradução...")
                translate_phase2.main()
                
                self.log("Iniciando Fase 1 de Tradução...")
                translate_game.main()
                
                self.log("Copiando arquivos atualizados para a pasta do jogo...")
                build_dir = os.path.join(BASE_DIR, "build")
                for filename in os.listdir(build_dir):
                    src_file = os.path.join(build_dir, filename)
                    dst_file = os.path.join(game_d, filename)
                    if os.path.isfile(src_file):
                        shutil.copy2(src_file, dst_file)
                self.log("Todos os arquivos foram aplicados com sucesso ao jogo!")
                
                sys.stdout = old_stdout
                self.log("Recompilação finalizada com sucesso!")
                self.after(0, lambda: self.compile_status.configure(text="Recompilação concluída com sucesso! Pode abrir o jogo.", text_color="green"))
                self.after(0, lambda: messagebox.showinfo("Sucesso", "Textos do jogo foram atualizados com base no cache!"))
            except Exception as e:
                sys.stdout = old_stdout
                self.log(f"Erro fatal na recompilação: {str(e)}")
                self.after(0, lambda: self.compile_status.configure(text="Erro na recompilação.", text_color="red"))
                self.after(0, lambda: messagebox.showerror("Erro", f"Falha na execução dos scripts:\n{str(e)}"))

        threading.Thread(target=run_compilation, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()


