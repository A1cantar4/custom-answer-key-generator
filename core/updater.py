import requests
import sys
import os
import subprocess
from tkinter import messagebox
import traceback

VERSAO_ATUAL = "1.4.0"
GITHUB_RAW_VERSAO_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/versao.txt"
GITHUB_RAW_SCRIPT_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/main/app.py"

def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

def verificar_e_atualizar(mostrar_mensagem=False):
    try:
        r = requests.get(GITHUB_RAW_VERSAO_URL)
        if r.status_code == 200:
            versao_online = r.text.strip()
            if versao_online != VERSAO_ATUAL:
                resp = messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?")
                if resp:
                    novo_script = requests.get(GITHUB_RAW_SCRIPT_URL)
                    if novo_script.status_code == 200:
                        caminho_atual = os.path.abspath(sys.argv[0])
                        with open(caminho_atual, "w", encoding="utf-8") as f:
                            f.write(novo_script.text)
                        messagebox.showinfo("Atualizado", "Aplicativo atualizado. Reiniciando...")
                        subprocess.Popen([sys.executable, caminho_atual])
                        sys.exit()
            elif mostrar_mensagem:
                messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")
    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para mais detalhes.")