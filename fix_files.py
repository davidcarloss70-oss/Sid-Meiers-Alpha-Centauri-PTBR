import re

files_to_fix = [
    'Tools/backup_test/xscript.txt',
    'Tools/backup_test/Script.txt',
    'Tools/backup_test/alphax.txt',
    'Tools/backup_test/alpha.txt'
]

for filepath in files_to_fix:
    try:
        with open(filepath, 'r', encoding='cp1252', errors='ignore') as f:
            content = f.read()
            
        new_content = content.replace('TTULO', 'TITLE').replace('TTULO', 'TITLE').replace('NOME', 'NAME')
        new_content = new_content.replace('TTULO', 'TITLE')
        new_content = new_content.replace('TÍTULO', 'TITLE')
        new_content = re.sub(r'\.TULO', '', new_content)
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        new_content = new_content.replace('', '')
        
        if new_content != content:
            with open(filepath, 'w', encoding='cp1252', errors='ignore') as f:
                f.write(new_content)
            print(f'Fixed variables in {filepath}')
    except Exception as e:
        print(f'Could not process {filepath}: {e}')
