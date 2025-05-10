import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import os
import sys
import json
import traceback
import webbrowser
import requests
import subprocess

VERSAO_ATUAL = "1.1.3"
GITHUB_RAW_VERSAO_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/versao.txt"
GITHUB_RAW_SCRIPT_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/app.py"

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".gabarito_settings.json")


def carregar_configuracoes():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def salvar_configuracoes(config):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(config, f)
    except:
        pass

config = carregar_configuracoes()

# ======================== GABARITO ========================
def gerar_gabarito_simples(qtd=40, min_pct=22, max_pct=28):
    for _ in range(1000):
        letras = ['A', 'B', 'C', 'D']
        random.shuffle(letras)
        percentuais = [random.randint(min_pct, max_pct) for _ in range(3)]
        restante = 100 - sum(percentuais)
        if min_pct <= restante <= max_pct:
            percentuais.append(restante)
            quantidades = [round(pct * qtd / 100) for pct in percentuais]
            while sum(quantidades) < qtd:
                quantidades[quantidades.index(min(quantidades))] += 1
            while sum(quantidades) > qtd:
                quantidades[quantidades.index(max(quantidades))] -= 1
            gabarito = []
            for letra, quantidade in zip(letras, quantidades):
                gabarito.extend([letra] * quantidade)
            random.shuffle(gabarito)
            if not tem_repeticoes_excessivas(gabarito):
                return gabarito
    raise ValueError("Não foi possível gerar um gabarito com os parâmetros fornecidos.")

def tem_repeticoes_excessivas(lista, max_reps=2):
    count = 1
    for i in range(1, len(lista)):
        if lista[i] == lista[i-1]:
            count += 1
            if count > max_reps:
                return True
        else:
            count = 1
    return False

# ======================== SALVAMENTO ========================
def salvar_gabarito(caminho, apenas_gabarito=False, assunto="", banca="", qtd_questoes=40):
    try:
        gabarito = gerar_gabarito_simples(qtd=qtd_questoes)
        if apenas_gabarito:
            texto = '\n'.join([f"{i+1}. {letra}" for i, letra in enumerate(gabarito)])
            with open(os.path.join(os.path.dirname(caminho), "apenas_gabarito.txt"), "w") as f:
                f.write(texto)
        else:
            instrucao = (
                f"Gere 5 questões objetivas sobre \"{assunto}\", difíceis e bem elaboradas, no estilo da banca \"{banca}\", "
                "seguindo o seguinte formato:\n\n"
                "- Enunciado claro e realista, apenas diga o gabarito quando solicitado\n"
                "- Quatro alternativas (A, B, C, D)\n"
                "- Apenas uma correta\n"
                "- **A posição correta deve seguir, em ordem, a sequência de letras fornecida abaixo**\n"
                "- **Use essa sequência apenas para estruturar as questões**\n"
                "- **Não repita nem mencione essa sequência na resposta**\n\n"
                "Sequência de gabarito:\n"
                f"{''.join(gabarito)}\n"
            )
            with open(caminho, "w") as f:
                f.write(instrucao)
    except Exception as e:
        registrar_erro(e)

# ======================== ERROS ========================
def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

# ======================== ATUALIZAÇÃO ========================
def verificar_e_atualizar():
    try:
        r = requests.get(GITHUB_RAW_VERSAO_URL)
        if r.status_code == 200:
            versao_online = r.text.strip()
            if versao_online != VERSAO_ATUAL:
                resp = messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?")
                if resp:
                    novo_script = requests.get(GITHUB_RAW_SCRIPT_URL)
                    if novo_script.status_code == 200:
                        caminho_atual = os.path.abspath(sys.argv[0])
                        with open(caminho_atual, "w", encoding="utf-8") as f:
                            f.write(novo_script.text)
                        messagebox.showinfo("Atualizado", "Aplicativo atualizado. Reiniciando...")
                        subprocess.Popen([sys.executable, caminho_atual])
                        sys.exit()
    except Exception as e:
        registrar_erro(e)

