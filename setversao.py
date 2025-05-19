import os
import re
import subprocess
from pathlib import Path
import zipfile

# === CONFIGURAÇÕES ===
VERSAO_PY = Path("core/versao.py")
INSTALADOR_ISS = Path("instalador.iss")
COMPILADOR_BAT = Path("compilador.bat")
DIST_DIR = Path("dist")
INNO_SETUP_PATH = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"  # Altere se necessário

NOME_EXE = "GabaritoApp.exe"
PASTA_RELEASES = Path("releases")

# === UTILITÁRIOS ===

def extrair_versao_atual():
    if not VERSAO_PY.exists():
        print("[ERRO] core/versao.py não encontrado.")
        return None
    with open(VERSAO_PY, "r", encoding="utf-8") as f:
        for linha in f:
            match = re.match(r'VERSAO_ATUAL\s*=\s*[\'"](.+?)[\'"]', linha)
            if match:
                return match.group(1)
    print("[ERRO] VERSAO_ATUAL não encontrada no versao.py.")
    return None

def atualizar_versao_py(nova_versao: str):
    with open(VERSAO_PY, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    with open(VERSAO_PY, "w", encoding="utf-8") as f:
        for linha in linhas:
            if linha.strip().startswith("VERSAO_ATUAL"):
                f.write(f'VERSAO_ATUAL = "{nova_versao}"\n')
            else:
                f.write(linha)

def atualizar_instalador_iss(nova_versao: str):
    if not INSTALADOR_ISS.exists():
        print("[ERRO] instalador.iss não encontrado.")
        return

    with open(INSTALADOR_ISS, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    with open(INSTALADOR_ISS, "w", encoding="utf-8") as f:
        for linha in linhas:
            if linha.strip().lower().startswith("appversion="):
                f.write(f"AppVersion={nova_versao}\n")
            elif linha.strip().lower().startswith("setupiconfile="):
                f.write('SetupIconFile=assets\\icon.ico\n')
            else:
                f.write(linha)

def compilar_exe():
    if COMPILADOR_BAT.exists():
        subprocess.run([str(COMPILADOR_BAT)], shell=True)
    else:
        print("[ERRO] Arquivo compilador.bat não encontrado.")

def compilar_instalador():
    if Path(INNO_SETUP_PATH).exists():
        subprocess.run([INNO_SETUP_PATH, str(INSTALADOR_ISS)], shell=True)
    else:
        print(f"[ERRO] Inno Setup não encontrado em: {INNO_SETUP_PATH}")
        print("Edite o caminho no script se estiver diferente.")

def criar_zip_release():
    exe_path = DIST_DIR / NOME_EXE
    if not exe_path.exists():
        print("[ERRO] Executável não encontrado após compilação.")
        return

    # Cria pasta releases se não existir
    PASTA_RELEASES.mkdir(exist_ok=True)

    zip_name = PASTA_RELEASES / "GabaritoApp.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(exe_path, arcname=NOME_EXE)

    print(f"[OK] Arquivo ZIP criado para release: {zip_name}")

# === EXECUÇÃO PRINCIPAL ===

def main():
    print("\n=== Atualizador de Versão do GabaritoApp ===\n")
    nova_versao = input("Digite a nova versão (ex: 1.7.9): ").strip()

    if not re.match(r"^\d+\.\d+\.\d+$", nova_versao):
        print("[ERRO] Formato de versão inválido. Use o formato X.Y.Z")
        return

    versao_antiga = extrair_versao_atual()
    if not versao_antiga:
        return

    print(f"\n→ Atualizando da versão {versao_antiga} para {nova_versao}...\n")

    atualizar_versao_py(nova_versao)
    atualizar_instalador_iss(nova_versao)

    print(f"[OK] Versão atualizada com sucesso para {nova_versao}.\n")

    if input("Deseja compilar o EXE agora? (s/n): ").lower() == "s":
        compilar_exe()

    if input("Deseja compilar o instalador agora? (s/n): ").lower() == "s":
        compilar_instalador()

    if input("Deseja gerar o .ZIP para release no GitHub? (s/n): ").lower() == "s":
        criar_zip_release()

    print("\n=== Processo concluído ===\n")

if __name__ == "__main__":
    main()