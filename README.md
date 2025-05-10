
# Gerador de Gabaritos Personalizados

Aplicativo com interface gráfica para gerar gabaritos de provas de forma automatizada e personalizada, ideal para simular questões no estilo de bancas como IBAM, entre outras.

Desenvolvido por [@A1cantar4](https://github.com/A1cantar4)

---

## ✅ Funcionalidades

- Geração de gabaritos com distribuição equilibrada de alternativas.
- Suporte a 2, 4 ou 5 alternativas (C/E, A-D, A-E).
- Criação de instruções para geração de questões em estilo de banca.
- Personalização do nome do arquivo com assunto e banca.
- Interface gráfica amigável com suporte a temas (via `ttkbootstrap`).
- Ícone e imagem de fundo personalizáveis.
- Salva preferências do usuário automaticamente.
- Atualização automática via GitHub.

---

## 🖼️ Interface

A interface gráfica permite:

- Inserir o assunto e a banca examinadora.
- Definir quantidade de questões (10 a 200).
- Escolher o número de alternativas.
- Marcar opções como salvar com nome personalizado e abrir a pasta após salvar

---

## ▶️ Como usar

1. Instale os requisitos com:
   ```bash
   pip install -r requirements.txt
   ```
   (Você pode criar esse arquivo com: `ttkbootstrap`, `Pillow`, `requests`)

2. Execute o aplicativo com Python 3:
   ```bash
   python app.py
   ```

---

## ⚙️ Compilação (opcional)

Para gerar um executável com o PyInstaller:

```bash
pyinstaller GeradorGabaritos.spec
```

Ou use o script de compilação no Windows:

```bash
compilar.bat
```

---

## 🆕 Atualizações

O app verifica automaticamente se há nova versão disponível no GitHub e permite atualização com um clique.

---

## 📁 Estrutura de Arquivos

- `app.py`: código-fonte principal.
- `compilar.bat`: script para compilar com PyInstaller.
- `GeradorGabaritos.spec`: especificação para compilação.
- `icon.ico`: ícone do programa.
- `background.png`: imagem de fundo da interface (opcional).
- `versao.txt`: arquivo online usado para verificação de versão.