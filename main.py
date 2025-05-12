from ttkbootstrap import Window
from ui.layout import GabaritoApp

if __name__ == "__main__":
    root = Window(themename="flatly")
    app = GabaritoApp(root)
    root.mainloop()