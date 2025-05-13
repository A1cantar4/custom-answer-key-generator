import json
import os

CONFIG_FILE = "user_config.json"
ENCODING = "utf-8"

# Configuração padrão se nenhuma for encontrada
default_config = {
    "open_after_saving": False,
    "use_custom_name": False,
    "last_used_subject": "",
    "last_used_board": "",
    "last_alt_count": 5,
    "last_question_count": 30
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding=ENCODING) as f:
                data = json.load(f)
                # Valida se todas as chaves estão presentes
                for key, value in default_config.items():
                    data.setdefault(key, value)
                return data
        except Exception:
            pass  # em caso de erro, cai no retorno padrão abaixo
    return default_config.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding=ENCODING) as f:
        json.dump(config, f, indent=4)
