import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os
import sys
import json
import traceback
import webbrowser
import requests
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

VERSAO_ATUAL = "1.3.5"
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

def gerar_gabarito_simples(qtd=40, letras=None, min_pct=10, max_pct=60):
    if letras is None:
        letras = ['A', 'B', 'C', 'D']
    for _ in range(1000):
        letras_embaralhadas = letras[:]
        random.shuffle(letras_embaralhadas)
        percentuais = [random.randint(min_pct, max_pct) for _ in range(len(letras) - 1)]
        restante = 100 - sum(percentuais)
        if min_pct <= restante <= max_pct:
            percentuais.append(restante)
            quantidades = [round(pct * qtd / 100) for pct in percentuais]
            while sum(quantidades) < qtd:
                quantidades[quantidades.index(min(quantidades))] += 1
            while sum(quantidades) > qtd:
                quantidades[quantidades.index(max(quantidades))] -= 1
            gabarito = []
            for letra, quantidade in zip(letras_embaralhadas, quantidades):
                gabarito.extend([letra] * quantidade)
            random.shuffle(gabarito)
            if not tem_repeticoes_excessivas(gabarito, max_reps=2 if len(letras) == 2 else 3):
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

def salvar_gabarito(caminho, assunto="", banca="", qtd_questoes=40, letras=None):
    try:
        gabarito = gerar_gabarito_simples(qtd=qtd_questoes, letras=letras)
        instrucao = (
            f"Gere 5 questões objetivas sobre \"{assunto}\", no estilo da banca \"{banca}\", "
            "seguindo o seguinte formato:\n\n"
            "- Enunciado claro e realista, apenas diga o gabarito quando solicitado\n"
            f"- {len(letras)} alternativas ({', '.join(letras)})\n"
            "- Apenas uma correta\n"
            "- **A posição correta deve seguir, em ordem, a sequência de letras fornecida abaixo**\n"
            "- **Use essa sequência apenas para estruturar as questões**\n"
            "- **Não repita nem mencione essa sequência na resposta**\n\n"
            "Sequência de gabarito:\n"
            f"{''.join(gabarito)}\n"
        )
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(instrucao)
    except Exception as e:
        registrar_erro(e)

def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

def verificar_e_atualizar(mostrar_mensagem=False):
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
            elif mostrar_mensagem:
                messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")
    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para mais detalhes.")


def salvar():
    assunto = entry_assunto.get().strip()
    banca = entry_banca.get().strip()
    if not assunto or not banca:
        entry_assunto.configure(style="Erro.TEntry")
        entry_banca.configure(style="Erro.TEntry")
        return

    entry_assunto.configure(style="Normal.TEntry")
    entry_banca.configure(style="Normal.TEntry")

    alternativas = var_alternativas.get()
    if alternativas not in ("2", "4", "5"):
        messagebox.showwarning("Atenção", "Escolha entre 2, 4 ou 5 alternativas antes de continuar.")
        return

    letras = {
        "2": ["C", "E"],
        "4": ["A", "B", "C", "D"],
        "5": ["A", "B", "C", "D", "E"]
    }[alternativas]

    pasta = config.get("pasta_salvamento", os.getcwd()) if var_mesma_pasta.get() else filedialog.askdirectory()
    if not pasta:
        return

    config["pasta_salvamento"] = pasta
    salvar_configuracoes(config)

    nome = f"{assunto}_{banca}" if var_nome_personalizado.get() else "gabarito"
    caminho = os.path.join(pasta, nome if nome.endswith(".txt") else f"{nome}.txt")

    salvar_gabarito(
        caminho,
        assunto=assunto,
        banca=banca,
        qtd_questoes=int(spin_qtd.get()),
        letras=letras
    )

    if var_abrir_apos_salvar.get():
        webbrowser.open(pasta)

    messagebox.showinfo("Sucesso", f"Gabarito salvo em:\n{caminho}")

# ======================== UI ========================
root = ttk.Window(themename="flatly")
root.title("Gerador de Gabaritos Personalizados")
root.geometry("700x580")
root.resizable(False, False)

try:
    root.iconbitmap(resource_path("icon.ico"))
except:
    pass

try:
    bg_image = Image.open(resource_path("background.png")).resize((700, 580))
    background_image = ImageTk.PhotoImage(bg_image)
    bg_label = ttk.Label(root, image=background_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    background_image = None

style = ttk.Style()
style.configure("Glass.TFrame", background="#f0f0f0")
style.configure("Erro.TEntry", fieldbackground="#ffcccc")
style.configure("Normal.TEntry", fieldbackground="white")

frame = ttk.Frame(root, padding=20, style="Glass.TFrame")
frame.pack(padx=40, pady=30, fill="both", expand=True)
frame.columnconfigure(1, weight=1)

var_nome_personalizado = ttk.BooleanVar(value=config.get("nome_personalizado", True))
var_mesma_pasta = ttk.BooleanVar()
var_abrir_apos_salvar = ttk.BooleanVar()
var_alternativas = ttk.StringVar()

ttk.Label(frame, text="Assunto:").grid(row=0, column=0, sticky="e", pady=6)
entry_assunto = ttk.Entry(frame)
entry_assunto.grid(row=0, column=1, pady=6, sticky="we")

ttk.Label(frame, text="Banca examinadora:").grid(row=1, column=0, sticky="e", pady=6)
entry_banca = ttk.Entry(frame)
entry_banca.grid(row=1, column=1, pady=6, sticky="we")

ttk.Label(frame, text="Quantidade de questões:").grid(row=2, column=0, sticky="e", pady=6)
spin_qtd = ttk.Spinbox(frame, from_=10, to=200, width=8)
spin_qtd.grid(row=2, column=1, sticky="w", pady=6)

ttk.Label(frame, text="Número de alternativas:").grid(row=3, column=0, sticky="e", pady=6)
radio_frame = ttk.Frame(frame)
radio_frame.grid(row=3, column=1, sticky="w")
ttk.Radiobutton(radio_frame, text="2 (C/E)", variable=var_alternativas, value="2").pack(side="left", padx=5)
ttk.Radiobutton(radio_frame, text="4 (A-D)", variable=var_alternativas, value="4").pack(side="left", padx=5)
ttk.Radiobutton(radio_frame, text="5 (A-E)", variable=var_alternativas, value="5").pack(side="left", padx=5)

ttk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=var_nome_personalizado).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
ttk.Checkbutton(frame, text="Salvar na mesma pasta", variable=var_mesma_pasta).grid(row=6, column=0, columnspan=2, sticky="w", pady=2)
ttk.Checkbutton(frame, text="Abrir pasta após salvar", variable=var_abrir_apos_salvar).grid(row=7, column=0, columnspan=2, sticky="w", pady=2)

ttk.Button(frame, text="Salvar Gabarito", command=salvar).grid(row=8, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="Verificar atualização", command=lambda: verificar_e_atualizar(mostrar_mensagem=True)).grid(row=9, column=0, columnspan=2, pady=5)

versao_label = ttk.Label(root, text=f"Versão {VERSAO_ATUAL}", background="#f0f0f0")
versao_label.pack(side="bottom", anchor="w", padx=10, pady=5)

verificar_e_atualizar()
root.mainloop()