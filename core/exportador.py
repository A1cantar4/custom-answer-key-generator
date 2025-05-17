from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import textwrap
import os

def salvar_pdf(caminho_txt, caminho_pdf=None):
    if not os.path.exists(caminho_txt):
        return False

    with open(caminho_txt, "r", encoding="utf-8") as f:
        conteudo = f.read()

    if not caminho_pdf:
        caminho_pdf = os.path.splitext(caminho_txt)[0] + ".pdf"

    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4
    margem = 2 * cm
    y = altura - margem

    # Fonte e tamanho
    c.setFont("Helvetica", 11)
    linhas = textwrap.wrap(conteudo, width=95)

    for linha in linhas:
        if y < margem:
            c.showPage()
            y = altura - margem
            c.setFont("Helvetica", 11)
        c.drawString(margem, y, linha)
        y -= 14

    c.save()
    return True
