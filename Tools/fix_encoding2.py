import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

try:
    # Attempt to fix double utf-8 encoding (utf-8 read as cp1252 and saved as utf-8)
    fixed_content = content.encode('windows-1252').decode('utf-8')
except Exception as e:
    print('Encoding trick failed:', e)
    fixed_content = content.replace('InstalaÃ§Ã£o', 'Instalação') \
                           .replace('CorreÃ§Ã£o', 'Correção') \
                           .replace('AvanÃ§ado', 'Avançado') \
                           .replace('ConfiguraÃ§Ãµes', 'Configurações') \
                           .replace('inglÃªs', 'inglês') \
                           .replace('TraduÃ§Ã£o', 'Tradução') \
                           .replace('NÃƒO', 'NÃO') \
                           .replace('NÃ£o', 'Não') \
                           .replace('ediÃ§Ãµes', 'edições') \
                           .replace('prÃ³prias', 'próprias') \
                           .replace('vÃ¡', 'vá') \
                           .replace('botÃ£o', 'botão') \
                           .replace('serÃ¡', 'será') \
                           .replace('sÃ³', 'só') \
                           .replace('VocÃª', 'Você') \
                           .replace('modificaÃ§Ãµes', 'modificações') \
                           .replace('apareÃ§am', 'apareçam') \
                           .replace('seguranÃ§a', 'segurança') \
                           .replace('variÃ¡veis', 'variáveis') \
                           .replace('âš', '⚠')

# Fix the DirectDraw=0
fixed_content = fixed_content.replace('DirectDraw=1', 'DirectDraw=0')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print('app.py fixed!')
