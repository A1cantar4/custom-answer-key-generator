import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
import sys
import requests

VERSAO_ATUAL = "1.1.0"
URL_VERSAO = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/versao.txt"
URL_SCRIPT = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/app.py"

def verificar_atualizacao():
    try:
        r = requests.get(URL_VERSAO)
        if r.status_code == 200:
            versao_disponivel = r.text.strip()
            if versao_disponivel != VERSAO_ATUAL:
                return versao_disponivel
    except:
        pass
    return None

def atualizar_script():
    try:
        r = requests.get(URL_SCRIPT)
        if r.status_code == 200:
            caminho = os.path.abspath(__file__)
            with open(caminho, "wb") as f:
                f.write(r.content)
            messagebox.showinfo("Atualizado", "Aplicativo atualizado com sucesso! Reinicie o programa.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

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

def salvar_gabarito(caminho, apenas_gabarito=False):
    assunto = entry_assunto.get().strip()
    if not assunto:
        messagebox.showwarning("Aviso", "Digite o nome do assunto.")
        return
    try:
        qtd = int(spin_qtd.get())
        gabarito = gerar_gabarito_simples(qtd)
        random.shuffle(gabarito)
        if apenas_gabarito:
            texto = "\n".join(f"{i+1}. {g}" for i, g in enumerate(gabarito))
        else:
            frase_instrucao = (
                f"Gere {qtd} questões objetivas sobre \"{assunto}\", difíceis e bem elaboradas, no estilo da banca IBAM, seguindo o seguinte formato:\n\n"
                "- Enunciado claro e realista, apenas diga o gabarito quando solicitado\n"
                "- Quatro alternativas (A, B, C, D)\n"
                "- Apenas uma correta\n"
                "- **A posição correta deve seguir, em ordem, a sequência de letras fornecida abaixo**\n"
                "- **Use essa sequência apenas para estruturar as questões**\n"
                "- **Não repita nem mencione essa sequência na resposta**\n\n"
                "Sequência de gabarito:\n"
                f"{''.join(gabarito)}\n"
            )
            texto = frase_instrucao
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(texto)
        messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{caminho}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        assunto = entry_assunto.get().strip()
        if var_nome_personalizado.get() and assunto:
            nome_base = assunto.replace(" ", "_")
        else:
            nome_base = "gabarito"
        if var_gabarito.get():
            caminho = os.path.join(pasta, f"{nome_base}_apenas_gabarito.txt")
            salvar_gabarito(caminho, apenas_gabarito=True)
        caminho_instrucao = os.path.join(pasta, f"{nome_base}.txt")
        salvar_gabarito(caminho_instrucao)

def salvar_pasta_atual():
    pasta_atual = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    assunto = entry_assunto.get().strip()
    if var_nome_personalizado.get() and assunto:
        nome_base = assunto.replace(" ", "_")
    else:
        nome_base = "gabarito"
    if var_gabarito.get():
        salvar_gabarito(os.path.join(pasta_atual, f"{nome_base}_apenas_gabarito.txt"), apenas_gabarito=True)
    salvar_gabarito(os.path.join(pasta_atual, f"{nome_base}.txt"))

def validar_assunto(*args):
    assunto = entry_assunto.get().strip()
    if not assunto:
        entry_assunto.config(bg='misty rose')
    else:
        entry_assunto.config(bg='white')

# Interface Tkinter
root = tk.Tk()
root.title("Gerador de Gabaritos IBAM")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

font_style = ("Helvetica", 11)

label_assunto = tk.Label(frame, text="Assunto:", font=font_style)
label_assunto.grid(row=0, column=0, padx=5, pady=5, sticky='e')

entry_assunto = tk.Entry(frame, width=35, font=font_style)
entry_assunto.grid(row=0, column=1, padx=5, pady=5)
entry_assunto.bind("<KeyRelease>", validar_assunto)

label_qtd = tk.Label(frame, text="Qtd questões:", font=font_style)
label_qtd.grid(row=1, column=0, padx=5, pady=5, sticky='e')

spin_qtd = tk.Spinbox(frame, from_=1, to=200, width=5, font=font_style)
spin_qtd.grid(row=1, column=1, sticky='w', padx=5, pady=5)

var_gabarito = tk.BooleanVar()
check_gabarito = tk.Checkbutton(frame, text="Salvar apenas gabarito", variable=var_gabarito, font=font_style)
check_gabarito.grid(row=2, column=0, columnspan=2, pady=5)

var_nome_personalizado = tk.BooleanVar()
check_nome_personalizado = tk.Checkbutton(frame, text="Salvar com nome personalizado", variable=var_nome_personalizado, font=font_style)
check_nome_personalizado.grid(row=3, column=0, columnspan=2, pady=5)

btn_salvar_outro = tk.Button(frame, text="Salvar em outra pasta", font=font_style, command=escolher_pasta)
btn_salvar_outro.grid(row=4, column=0, padx=5, pady=10)

btn_salvar_atual = tk.Button(frame, text="Salvar na pasta atual", font=font_style, command=salvar_pasta_atual)
btn_salvar_atual.grid(row=4, column=1, padx=5, pady=10)

label_versao = tk.Label(root, text=f"Versão {VERSAO_ATUAL}", font=("Arial", 9), anchor='e')
label_versao.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

# Checar atualização
nova = verificar_atualizacao()
if nova:
    if messagebox.askyesno("Atualização", f"Nova versão disponível ({nova}). Deseja atualizar?"):
        atualizar_script()

root.mainloop()
