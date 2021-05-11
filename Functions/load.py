import tkinter as tk
from tkinter import filedialog
import pyedflib
import numpy as np
from Classes import Evento


def loadEDF():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .EDF",
        filetypes=(("EDF files", "*.edf"), ("all files", "*.*")),
    )

    return nome_arquivo

def loadTSE():
    root = tk.Tk()
    root.withdraw()

    f_tse = filedialog.askopenfilename(
        title="Selecione o arquivo .tse",
        filetypes=(("tse files", "*.tse"), ("all files", "*.*")),
    )
    return f_tse

def load_event():
    root = tk.Tk()
    root.withdraw()

    f_tse = filedialog.askopenfilename(
        title="Selecione o arquivo .tse",
        filetypes=(("tse files", "*.tse"), ("all files", "*.*")),
    )
    
    # f_tse = open("caminho_arquivo", "r")

    # conteudo = np.loadtxt(f_tse, dtype=('f4', 'f4', 'str', 'i4'), skiprows=2)

    conteudo = np.genfromtxt(f_tse, dtype="str", skip_header=2)

    quantidade_eventos = len(conteudo[:])

    eventos = []

    for i in range(0, quantidade_eventos):
        evento = Evento.Evento(
            float(conteudo[i][0]),
            float(conteudo[i][1]),
            conteudo[i][2],
            float(conteudo[i][3]),
        )
        eventos.append(evento)

    return eventos

def read_event(f_tse):
    conteudo = np.genfromtxt(f_tse, dtype="str", skip_header=2)

    quantidade_eventos = len(conteudo[:])

    eventos = []

    for i in range(0, quantidade_eventos):
        evento = Evento.Evento(
            float(conteudo[i][0]),
            float(conteudo[i][1]),
            conteudo[i][2],
            float(conteudo[i][3]),
        )
        eventos.append(evento)

    return eventos