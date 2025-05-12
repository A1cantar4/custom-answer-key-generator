import requests
import sys
import os
import subprocess
from tkinter import messagebox
import traceback
import re
import zipfile
import io
import shutil

VERSAO_ATUAL = "1.4.1"
GITHUB_RAW_UPDATER_URL = "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/refs/heads/master/core/updater.py"
GITHUB_ZIP_URL = "https://github.com/A1cantar4/gerador-de-gabaritos-personalizados/archive/refs/heads/master.zip"

def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

def extrair_versao(codigo_remoto):
    match = re.search(r'VERSAO_ATUAL\s*=\s*[\'"](.+?)[\'"]', codigo_remoto)
    return match.group(1) if match else None

def atualizar_projeto():
    try:
        response = requests.get(GITHUB_ZIP_URL)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                temp_folder = "temp_update"
                zip_ref.extractall(temp_folder)

                extraido = os.path.join(temp_folder, "gerador-de-gabaritos-personalizados-master")

                for item in os.listdir(extraido):
                    s = os.path.join(extraido, item)
                    d = os.path.join(".", item)

                    if os.path.exists(d):
                        if os.path.isfile(d):
                            os.remove(d)
                        else:
                            shutil.rmtree(d)

                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                    else:
                        shutil.copytree(s, d)

                shutil.rmtree(temp_folder)
                return True
        return False
    except Exception as e:
        registrar_erro(e)
        return False

def verificar_e_atualizar(mostrar_mensagem=False):
    try:
        r = requests.get(GITHUB_RAW_UPDATER_URL)
        if r.status_code == 200:
            codigo_remoto = r.text
            versao_online = extrair_versao(codigo_remoto)
            if versao_online and versao_online != VERSAO_ATUAL:
                resp = messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?")
                if resp:
                    sucesso = atualizar_projeto()
                    if sucesso:
                        messagebox.showinfo("Atualizado", "Aplicativo atualizado. Reiniciando...")
                        subprocess.Popen([sys.executable, sys.argv[0]])
                        sys.exit()
                    else:
                        messagebox.showerror("Erro", "Erro ao atualizar os arquivos do projeto.")
            elif mostrar_mensagem:
                messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")
        else:
            if mostrar_mensagem:
                messagebox.showerror("Erro", "Não foi possível acessar a versão online.")
    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para mais detalhes.")
