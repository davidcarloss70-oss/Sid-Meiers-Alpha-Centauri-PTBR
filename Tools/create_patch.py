import zipfile
import os

build_dir = r"C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\build"
patch_zip = r"C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Alpha_Centauri_PTBR_Patch.zip"

files_to_zip = [
    'labels.txt', 'concepts.txt', 'alpha.txt', 'alphax.txt', 'menus.txt',
    'gaians.txt', 'hive.txt', 'univ.txt', 'morgan.txt', 'spartans.txt', 'believers.txt', 'peace.txt',
    'cyborgs.txt', 'pirates.txt', 'drone.txt', 'angels.txt', 'fungboy.txt', 'caretake.txt', 'usurper.txt',
    'script.txt', 'interfac.txt', 'tutor.txt', 'faction.txt', 'blurbs.txt', 'Alpha Centauri.ini'
]

with zipfile.ZipFile(patch_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_zip:
        path = os.path.join(build_dir, f)
        if os.path.exists(path):
            zf.write(path, f)
            print(f'Added {f}')

print('Patch created successfully!')
