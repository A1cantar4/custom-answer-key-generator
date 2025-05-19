import ttkbootstrap as ttk

def aplicar_estilos(style=None):
    """
    Aplica o tema 'flatly' e configura os estilos personalizados para a interface.

    Args:
        style (ttk.Style): Objeto de estilo opcional. Se não for fornecido, será criado um novo.
    """
    if style is None:
        style = ttk.Style()

    style.theme_use("flatly")

    style.configure("Glass.TFrame", background="#ffffff", relief="flat")
    style.configure("TEntry", fieldbackground="#ffffff", borderwidth=1)
    style.configure("TCheckbutton", background="#ffffff")
    style.configure("TButton", padding=6, relief="flat")
    style.configure("Erro.TEntry", fieldbackground="#ffcccc")
    style.configure("Normal.TEntry", fieldbackground="white")

    return style
