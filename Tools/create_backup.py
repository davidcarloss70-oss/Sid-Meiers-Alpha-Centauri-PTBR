import zipfile
import os

game_dir = r"C:\Program Files (x86)\GOG Galaxy\Games\Sid Meier's Alpha Centauri Planetary Pack"
backup_zip = r"C:\Users\david\Documents\GitHub\Alpha-Centauri-PTBR\Tools\backup_en.zip"

files_to_backup = [
    'labels.txt', 'concepts.txt', 'alpha.txt', 'alphax.txt', 'menus.txt',
    'gaians.txt', 'hive.txt', 'univ.txt', 'morgan.txt', 'spartans.txt', 'believers.txt', 'peace.txt',
    'cyborgs.txt', 'pirates.txt', 'drone.txt', 'angels.txt', 'fungus.txt', 'alien1.txt', 'alien2.txt',
    'script.txt', 'interfac.txt', 'tutorial.txt', 'faction.txt', 'blurbs.txt'
]

with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_backup:
        path = os.path.join(game_dir, f)
        if os.path.exists(path):
            zf.write(path, f)
            print(f'Added {f}')

print('Backup created successfully!')
