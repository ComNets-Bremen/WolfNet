#!/usr/bin/env python3

# From https://www.pythontutorial.net/tkinter/tkinter-listbox/

import tkinter as tk
from tkinter import ttk
import configparser
from tkinter.messagebox import showinfo


CONFIGFILE="config.ini"

config = configparser.ConfigParser()

with open(CONFIGFILE, "w") as cf:
        config.write(cf)

print(config)

root = tk.Tk()
root.geometry("200x100")
root.resizable(False, False)
root.title("Listbox")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

langs = ('Java', 'C#', 'C', 'C++', 'Python',
        'Go', 'JavaScript', 'PHP', 'Swift')
langs_var = tk.StringVar(value=langs)

listbox = tk.Listbox(
    root,
    listvariable=langs_var,
    height=6,
    selectmode='extended')

listbox.grid(
    column=0,
    row=0,
    sticky='nwes'
)

scrollbar = ttk.Scrollbar(
    root,
    orient='vertical',
    command=listbox.yview
)
listbox['yscrollcommand'] = scrollbar.set

scrollbar.grid(
    column=1,
    row=0,
    sticky='ns')

# handle event
def items_selected(event):
    """ handle item selected event
    """
    # get selected indices
    selected_indices = listbox.curselection()
    # get selected items
    selected_langs = ",".join([listbox.get(i) for i in selected_indices])
    msg = f'You selected: {selected_langs}'

    showinfo(
        title='Information',
        message=msg)

listbox.bind('<<ListboxSelect>>', items_selected)

root.mainloop()
"""
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()
"""
