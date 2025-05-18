from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
import os
import re

def salvar_pdf(caminho_txt, caminho_pdf=None):
    if not os.path.exists(caminho_txt):
        return False

    with open(caminho_txt, "r", encoding="utf-8") as f:
        conteudo = f.read()

    if not caminho_pdf:
        caminho_pdf = os.path.splitext(caminho_txt)[0] + ".pdf"

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    titulo = ParagraphStyle(name="Titulo", fontName="Times-Bold", fontSize=16, spaceAfter=12)
    corpo = ParagraphStyle(name="Corpo", fontName="Times-Roman", fontSize=12, leading=16, alignment=4)  # 4 = justificado

    story = []

    # Cabeçalho
    story.append(Paragraph("📄 Gabarito Gerado", titulo))
    story.append(Spacer(1, 12))

    # Separar gabarito (ex: 1. A\n2. B...) do restante do conteúdo
    padrao = r"(📌 Sequência de gabarito:\s*)([\s\S]+?)($|\n\n)"
    match = re.search(padrao, conteudo)

    if match:
        # Parte antes do gabarito
        antes = conteudo[:match.start(1)].strip()
        gabarito_texto = match.group(2).strip()
        depois = conteudo[match.end(2):].strip()

        # Parágrafos principais
        for linha in antes.splitlines():
            if linha.strip():
                story.append(Paragraph(linha.strip(), corpo))
            else:
                story.append(Spacer(1, 10))

        story.append(Spacer(1, 20))
        story.append(Paragraph("🧾 Tabela de Gabarito", titulo))
        story.append(Spacer(1, 10))

        # Montar tabela do gabarito
        linhas_gabarito = [linha for linha in gabarito_texto.splitlines() if re.match(r"^\d+\.\s+[A-ECE]$", linha)]
        dados = [["Nº", "Resposta"]]
        for linha in linhas_gabarito:
            num, letra = linha.split(".")
            dados.append([num.strip(), letra.strip()])

        tabela = Table(dados, colWidths=[3*cm, 4*cm])
        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tabela)

        # Parte extra depois do gabarito
        if depois:
            story.append(Spacer(1, 20))
            story.append(Paragraph("📎 Conteúdo Complementar", titulo))
            story.append(Spacer(1, 10))
            for linha in depois.splitlines():
                if linha.strip():
                    story.append(Paragraph(linha.strip(), corpo))
                else:
                    story.append(Spacer(1, 10))
    else:
        # Caso não consiga separar, exibe tudo como texto normal
        for linha in conteudo.splitlines():
            if linha.strip():
                story.append(Paragraph(linha.strip(), corpo))
            else:
                story.append(Spacer(1, 10))

    doc.build(story)
    return True
