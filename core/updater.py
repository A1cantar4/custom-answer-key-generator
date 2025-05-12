import requests
import sys
import os
import subprocess
from tkinter import messagebox
import traceback
import re

VERSAO_ATUAL = "1.4.0"
GITHUB_RAW_UPDATER_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/refs/heads/master/core/updater.py"

def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

def extrair_versao(codigo_remoto):
    match = re.search(r'VERSAO_ATUAL\s*=\s*[\'"](.+?)[\'"]', codigo_remoto)
    return match.group(1) if match else None

def verificar_e_atualizar(mostrar_mensagem=False):
    print("🔍 Verificando atualização... mostrar_mensagem =", mostrar_mensagem)
    try:
        r = requests.get(GITHUB_RAW_UPDATER_URL)
        if r.status_code == 200:
            codigo_remoto = r.text
            versao_online = extrair_versao(codigo_remoto)
            print(f"📄 Versão online: {versao_online} | Local: {VERSAO_ATUAL}")
            if versao_online and versao_online != VERSAO_ATUAL:
                resp = messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?")
                if resp:
                    caminho_atual = os.path.abspath(sys.argv[0])
                    with open(caminho_atual, "w", encoding="utf-8") as f:
                        f.write(codigo_remoto)
                    messagebox.showinfo("Atualizado", "Aplicativo atualizado. Reiniciando...")
                    subprocess.Popen([sys.executable, caminho_atual])
                    sys.exit()
            elif mostrar_mensagem:
                messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")
        else:
            if mostrar_mensagem:
                messagebox.showerror("Erro", "Não foi possível acessar a versão online.")
    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para mais detalhes.")
