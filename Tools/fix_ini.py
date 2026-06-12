import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the optimized text
start_idx = content.find('ini_optimized_text = """')
if start_idx != -1:
    end_idx = content.find('"""', start_idx + 24)
    if end_idx != -1:
        new_optimized = '''ini_optimized_text = """[PREFERENCES]

[Alpha Centauri]
ForceOldVoxelAlgorithm=1
DisableOpeningMovie=1
ds3d=1
eax=1
DirectDraw=0

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
MoviePlayerCommand=<DEFAULT>"""'''
        content = content[:start_idx] + new_optimized + content[end_idx+3:]

# Find load_ini_original and hardcode the text
load_orig_def = '''def load_ini_original():
    try:
        ini_original_text = """[PREFERENCES]
ForceOldVoxelAlgorithm=0

[Alpha Centauri]

ds3d=1
eax=1
DirectDraw=0

FastUnitAnim=0
SmoothUnitAnim=0
MainFontSize=16
InterludeFontSize=16
DisableOpeningMovie=0
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
        ini_text.delete("1.0", tk.END)
        ini_text.insert(tk.END, ini_original_text)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar original: {e}")'''

import re
content = re.sub(r'def load_ini_original\(\):.*?except Exception as e:.*?messagebox.showerror\("Erro", f"Erro ao carregar original: \{e\}"\)', load_orig_def, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py INI fixed!')
