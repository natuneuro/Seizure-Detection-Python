import tkinter as tk
from tkinter import filedialog
import os
import pyedflib
import numpy as np
from Classes import SinalEEG
from Classes2 import Evento


def LoadEvento(nomeArquivoTSE):
    conteudo = np.genfromtxt(nomeArquivoTSE, dtype="str", skip_header=2)

    quantidade_eventos = len(conteudo[:])

    eventos = []

    for i in range(0, quantidade_eventos - 1):
        evento = Evento.Evento(
            float(conteudo[i][0]),
            float(conteudo[i][1]),
            conteudo[i][2],
            float(conteudo[i][3]),
        )
        eventos.append(evento)

    return eventos


def ImportarCaminhoArquivos():
    nome_arquivo_edf = filedialog.askopenfilename(
        title="Selecione o arquivo .EDF",
        filetypes=(("EDF files", "*.edf"), ("all files", "*.*")),
    )

    nome_arquivo_tse = filedialog.askopenfilename(
        title="Selecione o arquivo .tse",
        filetypes=(("tse files", "*.tse"), ("all files", "*.*")),
    )

    return nome_arquivo_edf, nome_arquivo_tse


def ImportarDiretorios():
    nome_arquivo_edf = ObterNomeDiretorioEDF()
    nome_arquivo_tse = ObterDiretorioTSE()
    return nome_arquivo_edf, nome_arquivo_tse


def ObterNomeDiretorioEDF():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .EDF",
        filetypes=(("EDF files", "*.edf"), ("all files", "*.*")),
    )
    path = nome_arquivo
    nome_original = os.path.basename(os.path.normpath(path))
    print('Nome original: ' + nome_original)
    diretorio = nome_arquivo.replace(nome_original, '')
    print('Nome Diretorio: ' + diretorio)

    return diretorio


def ObterDiretorioTSE():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .TSE",
        filetypes=(("EDF files", "*.tse"), ("all files", "*.*")),
    )

    path = nome_arquivo
    nome_original = os.path.basename(os.path.normpath(path))
    print('Nome original: ' + nome_original)
    diretorio = nome_arquivo.replace(nome_original, '')
    print('Nome Diretorio: ' + diretorio)

    return diretorio


def ObterNomeArquivoEDF():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .EDF",
        filetypes=(("EDF files", "*.edf"), ("all files", "*.*")),
    )
    path = nome_arquivo
    nome_original = os.path.basename(os.path.normpath(path))
    print('Nome original: ' + nome_original)
    diretorio = nome_arquivo.replace(nome_original, '')
    print('Nome Diretorio: ' + diretorio)

    return nome_arquivo


def ObterNomeArquivoTSE():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .TSE",
        filetypes=(("EDF files", "*.tse"), ("all files", "*.*")),
    )

    return nome_arquivo


def ImportarSinalEEG():
    nome_arquivo_edf = ObterNomeArquivoEDF()
    path = nome_arquivo_edf
    nome_original = os.path.basename(os.path.normpath(path))
    print('Nome original: ' + nome_original)
    sinal_arquivo_edf = pyedflib.EdfReader(nome_arquivo_edf)
    sinal_eeg = SinalEEG.SinalEEG(sinal_arquivo_edf)
    nome_arquivo_tse = nome_arquivo_edf.replace(".edf", ".tse")

    return sinal_eeg, nome_original


def ImportarArquivoTSE():
    pass


# ESCOLHA DE MODELO
def ModeloEscolhido():
    nome_modelo = ObterNomeArquivoEDF()
    path = nome_modelo
    nome_original = os.path.basename(os.path.normpath(path))
    print('Nome original: ' + nome_original)

    return nome_original


def ObterNomeModelo():
    root = tk.Tk()
    root.withdraw()

    nome_arquivo = filedialog.askopenfilename(
        title="Select a exist model",
        filetypes=(("all files", "*.*")),
    )

    return nome_arquivo
