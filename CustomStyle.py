from imports import *

def SimpleStyle(root):
    style = ttk.Style(root)
    style.theme_use('classic') # \\ Theme

    # \\ Base colors \\
    background = '#868686'
    foreground = '#000000'
    accent = '#555555'
    active = '#666666'
    disabled = '#444444'

    # \\ Configure widget styles \\
    style.configure('.', 
                   font=('Helvetica', 10),
                   background=background,
                   foreground=foreground)

    style.configure('TFrame',
                    background=background)

    style.configure('TLabel',
                    font=('Helvetica', 12),
                    background=background,
                    foreground=foreground)

    style.configure('TButton',
                    background=accent,
                    borderwidth=1,
                    focusthickness=0,
                    relief='flat')
    style.map('TButton',
              background=[('active', active), 
                         ('disabled', disabled)],
              foreground=[('disabled', '#888888')])

    style.configure('TCombobox',
                    fieldbackground=accent,
                    arrowsize=15)
    style.map('TCombobox',
              fieldbackground=[('readonly', accent)],
              selectbackground=[('readonly', active)],
              selectforeground=[('readonly', foreground)])

    style.configure('TEntry',
                    fieldbackground=accent)
    style.map('TEntry',
              fieldbackground=[('readonly', accent)])

    style.configure('TLabelframe',
                    background=background,
                    foreground=foreground)
    style.configure('TLabelframe.Label',
                    background=background,
                    foreground=foreground) 
    
    