# ======================== UI ========================
def salvar():
    assunto = entry_assunto.get().strip()
    banca = entry_banca.get().strip()
    if not assunto or not banca:
        entry_assunto.config(bg="#ffcccc")
        entry_banca.config(bg="#ffcccc")
        return

    entry_assunto.config(bg="white" if not modo_escuro.get() else "#333333")
    entry_banca.config(bg="white" if not modo_escuro.get() else "#333333")

    pasta = config.get("pasta_salvamento", os.getcwd()) if var_mesma_pasta.get() else filedialog.askdirectory()
    if not pasta:
        return

    config["pasta_salvamento"] = pasta
    salvar_configuracoes(config)

    nome = assunto if var_nome_personalizado.get() else "gabarito.txt"
    caminho = os.path.join(pasta, nome if nome.endswith(".txt") else f"{nome}.txt")
    salvar_gabarito(
        caminho,
        apenas_gabarito=var_apenas_gabarito.get(),
        assunto=assunto,
        banca=banca,
        qtd_questoes=int(spin_qtd.get())
    )

    if var_abrir_apos_salvar.get():
        webbrowser.open(pasta)

    messagebox.showinfo("Sucesso", f"Gabarito salvo em:\n{caminho}")

def alternar_tema():
    tema = "dark" if modo_escuro.get() else "light"
    aplicar_tema(tema)
    config["tema"] = tema
    salvar_configuracoes(config)

def aplicar_tema(tema):
    bg = "#333333" if tema == "dark" else "#ffffff"
    fg = "#ffffff" if tema == "dark" else "#000000"
    root.configure(bg=bg)
    frame.configure(bg=bg)
    for widget in frame.winfo_children():
        if isinstance(widget, (tk.Label, tk.Checkbutton, tk.Button)):
            widget.configure(bg=bg, fg=fg)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg="#555555" if tema == "dark" else "white", fg=fg)
    versao_label.configure(bg="#dddddd", fg="#000000")

# ======================== JANELA ========================
root = tk.Tk()
root.title("GeradorDeGabaritosPersonalizados")
root.geometry("460x500")
root.resizable(False, False)

# Ícone e background
try:
    root.iconbitmap("icon.ico")
except:
    pass

background_image = None
try:
    bg_image = Image.open("background.png")
    background_image = ImageTk.PhotoImage(bg_image.resize((460, 500)))
    bg_label = tk.Label(root, image=background_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff")
frame.place(x=0, y=0, relwidth=1, relheight=0.9)

modo_escuro = tk.BooleanVar(value=config.get("tema") == "dark")
var_nome_personalizado = tk.BooleanVar(value=config.get("nome_personalizado", True))
var_apenas_gabarito = tk.BooleanVar()
var_mesma_pasta = tk.BooleanVar()
var_abrir_apos_salvar = tk.BooleanVar()

# Widgets
widgets = [
    (tk.Label(frame, text="Assunto:"), 0, 0, 'e'),
    (tk.Entry(frame, width=35), 0, 1, 'w', 2),
    (tk.Label(frame, text="Banca examinadora:"), 1, 0, 'e'),
    (tk.Entry(frame, width=35), 1, 1, 'w', 2),
    (tk.Label(frame, text="Quantidade de questões:"), 2, 0, 'e'),
    (tk.Spinbox(frame, from_=10, to=200, width=5), 2, 1, 'w'),
    (tk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=var_nome_personalizado), 3, 0, 'w', 2),
    (tk.Checkbutton(frame, text="Salvar outro arquivo com apenas o gabarito", variable=var_apenas_gabarito), 4, 0, 'w', 2),
    (tk.Checkbutton(frame, text="Salvar na mesma pasta", variable=var_mesma_pasta), 5, 0, 'w', 2),
    (tk.Checkbutton(frame, text="Abrir pasta após salvar", variable=var_abrir_apos_salvar), 6, 0, 'w', 2),
    (tk.Checkbutton(frame, text="Modo Escuro", variable=modo_escuro, command=alternar_tema), 7, 0, 'w', 2)
]

for widget, r, c, sticky, colspan in map(lambda x: (*x, 1) if len(x) == 4 else x, widgets):
    widget.grid(row=r, column=c, columnspan=colspan, sticky=sticky, pady=2)

entry_assunto = widgets[1][0]
entry_banca = widgets[3][0]
spin_qtd = widgets[5][0]

# Rodapé
versao_label = tk.Label(root, text=f"Versão {VERSAO_ATUAL}", anchor='se', bg="#dddddd")
versao_label.pack(side='left', fill='x', padx=5, pady=5)
tk.Button(root, text="Salvar Gabarito", command=salvar).pack(side="right", padx=10, pady=10)

aplicar_tema("dark" if modo_escuro.get() else "light")
verificar_e_atualizar()
root.mainloop()
