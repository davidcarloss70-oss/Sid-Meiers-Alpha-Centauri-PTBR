import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace tab name
content = content.replace('self.tabview.add("Correção Tela Preta (.ini)")', 'self.tabview.add("Edição de .ini")')

# We need to find def setup_ini_tab(self): and replace it entirely up to def load_ini(self):
import re
pattern = re.compile(r'def setup_ini_tab\(self\):.*?def load_ini\(self\):', re.DOTALL)

new_setup = '''def setup_ini_tab(self):
        self.tab_ini.grid_columnconfigure(0, weight=1)
        self.tab_ini.grid_rowconfigure(1, weight=1)
        
        info_frame = ctk.CTkFrame(self.tab_ini)
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        info_text = ("Editor de Alpha Centauri.ini:\\n\\n"
                     "Use os botões abaixo para gerenciar o arquivo de configuração do jogo.\\n"
                     "Recomendamos aplicar a Configuração Otimizada para evitar o travamento (tela preta) "
                     "que ocorre na expansão Alien Crossfire em PCs modernos.")
        ctk.CTkLabel(info_frame, text=info_text, justify="left", font=ctk.CTkFont(size=12)).pack(padx=10, pady=10)
        
        btn_top_frame = ctk.CTkFrame(self.tab_ini, fg_color="transparent")
        btn_top_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkButton(btn_top_frame, text="Carregar .ini do Jogo", command=self.load_ini).pack(side="left", padx=5)
        ctk.CTkButton(btn_top_frame, text="Aplicar Configuração Otimizada", command=self.apply_recommended_ini).pack(side="left", padx=5)
        ctk.CTkButton(btn_top_frame, text="Voltar .ini Original", command=self.reset_ini).pack(side="right", padx=5)
        
        self.ini_text = ctk.CTkTextbox(self.tab_ini, font=("Consolas", 12))
        self.ini_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        btn_bottom_frame = ctk.CTkFrame(self.tab_ini, fg_color="transparent")
        btn_bottom_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(btn_bottom_frame, text="Salvar Alterações no Jogo", command=self.save_ini).pack(side="right", padx=5)

    def apply_recommended_ini(self):
        recommended = """[PREFERENCES]

[Alpha Centauri]
ForceOldVoxelAlgorithm=1
DisableOpeningMovie=1
ds3d=1
eax=1
DirectDraw=1

FastUnitAnim=0
SmoothUnitAnim=0
MainFontSize=16
InterludeFontSize=16
Prefs Format=12
Difficulty=0
Map Type=0
Top Menu=1
Faction=1
Preferences=10111011111000011101110110110110
More Preferences=1110100111000101101000
Semaphore=00000000
Announce=111100001110101001
Rules=1101000001110
Customize=0
Custom World=2, 1, 1, 1, 1, 1, 1,                                
Time Controls=1
Latest Save=
Latest Scenario=
DontResetBeginnerPrefs=0

[PRACX]
Disabled=<DEFAULT>
ScreenWidth=<DEFAULT>
ScreenHeight=<DEFAULT>
WindowWidth=<DEFAULT>
WindowHeight=<DEFAULT>
ZoomLevels=<DEFAULT>
ScrollMin=<DEFAULT>
ScrollMax=<DEFAULT>
ScrollArea=<DEFAULT>
MouseOverTileInfo=<DEFAULT>
ShowUnworkedCityResources=<DEFAULT>
ListScrollLines=<DEFAULT>
ZoomedOutShowDetails=<DEFAULT>
MoviePlayerCommand=<DEFAULT>"""
        self.ini_text.delete("1.0", "end")
        self.ini_text.insert("1.0", recommended)

    def reset_ini(self):
        # Clears the file essentially so the game can recreate it, or inserts a bare minimum
        minimal = """[Alpha Centauri]"""
        self.ini_text.delete("1.0", "end")
        self.ini_text.insert("1.0", minimal)
        
    def load_ini(self):'''

content = pattern.sub(new_setup, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("App updated successfully.")
