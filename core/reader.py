from docx import Document
import PyPDF2

def extrair_texto_docx(caminho):
    doc = Document(caminho)
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())

def extrair_texto_pdf(caminho):
    texto = []
    with open(caminho, "rb") as f:
        leitor = PyPDF2.PdfReader(f)
        for pagina in leitor.pages:
            texto.append(pagina.extract_text())
    return "\n".join(texto).strip()