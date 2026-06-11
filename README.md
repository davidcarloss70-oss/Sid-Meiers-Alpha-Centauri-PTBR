# Alpha Centauri PT-BR

Tradução para o português brasileiro (PT-BR) do clássico jogo **Sid Meier's Alpha Centauri Planetary Pack**.

Este projeto contém o patch de tradução completo, além de uma aplicação exclusiva (interface gráfica) que permite não só a instalação fácil da tradução, mas também a customização e edição dos textos pelo próprio jogador!

---

## 🚀 Como Instalar a Tradução

Você tem duas opções para instalar a tradução no seu jogo:

### Opção 1: Instalação Manual (Rápida)
1. Baixe o arquivo **`Alpha_Centauri_PTBR_Patch.zip`** que está na raiz deste repositório.
2. Extraia **todo o conteúdo** do arquivo `.zip` diretamente na pasta raiz onde o seu jogo está instalado (ex: `C:\Program Files (x86)\GOG Galaxy\Games\Sid Meier's Alpha Centauri Planetary Pack`).
3. Confirme a substituição dos arquivos quando o Windows perguntar.
4. Pronto! O jogo já está traduzido.

### Opção 2: Instalação via Aplicativo (Recomendado)
Para uma experiência mais completa e segura, utilize a nossa ferramenta:
1. Acesse a pasta **`Tools`** neste repositório.
2. Execute o arquivo **`Alpha_Centauri_Tradutor_UI.exe`**.
3. Na aba **Instalação**, confirme se o caminho para a pasta do seu jogo está correto.
4. Clique no botão **Aplicar Tradução**. O aplicativo instalará o patch e criará um backup automático dos seus arquivos originais.
5. Se desejar, utilize a aba **Arquivo INI** na ferramenta para injetar as chaves de otimização de resolução e compatibilidade no seu `Alpha Centauri.ini`.

---

## 🛠️ Ferramenta de Edição (Tools)

Além de instalar a tradução, o **`Alpha_Centauri_Tradutor_UI.exe`** possui um **Editor de Traduções** embutido.

Caso você encontre alguma frase no jogo que prefira mudar, algum erro de digitação, ou apenas queira adaptar a tradução para o seu gosto pessoal:
1. Abra o aplicativo e vá até a aba **Editor**.
2. Faça uma busca pelo texto que deseja alterar (você pode pesquisar tanto pelo texto original em inglês quanto pela tradução atual).
3. Selecione a linha, edite o texto na parte de baixo e clique em **Salvar**.
4. Quando terminar suas edições, clique no botão **Recompilar**. 
5. O aplicativo irá injetar automaticamente suas mudanças no jogo! *(Nota: Esta ação modifica apenas os arquivos locais do seu jogo e funciona como um "sandbox", sem alterar o Patch ZIP original).*

Se algo der errado, você sempre pode usar a aba **Instalação** para **Restaurar o Inglês Original**.

---

## 📝 Sobre o Processo de Tradução

A tradução deste jogo massivo foi uma jornada técnica e linguística! O processo envolveu:
* Extração e injeção reversa dos arquivos `.txt` originais da engine do jogo.
* Tradução automatizada em massa utilizando a **API do Google Tradutor** para os textos pesados.
* Auxílio extensivo de **Inteligência Artificial** para criar as ferramentas de extração, revisar contextos iniciais e desenvolver o Editor Gráfico em Python/CustomTkinter.
* Revisão e correções manuais (feitas por humanos) para adequar termos técnicos e garantir a imersão do universo sci-fi da obra-prima de Sid Meier.

Por ser um projeto vasto e o jogo possuir dezenas de milhares de linhas, a aplicação de edição foi deixada à disposição para que a própria comunidade de jogadores possa ajudar a refinar e ajustar qualquer detalhe que tenha passado despercebido.

---

## 🏆 Créditos

* **Idealização, Tradução e Revisão Humana:** [davidcarloss70-oss](https://github.com/davidcarloss70-oss)
* **Engenharia de Software e IA:** Antigravity (IA)

Aproveite o jogo e nos vemos em Planeta!
