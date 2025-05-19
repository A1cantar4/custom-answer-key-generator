import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def criar_campos_texto(app, frame):
    """
    Cria os campos de entrada principais: Assunto, Banca, Matéria, Quantidade de questões.
    """
    ttk.Label(frame, text="Assunto:").grid(row=0, column=0, sticky="e", pady=6)
    app.entry_assunto = ttk.Entry(frame)
    app.entry_assunto.grid(row=0, column=1, pady=6, sticky="we")

    ttk.Label(frame, text="Banca examinadora:").grid(row=1, column=0, sticky="e", pady=6)
    app.entry_banca = ttk.Entry(frame)
    app.entry_banca.grid(row=1, column=1, pady=6, sticky="we")

    ttk.Label(frame, text="Matéria (opcional):").grid(row=2, column=0, sticky="e", pady=6)
    app.entry_materia = ttk.Entry(frame)
    app.entry_materia.grid(row=2, column=1, pady=6, sticky="we")

    ttk.Label(frame, text="Quantidade de questões:").grid(row=3, column=0, sticky="e", pady=6)
    app.spin_qtd = ttk.Spinbox(frame, from_=10, to=200, width=8)
    app.spin_qtd.grid(row=3, column=1, sticky="w", pady=6)


def criar_opcoes_alternativas(app, frame):
    """
    Cria os radio buttons para número de alternativas e combobox de dificuldade.
    """
    app.var_alternativas = ttk.StringVar(value="5")
    app.var_dificuldade = ttk.StringVar(value="Médio")

    ttk.Label(frame, text="Número de alternativas:").grid(row=4, column=0, sticky="e", pady=6)
    radio_frame = ttk.Frame(frame)
    radio_frame.grid(row=4, column=1, sticky="w")
    for val, texto in [("2", "2 (C/E)"), ("4", "4 (A-D)"), ("5", "5 (A-E)")]:
        ttk.Radiobutton(radio_frame, text=texto, variable=app.var_alternativas, value=val).pack(side="left", padx=5)

    ttk.Label(frame, text="Dificuldade:").grid(row=5, column=0, sticky="e", pady=6)
    dificuldade_combo = ttk.Combobox(
        frame,
        textvariable=app.var_dificuldade,
        values=["Fácil", "Médio", "Difícil", "Modo Extremo"],
        state="readonly"
    )
    dificuldade_combo.grid(row=5, column=1, sticky="w", pady=6)


def criar_checkbuttons(app, frame):
    """
    Cria checkboxes com base nas variáveis da instância.
    """
    app.var_nome_personalizado = ttk.BooleanVar(value=True)
    app.var_mesma_pasta = ttk.BooleanVar(value=True)
    app.var_abrir_apos_salvar = ttk.BooleanVar(value=False)
    app.var_preview = ttk.BooleanVar(value=False)
    app.var_exportar_pdf = ttk.BooleanVar(value=False)

    ttk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=app.var_nome_personalizado)\
        .grid(row=6, column=0, columnspan=2, sticky="w", pady=2)

    ttk.Checkbutton(frame, text="Salvar na mesma pasta", variable=app.var_mesma_pasta)\
        .grid(row=8, column=0, columnspan=2, sticky="w", pady=2)

    ttk.Checkbutton(frame, text="Abrir pasta após salvar", variable=app.var_abrir_apos_salvar)\
        .grid(row=9, column=0, columnspan=2, sticky="w", pady=2)

    ttk.Checkbutton(frame, text="Visualizar antes de salvar", variable=app.var_preview)\
        .grid(row=10, column=0, columnspan=2, sticky="w", pady=2)

    ttk.Checkbutton(frame, text="Exportar também como PDF", variable=app.var_exportar_pdf)\
        .grid(row=11, column=0, columnspan=2, sticky="w", pady=2)
