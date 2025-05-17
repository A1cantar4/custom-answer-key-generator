import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import webbrowser

from core.version import VERSAO_ATUAL
from core.generator import gerar_gabarito_balanceado
from core.updater import verificar_e_atualizar, registrar_erro
from core.settings import load_config, save_config
from core.reader import extrair_texto_docx, extrair_texto_pdf

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

        self.config = load_config()
        self.arquivos_importados = []
        self.setup_ui()
        verificar_e_atualizar()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("flatly")
        style.configure("Glass.TFrame", background="#ffffff", relief="flat")
        style.configure("TEntry", fieldbackground="#ffffff", borderwidth=1)
        style.configure("TCheckbutton", background="#ffffff")
        style.configure("TButton", padding=6, relief="flat")
        style.configure("Erro.TEntry", fieldbackground="#ffcccc")
        style.configure("Normal.TEntry", fieldbackground="white")

        frame = ttk.Frame(self.root, padding=20, style="Glass.TFrame")
        frame.pack(padx=40, pady=30, fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        self.var_nome_personalizado = ttk.BooleanVar(value=self.config.get("nome_personalizado", True))
        self.var_mesma_pasta = ttk.BooleanVar()
        self.var_abrir_apos_salvar = ttk.BooleanVar(value=self.config.get("open_after_saving", False))
        self.var_alternativas = ttk.StringVar(value=str(self.config.get("last_alt_count", 4)))

        ttk.Label(frame, text="Assunto:").grid(row=0, column=0, sticky="e", pady=6)
        self.entry_assunto = ttk.Entry(frame)
        self.entry_assunto.grid(row=0, column=1, pady=6, sticky="we")

        ttk.Label(frame, text="Banca examinadora:").grid(row=1, column=0, sticky="e", pady=6)
        self.entry_banca = ttk.Entry(frame)
        self.entry_banca.grid(row=1, column=1, pady=6, sticky="we")

        ttk.Label(frame, text="Matéria (opcional):").grid(row=2, column=0, sticky="e", pady=6)
        self.entry_materia = ttk.Entry(frame)
        self.entry_materia.grid(row=2, column=1, pady=6, sticky="we")

        ttk.Label(frame, text="Quantidade de questões:").grid(row=3, column=0, sticky="e", pady=6)
        self.spin_qtd = ttk.Spinbox(frame, from_=10, to=200, width=8)
        self.spin_qtd.grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(frame, text="Número de alternativas:").grid(row=4, column=0, sticky="e", pady=6)
        radio_frame = ttk.Frame(frame)
        radio_frame.grid(row=4, column=1, sticky="w")
        for val, texto in [("2", "2 (C/E)"), ("4", "4 (A-D)"), ("5", "5 (A-E)")]:
            ttk.Radiobutton(radio_frame, text=texto, variable=self.var_alternativas, value=val).pack(side="left", padx=5)

        ttk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=self.var_nome_personalizado).grid(row=5, column=0, columnspan=2, sticky="w", pady=2)

        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=6, sticky="w")

        ttk.Button(botoes_frame, text="Importar Arquivo (.docx ou .pdf)", command=self.importar_arquivo).pack(side="left", padx=(0, 10))
        self.label_arquivos = ttk.Label(botoes_frame, text="Nenhum arquivo anexado", foreground="gray")
        self.label_arquivos.pack(side="left")

        ttk.Checkbutton(frame, text="Salvar na mesma pasta", variable=self.var_mesma_pasta).grid(row=7, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Abrir pasta após salvar", variable=self.var_abrir_apos_salvar).grid(row=8, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Button(frame, text="Salvar Gabarito", command=self.salvar).grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Verificar atualização", command=lambda: verificar_e_atualizar(mostrar_mensagem=True)).grid(row=10, column=0, columnspan=2, pady=5)

        ttk.Label(self.root, text=f"Versão {VERSAO_ATUAL}", font=("Segoe UI", 9)).pack(side="bottom", anchor="w", padx=10, pady=5)

        self.entry_assunto.insert(0, self.config.get("last_used_subject", ""))
        self.spin_qtd.insert(0, self.config.get("last_question_count", 40))

    def importar_arquivo(self):
        caminhos = filedialog.askopenfilenames(filetypes=[("Documentos", "*.pdf *.docx")])
        self.arquivos_importados = list(caminhos)

        if self.arquivos_importados:
            nomes = [os.path.basename(p) for p in self.arquivos_importados]
            texto = "Arquivos: " + ", ".join(nomes)
            self.label_arquivos.config(text=texto, foreground="black")
            self.entry_assunto.delete(0, 'end')
            self.entry_assunto.insert(0, "[extraído dos arquivos anexados]")
        else:
            self.label_arquivos.config(text="Nenhum arquivo anexado", foreground="gray")

    def salvar(self):
        assunto = self.entry_assunto.get().strip()
        banca = self.entry_banca.get().strip()
        materia = self.entry_materia.get().strip()

        if not banca:
            self.entry_banca.configure(style="Erro.TEntry")
            return
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

        pasta = (
            self.config.get("pasta_salvamento", os.getcwd())
            if self.var_mesma_pasta.get()
            else filedialog.askdirectory()
        )
        if not pasta:
            return

        nome = f"{assunto}_{banca}" if self.var_nome_personalizado.get() else "gabarito"
        caminho = os.path.join(pasta, nome if nome.endswith(".txt") else f"{nome}.txt")

        try:
            gabarito = gerar_gabarito_balanceado(
                qtd=int(self.spin_qtd.get()),
                letras=letras
            )

            conteudo_extra = ""
            for caminho_importado in getattr(self, "arquivos_importados", []):
                if caminho_importado.lower().endswith(".docx"):
                    conteudo_extra += f"\n\n[Conteúdo do arquivo {os.path.basename(caminho_importado)}]:\n"
                    conteudo_extra += extrair_texto_docx(caminho_importado)
                elif caminho_importado.lower().endswith(".pdf"):
                    conteudo_extra += f"\n\n[Conteúdo do arquivo {os.path.basename(caminho_importado)}]:\n"
                    conteudo_extra += extrair_texto_pdf(caminho_importado)

            if conteudo_extra:
                assunto = "os conteúdos dos documentos anexados"
                if materia:
                    assunto += f", na matéria {materia}"

            instrucao = (
                f"Gere de 5 em 5 questões objetivas até finalizar as alternativas sobre \"{assunto}\", no estilo da banca \"{banca}\", "
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
                if conteudo_extra:
                    f.write("\n\nConteúdo adicional extraído dos documentos:\n")
                    f.write(conteudo_extra)

            if self.var_abrir_apos_salvar.get():
                webbrowser.open(pasta)

            messagebox.showinfo("Sucesso", f"Gabarito salvo em:\n{caminho}")

        except Exception as e:
            registrar_erro(e)

        self.config.update({
            "pasta_salvamento": pasta,
            "nome_personalizado": self.var_nome_personalizado.get(),
            "last_used_subject": assunto,
            "last_question_count": int(self.spin_qtd.get()),
            "last_alt_count": int(alternativas),
            "open_after_saving": self.var_abrir_apos_salvar.get()
        })
        save_config(self.config)
