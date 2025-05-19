
# 📝 Gerador de Gabaritos Personalizados

Uma aplicação com interface gráfica feita em Python para gerar sequências de gabaritos balanceadas e exportá-las como `.txt` e `.pdf`, com suporte a customização, estilos de banca e importação de arquivos externos como DOCX e PDF.

---

## 📦 Funcionalidades

- 🎯 Geração balanceada de gabaritos com 2, 4 ou 5 alternativas (ex: C/E, A-D, A-E)
- 🧠 Níveis de dificuldade ajustáveis (Fácil, Médio, Difícil, Modo Extremo)
- 📂 Importação de arquivos `.docx` e `.pdf` com leitura automática de conteúdo
- 🧾 Exportação para `.txt` e `.pdf`
- 💾 Lembrança de configurações anteriores (salvas em `user_config.json`)
- 🔁 Verificação de atualizações via GitHub
- 💡 Interface visual com `ttkbootstrap`

---

## 🖼️ Interface

![screenshot](https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/refs/heads/master/assets/preview.png)

---

## 🚀 Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/A1cantar4/gerador-de-gabaritos-personalizados.git
cd gerador-de-gabaritos-personalizados
```

### 2. Instalar dependências

Você pode usar `pip`:

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install ttkbootstrap python-docx PyPDF2 reportlab Pillow requests
```

### 3. Executar o programa

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
gerador-de-gabaritos-personalizados/
│
├── core/
│   ├── gerador.py         # Geração do gabarito balanceado
│   ├── leitor.py          # Leitura de arquivos DOCX e PDF
│   ├── exportador.py      # Exportação para PDF com ReportLab
│   ├── atualizador.py     # Sistema de atualização automática
│   ├── configuracoes.py   # Gerenciamento de configurações do usuário
│   └── versao.py          # Versão atual da aplicação
│
├── ui/
│   ├── layout.py          # Classe principal da interface
│   ├── estilo.py          # Estilo visual (cores, fontes, bordas)
│   ├── entrada.py         # Criação dos campos e opções da UI
│   └── funcoes.py         # Lógica dos botões (salvar, importar, etc.)
│
├── assets/
│   ├── icon.ico
│   ├── preview.png
│   ├── DejaVuSans.ttf     # Fonte dos arquivos
│   └── background.png
│
├── user_config.json       # Configurações salvas do usuário
├── requirements.txt       # Dependências do projeto
├── main.py                # Arquivo principal de execução
└── README.md              # Este arquivo
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Tkinter + ttkbootstrap** — interface gráfica moderna
- **ReportLab** — geração de PDFs
- **python-docx / PyPDF2** — leitura de arquivos
- **Pillow** — imagens no app
- **Requests** — atualizações automáticas

---

## 🧪 Testado em

- Windows 10/11
- Python 3.10+

---

## 🗂️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 🤝 Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma *issue* primeiro para discutir o que você gostaria de modificar.

---

## 👨‍💻 Autor

Desenvolvido por [A1cantar4](https://github.com/A1cantar4) com 💙
