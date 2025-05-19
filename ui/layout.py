# imports permanecem os mesmos
import re
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
from core.exportador import salvar_pdf


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
        self.root.geometry("700x700") # <--- Lembrar de mudar linha 40
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass

        try:
            bg_image = Image.open(resource_path("assets/background.png")).resize((700, 700)) # <-- Mudar quando mudar acima
            self.background_image = ImageTk.PhotoImage(bg_image)
            bg_label = ttk.Label(self.root, image=self.background_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.background_image = None

        self.config = load_config()
        self.arquivos_importados = []
        self.setup_ui()
        verificar_e_atualizar()

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
            registrar_erro(e)
            messagebox.showerror("Erro", "Erro ao tentar restaurar a última configuração.")


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
        self.var_mesma_pasta = ttk.BooleanVar(value=self.config.get("salvar_mesma_pasta", True))
        self.var_abrir_apos_salvar = ttk.BooleanVar(value=self.config.get("open_after_saving", False))
        self.var_preview = ttk.BooleanVar(value=self.config.get("preview", False))
        self.var_exportar_pdf = ttk.BooleanVar(value=self.config.get("exportar_pdf", False))
        self.var_alternativas = ttk.StringVar(value=str(self.config.get("last_alt_count", 5)))
        self.var_dificuldade = ttk.StringVar(value=self.config.get("modo_dificuldade", "Médio"))

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

        ttk.Label(frame, text="Dificuldade:").grid(row=5, column=0, sticky="e", pady=6)
        dificuldade_combo = ttk.Combobox(frame, textvariable=self.var_dificuldade, values=["Fácil", "Médio", "Difícil", "Modo Extremo"], state="readonly")
        dificuldade_combo.grid(row=5, column=1, sticky="w", pady=6)

        ttk.Checkbutton(frame, text="Salvar com nome do Assunto", variable=self.var_nome_personalizado).grid(row=6, column=0, columnspan=2, sticky="w", pady=2)

        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=7, column=0, columnspan=2, pady=6, sticky="w")

        ttk.Button(botoes_frame, text="Importar Arquivo (.docx ou .pdf)", command=self.importar_arquivo).pack(side="left", padx=(0, 10))
        self.label_arquivos = ttk.Label(botoes_frame, text="Nenhum arquivo anexado", foreground="gray")
        self.label_arquivos.pack(side="left")

        ttk.Checkbutton(frame, text="Salvar na mesma pasta", variable=self.var_mesma_pasta).grid(row=8, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Abrir pasta após salvar", variable=self.var_abrir_apos_salvar).grid(row=9, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Visualizar antes de salvar", variable=self.var_preview).grid(row=10, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Exportar também como PDF", variable=self.var_exportar_pdf).grid(row=11, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Button(frame, text="Salvar Gabarito", command=self.salvar).grid(row=12, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Verificar atualização", command=lambda: verificar_e_atualizar(mostrar_mensagem=True)).grid(row=13, column=0, columnspan=2, pady=5)

        ttk.Label(self.root, text=f"Versão {VERSAO_ATUAL}", font=("Segoe UI", 9)).pack(side="bottom", anchor="w", padx=10, pady=5)

        # Restaura últimos valores usados
        self.entry_assunto.insert(0, self.config.get("last_used_subject", ""))
        self.entry_banca.insert(0, self.config.get("last_used_board", ""))
        self.spin_qtd.insert(0, self.config.get("last_question_count", 40))

        # Botão discreto para reabrir última configuração
        ttk.Button(self.root, text="↺ Reabrir última Configuração", bootstyle="link", command=self.reabrir_ultima_config)\
            .place(x=430, y=594)
        
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
        qtd = self.spin_qtd.get().strip()
        alternativas = self.var_alternativas.get().strip()

        campos_obrigatorios = {
            "assunto": assunto,
            "banca": banca,
            "qtd": qtd,
            "alternativas": alternativas
        }

        campos_validos = True
        for campo, valor in campos_obrigatorios.items():
            if not valor or (campo == "qtd" and not valor.isdigit()):
                getattr(self, f"entry_{campo}" if campo in ["assunto", "banca"] else "spin_qtd").configure(style="Erro.TEntry")
                campos_validos = False
            else:
                getattr(self, f"entry_{campo}" if campo in ["assunto", "banca"] else "spin_qtd").configure(style="Normal.TEntry")

        if not campos_validos:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios corretamente.")
            return

        letras = {
            "2": ["C", "E"],
            "4": ["A", "B", "C", "D"],
            "5": ["A", "B", "C", "D", "E"]
        }[alternativas]

        # Garantir nome de arquivo válido
        nome_base = f"{assunto}_{banca}" if self.var_nome_personalizado.get() else "gabarito"
        nome_base = re.sub(r'[^a-zA-Z0-9_\- ]', '', nome_base).strip().replace(" ", "_")
        nome_arquivo = f"{nome_base}.txt"

        # Pasta de salvamento
        pasta = os.path.abspath(".") if self.var_mesma_pasta.get() else filedialog.askdirectory()
        if not pasta:
            return
        caminho = os.path.join(pasta, nome_arquivo)

        if os.path.exists(caminho):
            if not messagebox.askyesno("Arquivo existente", f"O arquivo '{nome_arquivo}' já existe. Deseja substituir?"):
                return

        # Geração do gabarito
        try:
            gabarito = gerar_gabarito_balanceado(
                qtd=int(qtd),
                letras=letras
            )
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Erro ao gerar o gabarito.")
            return

        # Extração de conteúdo adicional dos arquivos
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

        # Formatar sequência
        gabarito_enumerado = "\n".join(f"{i+1}. {letra}" for i, letra in enumerate(gabarito))
        modo = self.var_dificuldade.get()

        instrucoes_especificas = {
            "Fácil": "- Linguagem simples, questões diretas, sem pegadinhas.",
            "Médio": "- Nível padrão de concursos, sem exageros.",
            "Difícil": "- Questões mais analíticas, alternativas próximas.",
            "Modo Extremo": "- Questões altamente elaboradas, com linguagem complexa e alternativas muito parecidas."
        }

        instrucao = (
            f"Gere questões objetivas com base em \"{assunto}\" no estilo da banca \"{banca}\".\n\n"
            "Regras obrigatórias:\n"
            f"{instrucoes_especificas.get(modo, '')}\n"
            f"- Cada questão deve ter {len(letras)} alternativas ({', '.join(letras)}), com apenas UMA correta.\n"
            "- A posição da alternativa correta DEVE SEGUIR EXATAMENTE a ordem da lista abaixo.\n"
            "- NÃO mencione ou repita a sequência no enunciado, apenas se solicitado.\n"
            "- NÃO sublinhe, indique, ou coloque em negrito as alternativas corretas.\n"
            "- Gere 5 questões por vez.\n"
        )

        if "português" in assunto.lower() or "português" in materia.lower():
            instrucao += (
                "\nOBS: Como o tema envolve Português, use um texto base curto a cada 5 questões. "
                "Após 5 questões, gere um novo texto para o próximo grupo.\n"
            )

        instrucao += (
            "\n■ Exemplo:\n1. C\n2. A\n3. D\n=> A 1ª questão deve ter C como correta, a 2ª A, etc.\n"
            "\n▶ Sequência de gabarito:\n"
            f"{gabarito_enumerado}\n"
        )

        if self.var_preview.get():
            messagebox.showinfo("Preview do Gabarito", instrucao[:1000] + ("\n..." if len(instrucao) > 1000 else ""))

        # Salvar o .txt
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(instrucao)
            if conteudo_extra:
                f.write("\n\nConteúdo adicional extraído dos documentos:\n")
                f.write(conteudo_extra)

        # ✅ Exportar como PDF, se solicitado
        if self.var_exportar_pdf.get():
            try:
                sucesso_pdf = salvar_pdf(caminho)
                if not sucesso_pdf:
                    messagebox.showwarning("Aviso", "Não foi possível exportar o PDF.")
            except Exception as e:
                registrar_erro(e)
                messagebox.showwarning("Erro", "Erro ao exportar o PDF.")

        # Abrir pasta após salvar
        if self.var_abrir_apos_salvar.get():
            webbrowser.open(pasta)

        mensagem_final = f"Gabarito salvo em:\n{caminho}"

        if self.var_exportar_pdf.get():
            caminho_pdf = os.path.splitext(caminho)[0] + ".pdf"
            if os.path.exists(caminho_pdf):
                mensagem_final += f"\n\n✎ PDF exportado como:\n{caminho_pdf}"

        messagebox.showinfo("Sucesso", mensagem_final)


        # Atualiza e salva as configurações do usuário
        self.config.update({
            "pasta_salvamento": pasta,
            "nome_personalizado": self.var_nome_personalizado.get(),
            "salvar_mesma_pasta": self.var_mesma_pasta.get(),
            "open_after_saving": self.var_abrir_apos_salvar.get(),
            "preview": self.var_preview.get(),
            "exportar_pdf": self.var_exportar_pdf.get(),
            "last_used_subject": self.entry_assunto.get().strip(),
            "last_used_board": self.entry_banca.get().strip(),
            "last_question_count": int(qtd),
            "last_alt_count": int(alternativas),
            "modo_dificuldade": self.var_dificuldade.get()
        })
        save_config(self.config)