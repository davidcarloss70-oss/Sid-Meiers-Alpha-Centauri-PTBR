import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining encodings
replacements = {
    'estÃ¡': 'está',
    'InglÃªs': 'Inglês',
    'cifrÃ£o': 'cifrão',
    'nÃ£o': 'não',
    'AlteraÃ§Ãµes': 'Alterações'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py fixed again!')
