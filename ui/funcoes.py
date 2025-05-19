import os
import re
import webbrowser
from tkinter import filedialog, messagebox

from core.gerador import gerar_gabarito_balanceado
from core.leitor import extrair_texto_docx, extrair_texto_pdf
from core.exportador import salvar_pdf
from core.configuracoes import save_config
from core.atualizador import registrar_erro


def importar_arquivo(app):
    caminhos = filedialog.askopenfilenames(filetypes=[("Documentos", "*.pdf *.docx")])
    app.arquivos_importados = list(caminhos)

    if app.arquivos_importados:
        nomes = [os.path.basename(p) for p in app.arquivos_importados]
        texto = "Arquivos: " + ", ".join(nomes)
        app.label_arquivos.config(text=texto, foreground="black")
        app.entry_assunto.delete(0, 'end')
        app.entry_assunto.insert(0, "[extraído dos arquivos anexados]")
    else:
        app.label_arquivos.config(text="Nenhum arquivo anexado", foreground="gray")


def salvar_gabarito(app):
    assunto = app.entry_assunto.get().strip()
    banca = app.entry_banca.get().strip()
    materia = app.entry_materia.get().strip()
    qtd = app.spin_qtd.get().strip()
    alternativas = app.var_alternativas.get().strip()

    campos_obrigatorios = {
        "assunto": assunto,
        "banca": banca,
        "qtd": qtd,
        "alternativas": alternativas
    }

    campos_validos = True
    for campo, valor in campos_obrigatorios.items():
        widget = getattr(app, f"entry_{campo}" if campo in ["assunto", "banca"] else "spin_qtd")
        if not valor or (campo == "qtd" and not valor.isdigit()):
            widget.configure(style="Erro.TEntry")
            campos_validos = False
        else:
            widget.configure(style="Normal.TEntry")

    if not campos_validos:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios corretamente.")
        return

    letras = {
        "2": ["C", "E"],
        "4": ["A", "B", "C", "D"],
        "5": ["A", "B", "C", "D", "E"]
    }[alternativas]

    nome_base = f"{assunto}_{banca}" if app.var_nome_personalizado.get() else "gabarito"
    nome_base = re.sub(r'[^\w\- ]', '', nome_base).strip().replace(" ", "_")
    nome_arquivo = f"{nome_base}.txt"

    pasta = os.path.abspath(".") if app.var_mesma_pasta.get() else filedialog.askdirectory()
    if not pasta:
        return
    caminho = os.path.join(pasta, nome_arquivo)

    if os.path.exists(caminho):
        if not messagebox.askyesno("Arquivo existente", f"O arquivo '{nome_arquivo}' já existe. Deseja substituir?"):
            return

    try:
        gabarito = gerar_gabarito_balanceado(qtd=int(qtd), letras=letras)
    except Exception as e:
        registrar_erro(e)
        messagebox.showerror("Erro", "Erro ao gerar o gabarito.")
        return

    conteudo_extra = ""
    for caminho_importado in getattr(app, "arquivos_importados", []):
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

    gabarito_enumerado = "\n".join(f"{i + 1}. {letra}" for i, letra in enumerate(gabarito))
    modo = app.var_dificuldade.get()

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
        "- NUNCA mencione ou repita a sequência no enunciado, apenas se solicitado.\n"
        "- NUNCA sublinhe, indique, ou coloque em negrito as alternativas corretas.\n"
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

    if app.var_preview.get():
        messagebox.showinfo("Preview do Gabarito", instrucao[:1000] + ("\n..." if len(instrucao) > 1000 else ""))

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(instrucao)
        if conteudo_extra:
            f.write("\n\nConteúdo adicional extraído dos documentos:\n")
            f.write(conteudo_extra)

    if app.var_exportar_pdf.get():
        try:
            sucesso_pdf = salvar_pdf(caminho)
            if not sucesso_pdf:
                messagebox.showwarning("Aviso", "Não foi possível exportar o PDF.")
        except Exception as e:
            registrar_erro(e)
            messagebox.showwarning("Erro", "Erro ao exportar o PDF.")

    if app.var_abrir_apos_salvar.get():
        webbrowser.open(pasta)

    mensagem_final = f"Gabarito salvo em:\n{caminho}"

    if app.var_exportar_pdf.get():
        caminho_pdf = os.path.splitext(caminho)[0] + ".pdf"
        if os.path.exists(caminho_pdf):
            mensagem_final += f"\n\n✎ PDF exportado como:\n{caminho_pdf}"

    messagebox.showinfo("Sucesso", mensagem_final)

    app.config.update({
        "pasta_salvamento": pasta,
        "nome_personalizado": app.var_nome_personalizado.get(),
        "salvar_mesma_pasta": app.var_mesma_pasta.get(),
        "open_after_saving": app.var_abrir_apos_salvar.get(),
        "preview": app.var_preview.get(),
        "exportar_pdf": app.var_exportar_pdf.get(),
        "last_used_subject": app.entry_assunto.get().strip(),
        "last_used_board": app.entry_banca.get().strip(),
        "last_question_count": int(qtd),
        "last_alt_count": int(alternativas),
        "modo_dificuldade": app.var_dificuldade.get()
    })
    save_config(app.config)
