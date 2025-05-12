import os
import json

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".gabarito_settings.json")

def carregar_configuracoes():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def salvar_configuracoes(config):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(config, f)
    except:
        pass
