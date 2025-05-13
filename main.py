"""Ponto de entrada principal da aplicação de geração de gabaritos."""

from ttkbootstrap import Window
from ui.layout import GabaritoApp

THEME_NAME = "flatly"  # Pode ser alterado por configuração no futuro

if __name__ == "__main__":
    root = Window(themename=THEME_NAME)
    interface = GabaritoApp(root)
    root.mainloop()
