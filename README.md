# Gerador de Gabaritos Personalizados

Aplicativo com interface gráfica moderna para gerar gabaritos de provas personalizados, ideal para simular questões no estilo de bancas como IBAM, entre outras.

---

## ✅ Funcionalidades

- Geração de gabaritos com distribuição equilibrada de alternativas.
- Suporte a 2, 4 ou 5 alternativas (C/E, A-D, A-E).
- Interface amigável com temas modernos (via `ttkbootstrap`).
- Nome do arquivo personalizado com assunto e banca.
- Armazena preferências do usuário localmente.
- Atualização automática via GitHub.
- Totalmente modularizado para manutenção e expansão.

---

## 🖼️ Interface

A interface permite:

- Inserir assunto e banca examinadora.
- Escolher a quantidade de questões (10 a 200).
- Definir o número de alternativas (2, 4 ou 5).
- Marcar opções como "abrir após salvar" e "usar nome personalizado".

---

## ▶️ Como usar

### 1. Instale os requisitos

```bash
pip install -r requirements.txt
```

### 2. Execute o aplicativo

```bash
python main.py
```

---

## ⚙️ Estrutura do Projeto

```
gerador-de-gabaritos-personalizados/
│
├── main.py                       # ponto de entrada
├── requirements.txt
├── README.md
├── core/                         # lógica de negócio
│   ├── generator.py              # geração de gabarito
│   ├── config.py                 # configurações locais
│   └── updater.py                # verificação de versão
├── ui/                           # interface com o usuário
│   └── layout.py
├── assets/                       # imagens e ícones
│   ├── icon.ico
│   └── background.png
├── GeradorGabaritos.spec         # para gerar executável
└── versao.txt                    # (apenas no GitHub)
```

---

## 🆕 Atualizações

O app verifica automaticamente novas versões via GitHub e oferece atualização com um clique.

---

## 🛠️ Compilação (opcional)

Para compilar um executável com PyInstaller:

Execute o Compliator.bat

---

## 👨‍💻 Autor

Desenvolvido por [@A1cantar4](https://github.com/A1cantar4)
