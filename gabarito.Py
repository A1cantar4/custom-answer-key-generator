import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os
import sys

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

def validar_assunto(event=None):
    assunto = entry_assunto.get().strip()
    if not assunto:
        entry_assunto.config(bg="#ffcccc")
    else:
        entry_assunto.config(bg="white")

def salvar_gabarito(caminho_base):
    assunto = entry_assunto.get().strip()
    qtd_questoes = int(spin_qtd.get())
    nome_personalizado = var_nome_personalizado.get()
    gerar_apenas_gabarito = var_apenas_gabarito.get()

    if not assunto:
        messagebox.showwarning("Aviso", "Digite o nome do assunto.")
        return

    try:
        gabarito = gerar_gabarito_simples(qtd=qtd_questoes)
        random.shuffle(gabarito)

        # Salvar arquivo principal com instruções
        frase_instrucao = (
            f"Gere 5 questões objetivas sobre \"{assunto}\", difíceis e bem elaboradas, no estilo da banca IBAM, seguindo o seguinte formato:\n\n"
            "- Enunciado claro e realista, apenas diga o gabarito quando solicitado\n"
            "- Quatro alternativas (A, B, C, D)\n"
            "- Apenas uma correta\n"
            "- **A posição correta deve seguir, em ordem, a sequência de letras fornecida abaixo**\n"
            "- **Use essa sequência apenas para estruturar as questões**\n"
            "- **Não repita nem mencione essa sequência na resposta**\n\n"
            "Sequência de gabarito:\n"
        )
        texto_instrucao = f"{frase_instrucao}{''.join(gabarito)}\n"

        with open(caminho_base, "w") as f:
            f.write(texto_instrucao)

        # Salvar gabarito puro (opcional)
        if gerar_apenas_gabarito:
            pasta = os.path.dirname(caminho_base)
            caminho_gabarito = os.path.join(pasta, "apenas_gabarito.txt")
            texto_gabarito = "\n".join([f"{i+1}. {gabarito[i]}" for i in range(len(gabarito))])
            with open(caminho_gabarito, "w") as f2:
                f2.write(texto_gabarito)

        messagebox.showinfo("Sucesso", f"Arquivo(s) salvo(s) em:\n{os.path.dirname(caminho_base)}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        nome_arquivo = "gabarito.txt"
        if var_nome_personalizado.get():
            nome_base = entry_assunto.get().strip().replace(" ", "_")
            nome_arquivo = f"{nome_base}.txt"
        caminho = os.path.join(pasta, nome_arquivo)
        salvar_gabarito(caminho)

def salvar_pasta_atual():
    if getattr(sys, 'frozen', False):
        pasta_atual = os.path.dirname(sys.executable)
    else:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))

    nome_arquivo = "gabarito.txt"
    if var_nome_personalizado.get():
        nome_base = entry_assunto.get().strip().replace(" ", "_")
        nome_arquivo = f"{nome_base}.txt"
    caminho = os.path.join(pasta_atual, nome_arquivo)
    salvar_gabarito(caminho)

root = tk.Tk()
root.title("Gerador de Gabaritos IBAM")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

font_style = ("Helvetica", 11)

# Campo de Assunto
label_assunto = tk.Label(frame, text="Assunto:", font=font_style)
label_assunto.grid(row=0, column=0, padx=5, pady=5, sticky='e')

entry_assunto = tk.Entry(frame, width=35, font=font_style)
entry_assunto.grid(row=0, column=1, padx=5, pady=5)
entry_assunto.bind("<KeyRelease>", validar_assunto)

# Spinbox para quantidade de questões
label_qtd = tk.Label(frame, text="Qtd. Questões:", font=font_style)
label_qtd.grid(row=1, column=0, padx=5, pady=5, sticky='e')

spin_qtd = tk.Spinbox(frame, from_=10, to=100, width=5, font=font_style)
spin_qtd.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# Checkbutton para nome personalizado
var_nome_personalizado = tk.BooleanVar()
check_nome_personalizado = tk.Checkbutton(
    frame, text="Salvar com nome baseado no assunto",
    variable=var_nome_personalizado, font=font_style)
check_nome_personalizado.grid(row=2, column=0, columnspan=2, sticky='w')

# Checkbutton para salvar apenas gabarito adicional
var_apenas_gabarito = tk.BooleanVar(value=False)
check_apenas_gabarito = tk.Checkbutton(
    frame, text="Salvar também um arquivo apenas com o gabarito",
    variable=var_apenas_gabarito, font=font_style)
check_apenas_gabarito.grid(row=3, column=0, columnspan=2, sticky='w')

# Botões
btn_salvar_outro = tk.Button(frame, text="Salvar em outra pasta", font=font_style, command=escolher_pasta)
btn_salvar_outro.grid(row=5, column=0, padx=5, pady=10)

btn_salvar_atual = tk.Button(frame, text="Salvar na pasta atual", font=font_style, command=salvar_pasta_atual)
btn_salvar_atual.grid(row=5, column=1, padx=5, pady=10)

root.mainloop()
