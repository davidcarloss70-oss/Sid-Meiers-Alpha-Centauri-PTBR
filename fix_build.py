import re
import os

build_dir = 'Tools/build'

for filename in os.listdir(build_dir):
    if not filename.endswith('.txt') and not filename.endswith('.TXT'):
        continue
        
    filepath = os.path.join(build_dir, filename)
    try:
        with open(filepath, 'r', encoding='cp1252', errors='ignore') as f:
            content = f.read()
            
        new_content = content.replace('TTULO', 'TITLE').replace('TTULO', 'TITLE').replace('NOME', 'NAME')
        new_content = new_content.replace('TTULO', 'TITLE')
        new_content = new_content.replace('TÍTULO', 'TITLE')
        new_content = new_content.replace('TTULO', 'TITLE') # handling bad encoding
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
