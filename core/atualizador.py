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
import tempfile

from core.versao import VERSAO_ATUAL  # Atual versão do app

GITHUB_RAW_UPDATER_URL = (
    "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/refs/heads/master/core/versao.py"
)
GITHUB_ZIP_URL = (
    "https://github.com/A1cantar4/gerador-de-gabaritos-personalizados/archive/refs/heads/master.zip"
)

# Arquivos que não devem ser sobrescritos durante a atualização
IGNORAR_ARQUIVOS = ["config.json", "log_erro.txt", "__pycache__"]

def registrar_erro(e):
    erro = traceback.format_exc()
    with open("log_erro.txt", "a", encoding="utf-8") as f:
        f.write(erro + "\n")
    messagebox.showerror("Erro", f"Ocorreu um erro:\n{type(e).__name__}: {e}")

def extrair_versao(codigo_remoto):
    match = re.search(r'VERSAO_ATUAL\s*=\s*[\'"](.+?)[\'"]', codigo_remoto)
    return match.group(1) if match else None

def atualizar_projeto():
    try:
        response = requests.get(GITHUB_ZIP_URL)
        if response.status_code != 200:
            raise Exception("Não foi possível baixar o arquivo ZIP do GitHub.")

        if not zipfile.is_zipfile(io.BytesIO(response.content)):
            raise Exception("O arquivo ZIP recebido está corrompido ou inválido.")

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            temp_folder = tempfile.mkdtemp()
            zip_ref.extractall(temp_folder)

            extraido = os.path.join(temp_folder, "gerador-de-gabaritos-personalizados-master")

            for item in os.listdir(extraido):
                if item in IGNORAR_ARQUIVOS:
                    continue

                src = os.path.join(extraido, item)
                dest = os.path.join(".", item)

                if os.path.exists(dest):
                    if os.path.isfile(dest):
                        os.remove(dest)
                    else:
                        shutil.rmtree(dest)

                if os.path.isfile(src):
                    shutil.copy2(src, dest)
                else:
                    shutil.copytree(src, dest)

            # Salvar versão anterior para referência
            try:
                with open("versao_antiga.txt", "w", encoding="utf-8") as f:
                    f.write(VERSAO_ATUAL)
            except Exception as e:
                registrar_erro(e)

            shutil.rmtree(temp_folder)
            return True

    except Exception as e:
        registrar_erro(e)
        return False

def verificar_e_atualizar(mostrar_mensagem=False):
    try:
        r = requests.get(GITHUB_RAW_UPDATER_URL)
        if r.status_code != 200:
            if mostrar_mensagem:
                messagebox.showerror("Erro", "Não foi possível acessar a versão online.")
            return

        codigo_remoto = r.text
        versao_online = extrair_versao(codigo_remoto)

        if versao_online and versao_online != VERSAO_ATUAL:
            if messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?"):
                sucesso = atualizar_projeto()
                if sucesso:
                    messagebox.showinfo("Atualizado", "Aplicativo atualizado. Reiniciando...")
                    subprocess.Popen([sys.executable, sys.argv[0]])
                    sys.exit()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar os arquivos do projeto.")
        elif mostrar_mensagem:
            messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")
    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para mais detalhes.")
