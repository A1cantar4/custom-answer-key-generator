import os
import re
import subprocess
from pathlib import Path

# === CONFIGURAÇÕES ===
VERSAO_PY = Path("core/versao.py")
INSTALADOR_ISS = Path("instalador.iss")
COMPILADOR_BAT = Path("compilador.bat")
INNO_SETUP_PATH = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"  # ajuste se necessário

# === UTILITÁRIOS ===

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
    with open(INSTALADOR_ISS, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    with open(INSTALADOR_ISS, "w", encoding="utf-8") as f:
        for linha in linhas:
            if linha.strip().lower().startswith("appversion="):
                f.write(f"AppVersion={nova_versao}\n")
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

# === EXECUÇÃO ===

def main():
    print("\n=== Atualizador de Versão do GabaritoApp ===\n")
    nova_versao = input("Digite a nova versão (ex: 1.7.8): ").strip()

    if not re.match(r"^\d+\.\d+\.\d+$", nova_versao):
        print("[ERRO] Formato de versão inválido.")
        return

    if not VERSAO_PY.exists() or not INSTALADOR_ISS.exists():
        print("[ERRO] Arquivos versao.py ou instalador.iss não encontrados.")
        return

    atualizar_versao_py(nova_versao)
    atualizar_instalador_iss(nova_versao)

    print(f"\n[OK] Versão atualizada para {nova_versao} com sucesso.")

    if input("\nDeseja compilar o EXE agora? (s/n): ").lower() == "s":
        compilar_exe()

    if input("\nDeseja compilar o instalador agora? (s/n): ").lower() == "s":
        compilar_instalador()

    print("\n=== Processo concluído ===\n")

if __name__ == "__main__":
    main()