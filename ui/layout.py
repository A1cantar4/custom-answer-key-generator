import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from core.versao import VERSAO_ATUAL
from core.configuracoes import load_config
from core.atualizador import verificar_e_atualizar
from ui.estilos import aplicar_estilos
from ui.entrada import criar_campos_texto, criar_opcoes_alternativas, criar_checkbuttons
from ui.funcoes import importar_arquivo, salvar_gabarito


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
        self.root.geometry("700x700")
        self.root.resizable(False, False)

        # Ícone da janela
        try:
            self.root.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass

        # Background com imagem
        try:
            bg_image = Image.open(resource_path("assets/background.png")).resize((700, 700))
            self.background_image = ImageTk.PhotoImage(bg_image)
            bg_label = ttk.Label(self.root, image=self.background_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.background_image = None

        self.config = load_config()
        self.arquivos_importados = []

        self.style = ttk.Style()
        aplicar_estilos(self.style)

        self.setup_ui()
        verificar_e_atualizar()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20, style="Glass.TFrame")
        frame.pack(padx=40, pady=30, fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        # Variáveis de controle
        self.var_nome_personalizado = ttk.BooleanVar(value=self.config.get("nome_personalizado", True))
        self.var_mesma_pasta = ttk.BooleanVar(value=self.config.get("salvar_mesma_pasta", True))
        self.var_abrir_apos_salvar = ttk.BooleanVar(value=self.config.get("open_after_saving", False))
        self.var_preview = ttk.BooleanVar(value=self.config.get("preview", False))
        self.var_exportar_pdf = ttk.BooleanVar(value=self.config.get("exportar_pdf", False))
        self.var_alternativas = ttk.StringVar(value=str(self.config.get("last_alt_count", 5)))
        self.var_dificuldade = ttk.StringVar(value=self.config.get("modo_dificuldade", "Médio"))

        # Criação da interface
        criar_campos_texto(self, frame)
        criar_opcoes_alternativas(self, frame)
        criar_checkbuttons(self, frame)

        # Botões principais
        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=7, column=0, columnspan=2, pady=6, sticky="w")

        ttk.Button(botoes_frame, text="Importar Arquivo (.docx ou .pdf)", command=lambda: importar_arquivo(self))\
            .pack(side="left", padx=(0, 10))

        self.label_arquivos = ttk.Label(botoes_frame, text="Nenhum arquivo anexado", foreground="gray")
        self.label_arquivos.pack(side="left")

        ttk.Button(frame, text="Salvar Gabarito", command=lambda: salvar_gabarito(self))\
            .grid(row=12, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Verificar atualização", command=lambda: verificar_e_atualizar(mostrar_mensagem=True))\
            .grid(row=13, column=0, columnspan=2, pady=5)

        ttk.Label(self.root, text=f"Versão {VERSAO_ATUAL}", font=("Segoe UI", 9))\
            .pack(side="bottom", anchor="w", padx=10, pady=5)

        # Restaura valores salvos anteriormente
        self.entry_assunto.insert(0, self.config.get("last_used_subject", ""))
        self.entry_banca.insert(0, self.config.get("last_used_board", ""))
        self.spin_qtd.insert(0, self.config.get("last_question_count", 40))

        # Botão discreto para reabrir configuração
        ttk.Button(self.root, text="↺ Reabrir última Configuração", bootstyle="link", command=self.reabrir_ultima_config)\
            .place(x=430, y=594)

    def reabrir_ultima_config(self):
        try:
            config = load_config()

            self.entry_assunto.delete(0, 'end')
            self.entry_assunto.insert(0, config.get("last_used_subject", ""))

            self.entry_banca.delete(0, 'end')
            self.entry_banca.insert(0, config.get("last_used_board", ""))

            self.spin_qtd.delete(0, 'end')
            self.spin_qtd.insert(0, config.get("last_question_count", 40))

            self.var_alternativas.set(str(config.get("last_alt_count", 5)))
            self.var_nome_personalizado.set(config.get("nome_personalizado", True))
            self.var_mesma_pasta.set(config.get("salvar_mesma_pasta", True))
            self.var_abrir_apos_salvar.set(config.get("open_after_saving", False))
            self.var_exportar_pdf.set(config.get("exportar_pdf", False))
            self.var_preview.set(config.get("preview", False))
            self.var_dificuldade.set(config.get("modo_dificuldade", "Médio"))

            messagebox.showinfo("Configuração carregada", "A última configuração foi restaurada com sucesso.")
        except Exception as e:
            from core.atualizador import registrar_erro
            registrar_erro(e)
            messagebox.showerror("Erro", "Erro ao tentar restaurar a última configuração.")
