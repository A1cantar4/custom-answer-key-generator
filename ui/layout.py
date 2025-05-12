import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import webbrowser

from core.config import carregar_configuracoes, salvar_configuracoes
from core.generator import gerar_gabarito_balanceado
from core.updater import verificar_e_atualizar, registrar_erro

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GabaritoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Gabaritos Personalizados")
        self.root.geometry("700x580")
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass

        try:
            bg_image = Image.open(resource_path("assets/background.png")).resize((700, 580))
            self.background_image = ImageTk.PhotoImage(bg_image)
            bg_label = ttk.Label(self.root, image=self.background_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.background_image = None

        self.config = carregar_configuracoes()
        self.setup_ui()

        verificar_e_atualizar()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Glass.TFrame", background="#f0f0f0")
        style.configure("Erro.TEntry", fieldbackground="#ffcccc")
        style.configure("Normal.TEntry", fieldbackground="white")

        frame = ttk.Frame(self.root, padding=20, style="Glass.TFrame")
        frame.pack(padx=40, pady=30, fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        self.var_nome_personalizado = ttk.BooleanVar(value=self.config.get("nome_personalizado", True))
        self.var_mesma_pasta = ttk.BooleanVar()
        self.var_abrir_apos_salvar = ttk.BooleanVar()
        self.var_alternativas = ttk.StringVar()

        ttk.Label(frame, text="Assunto:").grid(row=0, column=0, sticky="e", pady=6)
        self.entry_assunto = ttk.Entry(frame)
        self.entry_assunto.grid(row=0, column=1, pady=6, sticky="we")

        ttk.Label(frame, text="Banca examinadora:").grid(row=1, column=0, sticky="e", pady=6)
        self.entry_banca = ttk.Entry(frame)
        self.entry_banca.grid(row=1, column=1, pady=6, sticky="we")

        ttk.Label(frame, text="Quantidade de questões:").grid(row=2, column=0, sticky="e", pady=6)
        self.spin_qtd = ttk.Spinbox(frame, from_=10, to=200, width=8)
        self.spin_qtd.grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(frame, text="Número de alternativas:").grid(row=3, column=0, sticky="e", pady=6)
        radio_frame = ttk.Frame(frame)
        radio_frame.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(radio_frame, text="2 (C/E)", variable=self.var_alternativas, value="2").pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="4 (A-D)", variable=self.var_alternativas, value="4").pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="5 (A-E)", variable=self.var_alternativas, value="5").pack(side="left", padx=5)

        ttk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=self.var_nome_personalizado).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Salvar na mesma pasta", variable=self.var_mesma_pasta).grid(row=6, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Abrir pasta após salvar", variable=self.var_abrir_apos_salvar).grid(row=7, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Button(frame, text="Salvar Gabarito", command=self.salvar).grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Verificar atualização", command=lambda: verificar_e_atualizar(mostrar_mensagem=True)).grid(row=9, column=0, columnspan=2, pady=5)

        versao_label = ttk.Label(self.root, text="Versão 1.3.5", background="#f0f0f0")
        versao_label.pack(side="bottom", anchor="w", padx=10, pady=5)

    def salvar(self):
        assunto = self.entry_assunto.get().strip()
        banca = self.entry_banca.get().strip()

        if not assunto or not banca:
            self.entry_assunto.configure(style="Erro.TEntry")
            self.entry_banca.configure(style="Erro.TEntry")
            return

        self.entry_assunto.configure(style="Normal.TEntry")
        self.entry_banca.configure(style="Normal.TEntry")

        alternativas = self.var_alternativas.get()
        if alternativas not in ("2", "4", "5"):
            messagebox.showwarning("Atenção", "Escolha entre 2, 4 ou 5 alternativas antes de continuar.")
            return

        letras = {
            "2": ["C", "E"],
            "4": ["A", "B", "C", "D"],
            "5": ["A", "B", "C", "D", "E"]
        }[alternativas]

        pasta = self.config.get("pasta_salvamento", os.getcwd()) if self.var_mesma_pasta.get() else filedialog.askdirectory()
        if not pasta:
            return

        self.config["pasta_salvamento"] = pasta
        self.config["nome_personalizado"] = self.var_nome_personalizado.get()
        salvar_configuracoes(self.config)

        nome = f"{assunto}_{banca}" if self.var_nome_personalizado.get() else "gabarito"
        caminho = os.path.join(pasta, nome if nome.endswith(".txt") else f"{nome}.txt")

        try:
            gabarito = gerar_gabarito_balanceado(qtd=int(self.spin_qtd.get()), letras=letras)
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

            if self.var_abrir_apos_salvar.get():
                webbrowser.open(pasta)

            messagebox.showinfo("Sucesso", f"Gabarito salvo em:\n{caminho}")

        except Exception as e:
            registrar_erro(e)