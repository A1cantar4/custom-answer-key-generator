from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import re

# Caminho relativo à pasta do script (core)
FONTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'DejaVuSans.ttf'))

# Registra a fonte DejaVuSans com suporte a Unicode simples
pdfmetrics.registerFont(TTFont('DejaVuSans', FONTE_PATH))

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
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm
    )

    # Estilos com a fonte registrada
    titulo = ParagraphStyle(name="Titulo", fontName="DejaVuSans", fontSize=16, spaceAfter=12)
    corpo = ParagraphStyle(name="Corpo", fontName="DejaVuSans", fontSize=12, leading=16, alignment=4)

    story = []

    # Cabeçalho
    story.append(Paragraph("■ Gabarito Gerado", titulo))
    story.append(Spacer(1, 12))

    # Regex adaptado ao novo símbolo ▶
    padrao = r"(▶ Sequência de gabarito:\s*)([\s\S]+?)($|\n\n)"
    match = re.search(padrao, conteudo)

    if match:
        antes = conteudo[:match.start(1)].strip()
        gabarito_texto = match.group(2).strip()
        depois = conteudo[match.end(2):].strip()

        # Texto antes do gabarito
        for linha in antes.splitlines():
            if linha.strip():
                story.append(Paragraph(linha.strip(), corpo))
            else:
                story.append(Spacer(1, 10))

        story.append(Spacer(1, 20))
        story.append(Paragraph("✎ Tabela de Gabarito", titulo))
        story.append(Spacer(1, 10))

        # Tabela de gabarito
        linhas_gabarito = [linha for linha in gabarito_texto.splitlines() if re.match(r"^\d+\.\s+[A-ECE]$", linha)]
        dados = [["Nº", "Resposta"]]
        for linha in linhas_gabarito:
            num, letra = linha.split(".")
            dados.append([num.strip(), letra.strip()])

        tabela = Table(dados, colWidths=[3 * cm, 4 * cm])
        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tabela)

        # Texto depois do gabarito
        if depois:
            story.append(Spacer(1, 20))
            story.append(Paragraph("➤ Conteúdo Complementar", titulo))
            story.append(Spacer(1, 10))
            for linha in depois.splitlines():
                if linha.strip():
                    story.append(Paragraph(linha.strip(), corpo))
                else:
                    story.append(Spacer(1, 10))
    else:
        # Caso não encontre o padrão ▶, exibe tudo normalmente
        for linha in conteudo.splitlines():
            if linha.strip():
                story.append(Paragraph(linha.strip(), corpo))
            else:
                story.append(Spacer(1, 10))

    doc.build(story)
    return True
