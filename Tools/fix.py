with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if 'info_text = ("Editor de Alpha Centauri.ini:' in line:
        skip = True
        new_lines.append('        info_text = ("Editor de Alpha Centauri.ini:\\n\\n" "Use os botões abaixo para gerenciar o arquivo de configuração do jogo.\\n" "Recomendamos aplicar a Configuração Otimizada para evitar o travamento (tela preta) " "que ocorre na expansão Alien Crossfire em PCs modernos.")\n')
        continue
    if skip:
        if 'que ocorre na expansão Alien Crossfire em PCs modernos.")' in line:
            skip = False
        continue
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
