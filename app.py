import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import os
import sys
import json
import traceback
import webbrowser

# Run Compilação .EXE
# & "C:\Users\falca\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe" --noconfirm --onefile --windowed app.py

# Atualizar versão antes de Compilar e dar Push

# ======================== CONFIGURAÇÕES ========================
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
def salvar_gabarito_em_lote(pasta, qtd_arquivos):
    try:
        for i in range(qtd_arquivos):
            salvar_gabarito(
                os.path.join(pasta, f"gabarito_{i+1}.txt"),
                apenas_gabarito=var_apenas_gabarito.get(),
                assunto=entry_assunto.get().strip(),
                qtd_questoes=int(spin_qtd.get())
            )
        abrir_pasta(pasta)
        messagebox.showinfo("Sucesso", f"{qtd_arquivos} gabaritos salvos em:\n{pasta}")
    except Exception as e:
        registrar_erro(e)

def salvar_gabarito(caminho, apenas_gabarito=False, assunto="", qtd_questoes=40):
    try:
        gabarito = gerar_gabarito_simples(qtd=qtd_questoes)
        if apenas_gabarito:
            texto = '\n'.join([f"{i+1}. {letra}" for i, letra in enumerate(gabarito)])
            with open(os.path.join(os.path.dirname(caminho), "apenas_gabarito.txt"), "w") as f:
                f.write(texto)
        else:
            instrucao = (
                f"Gere 5 questões objetivas sobre \"{assunto}\", difíceis e bem elaboradas, no estilo da banca IBAM, "
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

def abrir_pasta(pasta):
    try:
        webbrowser.open(pasta)
    except Exception as e:
        registrar_erro(e)

# ======================== ERROS ========================
def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

# ======================== UI ========================
def atualizar_validacao_assunto(event=None):
    if not entry_assunto.get().strip():
        entry_assunto.config(bg="#ffcccc")
    else:
        entry_assunto.config(bg="white" if not modo_escuro.get() else "#333333")

def alternar_tema():
    tema = "dark" if modo_escuro.get() else "light"
    aplicar_tema(tema)
    config["tema"] = tema
    salvar_configuracoes(config)

def aplicar_tema(tema):
    bg = "#333333" if tema == "dark" else "#ffffff"
    fg = "#ffffff" if tema == "dark" else "#000000"
    btn_bg = "#444444" if tema == "dark" else "#f0f0f0"

    root.configure(bg=bg)
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=bg, fg=fg)
        elif isinstance(widget, (tk.Button, tk.Checkbutton)):
            widget.configure(bg=btn_bg, fg=fg)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg="#555555" if tema == "dark" else "white", fg=fg)

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if not pasta:
        return

    if var_em_lote.get():
        qtd = int(spin_lote.get())
        salvar_gabarito_em_lote(pasta, qtd)
    else:
        nome = entry_assunto.get().strip() if var_nome_personalizado.get() else "gabarito.txt"
        caminho = os.path.join(pasta, nome if nome.endswith(".txt") else f"{nome}.txt")
        salvar_gabarito(
            caminho,
            apenas_gabarito=var_apenas_gabarito.get(),
            assunto=entry_assunto.get().strip(),
            qtd_questoes=int(spin_qtd.get())
        )
        abrir_pasta(pasta)
        messagebox.showinfo("Sucesso", f"Gabarito salvo em:\n{caminho}")

def atualizar_estado_lote():
    if var_em_lote.get():
        spin_lote.config(state="normal")
    else:
        spin_lote.config(state="disabled")

def atualizar_nome_personalizado():
    config["nome_personalizado"] = var_nome_personalizado.get()
    salvar_configuracoes(config)

# ======================== JANELA ========================
root = tk.Tk()
root.title("Gerador de Gabaritos IBAM")
root.geometry("460x400")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

modo_escuro = tk.BooleanVar(value=config.get("tema") == "dark")
var_nome_personalizado = tk.BooleanVar(value=config.get("nome_personalizado", True))
var_apenas_gabarito = tk.BooleanVar()
var_em_lote = tk.BooleanVar()

# Entrada assunto
tk.Label(frame, text="Assunto:").grid(row=0, column=0, sticky='e')
entry_assunto = tk.Entry(frame, width=35)
entry_assunto.grid(row=0, column=1, columnspan=2, sticky='w')
entry_assunto.bind("<KeyRelease>", atualizar_validacao_assunto)

# Questões
tk.Label(frame, text="Quantidade de questões:").grid(row=1, column=0, sticky='e')
spin_qtd = tk.Spinbox(frame, from_=10, to=200, width=5)
spin_qtd.grid(row=1, column=1, sticky='w')

# Opções
tk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=var_nome_personalizado, command=atualizar_nome_personalizado).grid(row=2, column=0, columnspan=2, sticky='w')
tk.Checkbutton(frame, text="Salvar apenas gabarito", variable=var_apenas_gabarito).grid(row=3, column=0, columnspan=2, sticky='w')
tk.Checkbutton(frame, text="Gerar múltiplos gabaritos", variable=var_em_lote, command=atualizar_estado_lote).grid(row=4, column=0, columnspan=2, sticky='w')

tk.Label(frame, text="Qtd arquivos:").grid(row=5, column=0, sticky='e')
spin_lote = tk.Spinbox(frame, from_=2, to=100, width=5, state="disabled")
spin_lote.grid(row=5, column=1, sticky='w')

# Botões
tk.Button(frame, text="Salvar gabarito", command=escolher_pasta).grid(row=6, column=0, columnspan=3, pady=10)

# Tema
tk.Checkbutton(frame, text="Modo Escuro", variable=modo_escuro, command=alternar_tema).grid(row=7, column=0, columnspan=2, sticky='w')

# Versão
tk.Label(root, text="Versão 1.1.2", anchor='se').pack(side='bottom', fill='x', pady=5)

# Aplicar tema
aplicar_tema("dark" if modo_escuro.get() else "light")
atualizar_validacao_assunto()

root.mainloop()
