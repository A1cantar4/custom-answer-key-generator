# Ponto de ligação entre todas os arquivos

# Como está tudo "linkado" no Layout.py, então importar é o essencial
from ttkbootstrap import Window
from ui.layout import GabaritoApp


THEME_NAME = "flatly"  # Nome do tema principal

# Startar APP
if __name__ == "__main__":
    root = Window(themename=THEME_NAME)
    interface = GabaritoApp(root)
    root.mainloop()