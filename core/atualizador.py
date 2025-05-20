import requests
import sys
import os
import subprocess
import traceback
import re
import zipfile
import io
import shutil
import tempfile
import ctypes
import time
from tkinter import messagebox
from core.versao import VERSAO_ATUAL

# URLs
GITHUB_RAW_VERSAO_URL = (
    "https://raw.githubusercontent.com/A1cantar4/gerador-de-gabaritos-personalizados/refs/heads/master/core/versao.py"
)
GITHUB_ZIP_SOURCE_URL = (
    "https://github.com/A1cantar4/gerador-de-gabaritos-personalizados/archive/refs/heads/master.zip"
)
GITHUB_ZIP_EXE_URL = (
    "https://github.com/A1cantar4/gerador-de-gabaritos-personalizados/releases/latest/download/GabaritoApp.zip"
)

NOME_EXECUTAVEL = "GabaritoApp.exe"
IGNORAR_ARQUIVOS = [
    "config.json", "log_erro.txt", "__pycache__", ".gitignore", ".gitattributes", ".git", ".github"
]

# === Utilitários ===

def is_frozen():
    return getattr(sys, 'frozen', False)

def tem_permissao_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def registrar_erro(e):
    erro = traceback.format_exc()
    try:
        with open("log_erro.txt", "a", encoding="utf-8") as f:
            f.write(erro + "\n")
    except:
        pass
    try:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{type(e).__name__}: {e}")
    except:
        pass

def extrair_versao(codigo_remoto):
    match = re.search(r'VERSAO_ATUAL\s*=\s*[\'"](.+?)[\'"]', codigo_remoto)
    return match.group(1) if match else None

# === Atualização modo .PY ===

def atualizar_codigo_fonte():
    try:
        response = requests.get(GITHUB_ZIP_SOURCE_URL)
        if response.status_code != 200:
            raise Exception("Não foi possível baixar o código-fonte.")

        if not zipfile.is_zipfile(io.BytesIO(response.content)):
            raise Exception("Arquivo ZIP do GitHub inválido ou corrompido.")

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            temp_folder = tempfile.mkdtemp()
            zip_ref.extractall(temp_folder)

            extraido = os.path.join(temp_folder, "gerador-de-gabaritos-personalizados-master")

            for item in os.listdir(extraido):
                if item in IGNORAR_ARQUIVOS or item.startswith("."):
                    continue

                src = os.path.join(extraido, item)
                dest = os.path.join(".", item)

                if os.path.exists(dest):
                    try:
                        if os.path.isfile(dest) or os.path.islink(dest):
                            os.remove(dest)
                        else:
                            shutil.rmtree(dest)
                    except:
                        continue

                try:
                    if os.path.isfile(src):
                        shutil.copy2(src, dest)
                    else:
                        shutil.copytree(src, dest)
                except:
                    continue

            with open("versao_antiga.txt", "w", encoding="utf-8") as f:
                f.write(VERSAO_ATUAL)

            shutil.rmtree(temp_folder)
            return True

    except Exception as e:
        registrar_erro(e)
        return False

# === Atualização modo .EXE ===

def criar_e_executar_reiniciador():
    nome_atual = os.path.basename(sys.executable)
    bat_conteudo = f"""@echo off
timeout /t 2 >nul
if exist "{nome_atual}" (
    ren "{nome_atual}" antigo_backup.exe
)
move /Y novo_temp.exe "{nome_atual}" >nul
start "" "{nome_atual}"
exit
"""
    try:
        with open("reiniciador.bat", "w", encoding="utf-8") as f:
            f.write(bat_conteudo)
        subprocess.Popen(["cmd", "/c", "start", "reiniciador.bat"])
    except Exception as e:
        registrar_erro(e)

def atualizar_executavel():
    try:
        response = requests.get(GITHUB_ZIP_EXE_URL)
        if response.status_code != 200:
            raise Exception("Não foi possível baixar a release.")

        zip_bytes = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_bytes) as z:
            exe_temp = "novo_temp.exe"
            for nome in z.namelist():
                if nome.endswith(".exe"):
                    with open(exe_temp, "wb") as f:
                        f.write(z.read(nome))
                    break
            else:
                raise Exception("Executável não encontrado no ZIP.")

        criar_e_executar_reiniciador()
        return True

    except Exception as e:
        registrar_erro(e)
        return False

# === Verificador principal híbrido ===

def verificar_e_atualizar(mostrar_mensagem=False):
    try:
        r = requests.get(GITHUB_RAW_VERSAO_URL)
        if r.status_code != 200:
            if mostrar_mensagem:
                messagebox.showerror("Erro", "Não foi possível acessar a versão online.")
            return

        versao_online = extrair_versao(r.text)

        if versao_online and versao_online != VERSAO_ATUAL:
            if messagebox.askyesno("Atualização disponível", f"Versão {versao_online} disponível. Atualizar agora?"):

                if not tem_permissao_admin():
                    resposta = messagebox.askyesno("Permissão necessária", "A atualização requer permissões de administrador. Deseja continuar?")
                    if resposta:
                        ctypes.windll.shell32.ShellExecuteW(
                            None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
                        )
                    sys.exit()

                sucesso = atualizar_executavel() if is_frozen() else atualizar_codigo_fonte()

                if sucesso:
                    messagebox.showinfo("Atualizado", "Atualização concluída. O aplicativo será reiniciado.")
                    if not is_frozen():
                        subprocess.Popen([sys.executable, os.path.abspath(sys.argv[0])])
                    sys.exit()
                else:
                    messagebox.showerror("Erro", "Erro durante a atualização.")

        elif mostrar_mensagem:
            messagebox.showinfo("Atualização", "Você já está com a versão mais recente.")

    except Exception as e:
        registrar_erro(e)
        if mostrar_mensagem:
            messagebox.showerror("Erro", "Erro ao verificar atualização. Veja o log para detalhes.")
