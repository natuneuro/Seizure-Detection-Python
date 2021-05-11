from tkinter import *
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
from tkinter.filedialog import askopenfile, askopenfilename
from PIL import Image, ImageTk
import sqlite3
import numpy as np
import tensorflow as tf
import math
import sys
import matplotlib.pyplot as plt
from sklearn import preprocessing
import os
import time
import mne
import pyedflib
from Classes2 import Evento
from Classes2 import SinalEEG
from Functions import load, processing, network, plots
#from Modulos import LeituraArquivos,ConfusionMatrix, ProcessamentoDoSinal, LeituraEventos, AssociaTrechoEvento, CriaImagen, CNN

from Modulos2 import (
    CNN,
    AssociaTrechoEvento,
    ConfusionMatrix,
    CriaImagen,
    LeituraArquivos,
    LeituraEventos,
    ProcessamentoDoSinal,
    CriaRede,
    UsaRede,
    graficos,
)

Imagem1 = "ufmg _logo.png"

root = tix.Tk()
accuracyValue = "A"
recall = "A"
precision = "A"
arquivoName = ""

# global variable
blank_2 = []
blank_1 = []


class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatorioCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.codigo_entry.get()
        self.ageRel = self.age_entry
        self.infoRel = self.info_entry.get()
        self.generoRel = self.gender_entry
        self.accuracy = accuracyValue
        self.recall = recall
        self.precision = precision
        self.nomeArquivo = arquivoName

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Paciente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Cod: ')
        self.c.drawString(50, 670, 'Age: ')
        self.c.drawString(50, 630, 'Gender: ')
        self.c.drawString(50, 600, 'Informations about: ')
        self.c.drawString(50, 570, 'File name: ')
        self.c.drawString(50, 530, 'Algorithm results: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.age_entry)

        self.c.drawString(150, 630, self.generoRel)
        self.c.drawString(200, 600, self.infoRel)
        self.c.drawString(200, 570, self.nomeArquivo)
        self.c.drawString(300, 530, self.accuracy)
        self.c.rect(20, 300, 550, 5, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.info_entry.delete(0, END)
        self.Tipvar.set('Male')
        self.nomeArquivo = ''
        self.accuracy_entry = ''
        self.recall_entry = ''
        self.precision_entry = ''

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd()
        ### Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nomeArquivo CHAR(200) NOT NULL,
                info CHAR(200),
                age INT(50),
                genero CHAR(40),
                accuracy INT(40),
                recall INT(40),
                precision  INT(40)
            );
        
        """)
        # ADD  acurracy CHAR(40)
        self.conn.commit()
        self.desconecta_bd()

    def variaveis_inicio(self):
        self.codigo = self.codigo_entry.get()
        self.age = self.age_entry.get()
        self.genero = self.Tipvar.get()
        self.info = self.info_entry.get()
        self.nomeArquivo = self.nomeArquivo
        self.accuracy = self.accuracy_entry
        self.recall = self.recall_entry
        self.precision = self.precision_entry
        self.ditArquivoEDF = self.ditArquivoEDF
        self.nomeArquivoEDF = self.nomeArquivoEDF
        self.nome_arquivo_salvo = self.nome_arquivo_salvo

    def variaveis_acao(self):
        self.codigo = self.codigo_entry.get()
        self.age = self.age_entry.get()
        self.genero = self.Tipvar.get()
        self.info = self.info_entry.get()
        self.nomeArquivo = self.nomeArquivo
        self.accuracy = self.accuracy_entry
        self.recall = self.recall_entry
        self.precision = self.precision_entry

    def add_cliente(self):
        self.variaveis_inicio()
        if self.nome_arquivo_salvo == "":
            msg = "To register a new patient,\n"
            msg += "it is necessary to select the files"
            messagebox.showinfo("Customer registration - Warning !!!", msg)
        else:
            self.conecta_bd()
            self.cursor.execute(
                """ INSERT INTO clientes (age,genero, info, accuracy, recall, precision, nomeArquivo)
                VALUES(?, ?, ?, ?, ?, ?,?) """,
                (self.age, self.genero, self.info, self.accuracy, self.recall,
                 self.precision, self.nome_arquivo_salvo))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_cliente()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(
            """ SELECT cod, age, genero , info, accuracy,recall,precision, nomeArquivo FROM clientes 
            ORDER BY cod;  """)

        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            print(self.listaCli.item(n, 'values'))
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaCli.item(
                n, 'values')
            self.codigo_entry.insert(END, col1)
            self.info_entry.insert(END, col4)
            self.nomeArquivo = col8
            self.accuracy_entry = col5
            self.recall_entry = col6
            self.precision_entry = col7
            self.age_entry.insert(END, col2)
            self.Tipvar.set(col3)
            global accuracyValue
            accuracyValue = col5
            global recall
            recall = col6
            global precision
            precision = col7
            global arquivoName
            arquivoName = col8

    def deleta_cliente(self):
        self.variaveis_acao()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """,
                            (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()

    def alterar_cliente(self):
        self.variaveis_acao()
        self.conecta_bd()
        self.cursor.execute(
            """  UPDATE clientes SET age = ?, info = ?, genero = ?, accuracy = ?, recall=?, precision=?,  nomeArquivo = ?
            WHERE  cod = ?  """,
            (self.age, self.info, self.genero, accuracyValue, precision,
             precision, arquivoName, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        codigo = self.codigo_entry.get()
        self.cursor.execute(
            """  SELECT cod, age, info, genero, accuracy, recall, precision, nomeArquivo FROM clientes
            WHERE cod LIKE '%s' ORDER BY cod ASC""" % codigo)
        buscaCli = self.cursor.fetchall()
        for i in buscaCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()


class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.root2 = root
        self.sinal_eeg = []
        self.eventos = []
        self.nomeArquivo = ''
        self.accuracy_entry = ''
        self.ditArquivoEDF = ''
        self.nomeArquivoEDF = ''
        self.nome_arquivo_salvo = ''
        self.recall_entry = ''
        self.precision_entry = ''
        self.new_model_name = ''
        self.tela()
        self.frames_de_tela()
        self.widgets_frame()
        self.montaTabelas()

        root.mainloop()

    def buscar_arquivo(self):
        aux, self.nomeArquivo = LeituraArquivos.ImportarSinalEEG()
        print("-------------------------------")
        print(self.nomeArquivo)
        print("-------------------------------")
        self.sinal_eeg.append(aux)
        aux2 = LeituraEventos.importar_evento()
        self.eventos.append(aux2)

    def buscar_arquivo2(self):
        self.ditArquivoEDF, self.ditArquivoTSE = LeituraArquivos.ImportarDiretorios(
        )
        print("ARQUIVO EDF DIRETORIO" + self.ditArquivoEDF)
        print("ARQUIVO TSE DIRETORIO" + self.ditArquivoTSE)

    def buscar_arquivos3(self):
        self.nomeArquivoEDF, self.nomeArquivoTSE = LeituraArquivos.ImportarCaminhoArquivos(
        )
        print("Nome arquivo" + self.nomeArquivoEDF)
        print("Nome arquivo" + self.nomeArquivoTSE)

    def buscar_arquivos(self):
        #IMPORTAR DIRETORIOS DO ARQUIVO
        print(" LI ARQUIVOS E PEGUEI O CAMINHO ---------------------")
        self.nomeArquivoEDF, self.nomeArquivoTSE = LeituraArquivos.ImportarCaminhoArquivos(
        )

        print("CAMINHO ARQUIVO EDF" + self.nomeArquivoEDF)
        print("CAMINHO ARQUIVO TSE" + self.nomeArquivoTSE)
        #IMPORTAR NOME DOS ARQUIVOS
        print("AGORA VOU PEGAR OS NOMES ORIGINAIS ---------------------")
        path = self.nomeArquivoEDF
        nome_arquivo = self.nomeArquivoEDF
        nome_original = os.path.basename(os.path.normpath(path))
        self.ditArquivoEDF = nome_arquivo.replace(nome_original, '')

        path2 = self.nomeArquivoTSE
        nome_arquivo2 = self.nomeArquivoTSE
        nome_original2 = os.path.basename(os.path.normpath(path))
        self.ditArquivoTSE = nome_arquivo.replace(nome_original2, '')

        print("DIRETÓRIO ARQUIVO EDF" + self.ditArquivoEDF)
        print("DIRETÓRIO ARQUIVO TSE" + self.ditArquivoTSE)

        #IMPORTAR APENAS O CAMINHO SEM O NOME DO ARQUIVO
        print("AGORA VOU PEGAR SÓ O CAMINHO E O EVENTO ---------------------")
        self.nomeArquivo = self.nomeArquivoEDF
        path = self.nomeArquivoEDF
        nome_original = os.path.basename(os.path.normpath(path))
        print('Nome original: ' + nome_original)
        sinal_arquivo_edf = pyedflib.EdfReader(self.nomeArquivoEDF)
        sinal_eeg = SinalEEG.SinalEEG(sinal_arquivo_edf)
        nome_arquivo_tse = self.nomeArquivoEDF.replace(".edf", ".tse")
        self.nome_arquivo_salvo = nome_original.replace(".edf", "")
        self.sinal_eeg.append(sinal_eeg)
        conteudo = np.genfromtxt(self.nomeArquivoTSE,
                                 dtype="str",
                                 skip_header=2)
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

        sinal_eeg2 = eventos
        self.eventos.append(sinal_eeg2)

        print("FIM ---------------------------")

    def comecar(self):
        self.JanelaClassificacao()
        self.accuracy_entry = self.accurancyValue_Entry
        self.recall_entry = self.recallValue_Entry
        self.precision_entry = self.precisionValue_Entry
        self.add_cliente()

    def comecar2(self):
        print("---------------------")
        self.JanelaPrediction()
        print("---------------------")
        self.accuracy_entry = self.accurancyValue_Entry
        self.recall_entry = self.recallValue_Entry
        self.precision_entry = self.precisionValue_Entry
        self.add_cliente()

    def tela(self):
        self.root.title("Epilepsy Detection")
        self.root.config(bg="#DFEBE9")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)
        self.logo_cerebro = PhotoImage(file="logos/cerebrito.png")
        label = Label(image=self.logo_cerebro, bg="#DFEBE9")
        label.image = self.logo_cerebro  # keep a reference!
        label.pack(side=LEFT, padx=64, pady=55)

        self.logo_ufmg = Image.open("logos/ufmg _logo.png")
        self.resized_ufmg = self.logo_ufmg.resize((100, 42), Image.ANTIALIAS)
        self.logo_ufmg_resized = ImageTk.PhotoImage(self.resized_ufmg)
        label = Label(image=self.logo_ufmg_resized, bg="#DFEBE9")
        label.image = self.logo_ufmg_resized  # keep a reference!
        label.pack(side=LEFT, anchor=SE, padx=30, pady=30)

        self.logo_labbio = Image.open("logos/labbio_logo.png")
        self.resized_labbio = self.logo_labbio.resize((100, 42),
                                                      Image.ANTIALIAS)
        self.logo_labbio_resized = ImageTk.PhotoImage(self.resized_labbio)
        label = Label(image=self.logo_labbio_resized, bg="#DFEBE9")
        label.image = self.logo_labbio_resized  # keep a reference!
        label.pack(side=LEFT, anchor=SE, padx=1, pady=30)

    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#DFEBE9')
        self.frame_1.place(relx=0.70, rely=0.02, relwidth=0.27, relheight=0.80)

    def widgets_frame(self):
        ## Criando botao limpar
        self.Boton_info = Button(self.frame_1,
                                 text="Abaut",
                                 font=("AvantGarde", 20, "bold"),
                                 command=self.JanelaAbout,
                                 bg="#14787A",
                                 fg="#ffffff",
                                 width="15",
                                 height="1",
                                 cursor="hand2")

        self.Boton_info.place(relx=0.02,
                              rely=0.2,
                              relwidth=0.98,
                              relheight=0.10)

        ## Criando botao buscar
        self.Boton_add = Button(self.frame_1,
                                text="Add Patient",
                                font=("AvantGarde", 20, "bold"),
                                command=self.JanelaAddPaciente,
                                bg="#14787A",
                                fg="#ffffff",
                                width="15",
                                height="1",
                                cursor="hand2")
        self.Boton_add.place(relx=0.02,
                             rely=0.4,
                             relwidth=0.98,
                             relheight=0.10)

        ## Criando botao novo
        self.Boton_open = Button(self.frame_1,
                                 text="Open Patient",
                                 font=("AvantGarde", 20, "bold"),
                                 command=self.JanelaShowPaciente,
                                 bg="#14787A",
                                 fg="#ffffff",
                                 width="15",
                                 height="1",
                                 cursor="hand2")
        self.Boton_open.place(relx=0.02,
                              rely=0.6,
                              relwidth=0.98,
                              relheight=0.10)

        ## Criando botao alterar
        self.Boton_close = Button(self.frame_1,
                                  text="Close",
                                  font=("AvantGarde", 20, "bold"),
                                  command=self.root.quit,
                                  bg="#14787A",
                                  fg="#ffffff",
                                  width="15",
                                  height="1",
                                  cursor="hand2")
        self.Boton_close.place(relx=0.02,
                               rely=0.8,
                               relwidth=0.98,
                               relheight=0.10)

    ################################# ADD PAT ###########################################
    def frames_de_telaAddPat(self):
        self.frame_1 = Frame(self.root2,
                             bd=4,
                             bg='#DFEBE9',
                             highlightbackground='#759fe6',
                             highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root2, bd=4, bg='#DFEBE9')
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frameAddPat(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#DFEBE9')
        self.aba2.configure(background='#DFEBE9')

        self.abas.add(self.aba1, text=" ")
        self.abas.add(self.aba2, text=" ")

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        self.canvas_bt = Canvas(self.aba1,
                                bd=0,
                                bg='#1e3743',
                                highlightbackground='gray',
                                highlightthickness=5)

        self.canvas_bt.place(relx=0.19,
                             rely=0.08,
                             relwidth=0.42,
                             relheight=0.19)
        ## Criando botao limpar
        self.bt_lipar = Button(self.aba1,
                               text="Clean",
                               bd=2,
                               bg='#14787A',
                               activebackground='#108ecb',
                               activeforeground='white',
                               fg='white',
                               font=('verdana', 9, 'bold'),
                               command=self.limpa_cliente)
        self.bt_lipar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        ## Criando botao buscar
        self.bt_buscar = Button(self.aba1,
                                text="Search",
                                bd=2,
                                bg='#14787A',
                                activebackground='#108ecb',
                                activeforeground='white',
                                fg='white',
                                font=('verdana', 9, 'bold'),
                                command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        texto_balao_buscar = "Type in the info field the patient you want to search"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar,
                                      balloonmsg=texto_balao_buscar)

        ## Criando botao apagar
        self.bt_apagar = Button(self.aba1,
                                text="Delete",
                                bd=2,
                                bg='#14787A',
                                activebackground='#108ecb',
                                activeforeground='white',
                                fg='white',
                                font=('verdana', 9, 'bold'),
                                command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.4, rely=0.1, relwidth=0.1, relheight=0.15)

        ## Criando botao alterar
        self.bt_alterar = Button(self.aba1,
                                 text="Change",
                                 bd=2,
                                 bg='#14787A',
                                 activebackground='#108ecb',
                                 activeforeground='white',
                                 fg='white',
                                 font=('verdana', 9, 'bold'),
                                 command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.5, rely=0.1, relwidth=0.1, relheight=0.15)

        ## Botão Classificação
        # Deve abrir uma opção para escrever qual o modelo que deseja usar para realizar a classificação
        #
        #
        #
        self.bt_novo = Button(self.aba1,
                              text="Classification",
                              bd=2,
                              bg='#1e3743',
                              activebackground='#108ecb',
                              activeforeground='white',
                              fg='white',
                              font=('verdana', 11, 'bold'),
                              command=self.JanelaClassificacaoSetup)
        self.bt_novo.place(relx=0.68, rely=0.1, relwidth=0.3, relheight=0.15)

        ## Botão Predicitions
        # Deve demonstrar o que queremos ver dos dados
        #
        #

        self.bt_novo2 = Button(self.aba1,
                               text="Predictions",
                               bd=2,
                               bg='#1e3743',
                               activebackground='#108ecb',
                               activeforeground='white',
                               fg='white',
                               font=('verdana', 11, 'bold'),
                               command=self.JanelaPredictionSetup)
        self.bt_novo2.place(relx=0.68, rely=0.25, relwidth=0.3, relheight=0.15)

        ## Botão Treino
        # Deve avisar se deseja executar um treino com um modelo já existente ou se irá criar um novo modelo
        #
        #

        self.bt_novo2 = Button(self.aba1,
                               text="Train",
                               bd=2,
                               bg='#1e3743',
                               activebackground='#108ecb',
                               activeforeground='white',
                               fg='white',
                               font=('verdana', 11, 'bold'),
                               command=self.JanelaTreinamento)
        self.bt_novo2.place(relx=0.68, rely=0.40, relwidth=0.3, relheight=0.15)

        ## Criando botao Treinamento
        #self.bt_treinamento = Button(self.aba1, text="Classify", bd=2, bg='#00FFFF',
        #                        activebackground='yellow', activeforeground='black',fg = 'black',
        #                        font = ('verdana',9,'bold'), command=self.JanelaClassificacao)
        #self.bt_treinamento.place(relx=0.5, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao files
        self.bt_files = Button(self.aba1,
                               text="Files",
                               bd=2,
                               font=('verdana', 9, 'bold'),
                               command=lambda: self.buscar_arquivos())
        self.bt_files.place(relx=0.5, rely=0.43, relwidth=0.1, relheight=0.15)

        ## Criação da label e entrada de código
        self.lb_codigo = Label(self.aba1,
                               text="Code",
                               bg="#DFEBE9",
                               fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        ## Criação da label e entrada da age -
        self.lb_idade = Label(self.aba1,
                              text="Age :",
                              bg="#DFEBE9",
                              fg='#107db2')
        self.age_entry = Entry(self.aba1)
        self.lb_idade.place(relx=0.05, rely=0.3)
        self.age_entry.place(relx=0.05, rely=0.45, relwidth=0.2)

        ## Criação da label e entrada da genero
        self.lb_genero = Label(self.aba1,
                               text="Gender :",
                               bg="#DFEBE9",
                               fg='#107db2')
        self.lb_genero.place(relx=0.05, rely=0.68)

        self.Tipvar = StringVar()
        self.TipV = ('Male', 'Woman')
        self.Tipvar.set("Male")
        self.popupMenu = OptionMenu(self.aba1, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.05, rely=0.80, relwidth=0.3)
        self.gender_entry = self.Tipvar.get()

        ## Criação da label e entrada da File
        self.lb_files = Label(self.aba1,
                              text="Files :",
                              bg="#DFEBE9",
                              fg='#107db2')
        self.lb_files.place(relx=0.5, rely=0.3)

        ## Criação da label e entrada da Info
        self.lb_info = Label(self.aba1,
                             text="Info :",
                             bg="#DFEBE9",
                             fg='#107db2')
        self.lb_info.place(relx=0.5, rely=0.6)
        self.info_entry = Entry(self.aba1)
        self.info_entry.place(relx=0.5, rely=0.75, relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2,
                                     height=3,
                                     column=("col1", "col2", "col3", "col4",
                                             "col5", "col6", "col7", "col8"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Cod")
        self.listaCli.heading("#2", text="Age")
        self.listaCli.heading("#3", text="Gender")
        self.listaCli.heading("#4", text="Info")
        self.listaCli.heading("#5", text="Accur.")
        self.listaCli.heading("#6", text="Recall")
        self.listaCli.heading("#7", text="Precision")
        self.listaCli.heading("#8", text="File")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=40)
        self.listaCli.column("#2", width=40)
        self.listaCli.column("#3", width=70)
        self.listaCli.column("#4", width=120)
        self.listaCli.column("#5", width=50)
        self.listaCli.column("#6", width=50)
        self.listaCli.column("#7", width=50)
        self.listaCli.column("#8", width=150)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96,
                               rely=0.1,
                               relwidth=0.04,
                               relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root2)
        self.root2.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit():
            self.root2.destroy()

        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_cascade(label="Reports", menu=filemenu2)
        filemenu.add_command(label="exit", command=Quit)
        filemenu2.add_command(label="Clean", command=self.limpa_cliente)
        filemenu2.add_command(label="Customer File",
                              command=self.gerarRelatorioCliente)

    def tela2(self):
        self.root2.title("Add Patient")
        self.root2.config(bg="#DFEBE9")
        self.root2.geometry("1024x768")
        self.root2.resizable(True, True)
        self.root2.maxsize(width=900, height=700)
        self.root2.minsize(width=500, height=400)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()

    def JanelaAddPaciente(self):
        self.root2 = Toplevel()
        self.tela2()
        self.frames_de_telaAddPat()
        self.widgets_frameAddPat()
        self.lista_frame2()
        self.select_lista()
        self.Menus()

    ################################################ TELA TreinamentoSetup

    def tela10(self):
        self.root6.title("Train")
        self.root6.config(bg="#DFEBE9")
        self.root6.geometry("1024x768")
        self.root6.resizable(True, True)
        self.root6.maxsize(width=300, height=300)
        self.root6.minsize(width=300, height=300)
        self.root6.transient(self.root2)
        self.root6.focus_force()
        self.root6.grab_set()

    def TelaTreino(self):

        canvasroot6 = Canvas(self.root6,
                             width=1000,
                             height=700,
                             relief='raised',
                             bg="#DFEBE9")
        canvasroot6.pack()

        def Validar():
            self.TreinamentoOcorrendo()
            time.sleep(200)
            self.TreinamentoModelo()
            print("Treinou")

        #Imagens logs=os
        width = 500
        height = 200

        # Title
        label2 = Label(self.root6,
                       text="""Select whether you want to create a new model 
        or use one that actually exists:""")
        label2.config(font=('helvetica', 9), bg="#DFEBE9")
        canvasroot6.create_window(100, 20, window=label2)

        ## Criação da label e entrada do tipo
        self.lb_type = Label(self.root6,
                             text="Model :",
                             bg="#DFEBE9",
                             fg='#107db2')
        self.lb_type.place(relx=0.05, rely=0.2)
        self.Tipvar = StringVar()
        self.TipV = ('New Model', 'Old Model')
        self.Tipvar.set("New Model")
        self.popupMenu = OptionMenu(self.root6, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.05, rely=0.3, relwidth=0.5)
        self.model_type_entry = self.Tipvar.get()

        ## Criasção da label e entrada do tipo
        self.lb_name = Label(self.root6,
                             text="Chose model name:",
                             bg="#DFEBE9",
                             fg='#107db2')
        self.lb_name.place(relx=0.05, rely=0.45)
        self.new_model_name = Entry(self.root6)
        self.new_model_name.place(relx=0.05, rely=0.55, relwidth=0.5)

        ## Criasção da label e entrada do tipo
        self.lb_model = Label(self.root6,
                              text="Select the file for train (namefile[0]):",
                              bg="#DFEBE9",
                              fg='#107db2')
        self.lb_model.place(relx=0.05, rely=0.65)
        self.bt_files = Button(self.root6,
                               text="Files",
                               bd=2,
                               font=('verdana', 9, 'bold'),
                               command=lambda: self.buscar_arquivo2())
        self.bt_files.place(relx=0.05, rely=0.75, relwidth=0.5, relheight=0.1)

        ## Criação da label e entrada do tipo

        self.Boton_done = Button(self.root6,
                                 text="Done",
                                 font=("AvantGarde", 9, "bold"),
                                 command=Validar,
                                 bg="#14787A",
                                 fg="#ffffff",
                                 width="15",
                                 height="1",
                                 cursor="hand2")
        self.Boton_done.place(relx=0.70,
                              rely=0.8,
                              relwidth=0.20,
                              relheight=0.10)

    def JanelaTreinamento(self):
        self.root6 = Toplevel()
        self.tela10()
        self.TelaTreino()

    ################################################ TELA ClassficacaoSetup

    def tela11(self):
        self.root7.title("Classification")
        self.root7.config(bg="#DFEBE9")
        self.root7.geometry("1024x768")
        self.root7.resizable(True, True)
        self.root7.maxsize(width=300, height=300)
        self.root7.minsize(width=300, height=300)
        self.root7.transient(self.root2)
        self.root7.focus_force()
        self.root7.grab_set()

    def TelaClassificacao(self):
        canvasroot7 = Canvas(self.root7,
                             width=1000,
                             height=700,
                             relief='raised',
                             bg="#DFEBE9")
        canvasroot7.pack()

        def Classificando():
            self.JanelaClassificacao()
            print("ACCURACY ENTRY: " + self.accuracy_entry)
            print("RECALL ENTRY: " + self.recall_entry)
            print("PRECISION ENTRY: " + self.precision_entry)
            self.accuracy_entry = self.accurancyValue_Entry
            self.recall_entry = self.recallValue_Entry
            self.precision_entry = self.precisionValue_Entry
            print("ACCURACY ENTRY: " + self.accuracy_entry)
            print("RECALL ENTRY: " + self.recall_entry)
            print("PRECISION ENTRY: " + self.precision_entry)
            print("Add Cliente")
            self.add_cliente()
            print("Finalizou Treino e salvou cliente")

        #Imagens logs=os
        width = 500
        height = 200

        # Title
        label2 = Label(
            self.root7,
            text="""Choose a pre-existing model to classify your data.
        If you wanted to create a new model , go back and 
        select the Training option""")
        label2.config(font=('helvetica', 9), bg="#DFEBE9")
        canvasroot7.create_window(145, 40, window=label2)

        ## Criasção da label e entrada do tipo
        self.lb_name = Label(self.root7,
                             text="Select Model Name",
                             bg="#DFEBE9",
                             fg='#107db2')
        self.lb_name.place(relx=0.05, rely=0.25)
        self.existed_model_name = Entry(self.root7)
        self.existed_model_name.place(relx=0.05, rely=0.35, relwidth=0.5)

        ## Botão de Seleção dos Arquivos para Classificação

        ## Criação da label e entrada do tipo

        self.Boton_done = Button(self.root7,
                                 text="Done",
                                 font=("AvantGarde", 9, "bold"),
                                 command=Classificando,
                                 bg="#14787A",
                                 fg="#ffffff",
                                 width="15",
                                 height="1",
                                 cursor="hand2")
        self.Boton_done.place(relx=0.70,
                              rely=0.8,
                              relwidth=0.20,
                              relheight=0.10)

    def JanelaClassificacaoSetup(self):
        self.root7 = Toplevel()
        self.tela11()
        self.TelaClassificacao()

    ################################################ TELA ClassficacaoSetup

    def tela13(self):
        self.root10.title("Prediction")
        self.root10.config(bg="#DFEBE9")
        self.root10.geometry("1024x768")
        self.root10.resizable(True, True)
        self.root10.maxsize(width=300, height=300)
        self.root10.minsize(width=300, height=300)
        self.root10.transient(self.root2)
        self.root10.focus_force()
        self.root10.grab_set()

    def TelaPrediction(self):
        canvasroot10 = Canvas(self.root10,
                              width=1000,
                              height=700,
                              relief='raised',
                              bg="#DFEBE9")
        canvasroot10.pack()

        def Prediction():
            self.JanelaPrediction()
            print("ACCURACY ENTRY: " + self.accuracy_entry)
            print("RECALL ENTRY: " + self.recall_entry)
            print("PRECISION ENTRY: " + self.precision_entry)
            self.accuracy_entry = self.accurancyValue_Entry
            self.recall_entry = self.recallValue_Entry
            self.precision_entry = self.precisionValue_Entry
            print("ACCURACY ENTRY: " + self.accuracy_entry)
            print("RECALL ENTRY: " + self.recall_entry)
            print("PRECISION ENTRY: " + self.precision_entry)
            print("Add Cliente")
            self.add_cliente()
            print("Finalizou Treino e salvou cliente")

        #Imagens logs=os
        width = 500
        height = 200

        # Title
        label2 = Label(
            self.root10,
            text="""Choose a pre-existing model to pretict your data.
        If you wanted to create a new model , go back and 
        select the Training option""")
        label2.config(font=('helvetica', 9), bg="#DFEBE9")
        canvasroot10.create_window(145, 40, window=label2)

        ## Criasção da label e entrada do tipo
        self.lb_name = Label(self.root10,
                             text="Select Model Name",
                             bg="#DFEBE9",
                             fg='#107db2')
        self.lb_name.place(relx=0.05, rely=0.25)
        self.existed_model_name = Entry(self.root10)
        self.existed_model_name.place(relx=0.05, rely=0.35, relwidth=0.5)

        ## Botão de Seleção dos Arquivos para Classificação

        ## Criação da label e entrada do tipo

        self.Boton_done = Button(self.root10,
                                 text="Done",
                                 font=("AvantGarde", 9, "bold"),
                                 command=Prediction,
                                 bg="#14787A",
                                 fg="#ffffff",
                                 width="15",
                                 height="1",
                                 cursor="hand2")
        self.Boton_done.place(relx=0.70,
                              rely=0.8,
                              relwidth=0.20,
                              relheight=0.10)

    def JanelaPredictionSetup(self):
        self.root10 = Toplevel()
        self.tela13()
        self.TelaPrediction()

    ############################################### ABOUT
    def tela3(self):
        self.root3.title("About")
        self.root3.config(bg="#DFEBE9")
        self.root3.geometry("1024x768")
        self.root3.resizable(0, 0)
        self.root3.transient(self.root)
        self.root3.focus_force()
        self.root3.grab_set()

    def Tela(self):
        canvasroot3 = Canvas(self.root3,
                             width=1000,
                             height=700,
                             relief='raised',
                             bg="#DFEBE9")
        canvasroot3.pack()

        self.Boton_close = Button(self.root3,
                                  text="Close",
                                  font=("AvantGarde", 20, "bold"),
                                  command=self.root3.destroy,
                                  bg="#14787A",
                                  fg="#ffffff",
                                  width="15",
                                  height="1",
                                  cursor="hand2")
        self.Boton_close.place(relx=0.70,
                               rely=0.8,
                               relwidth=0.20,
                               relheight=0.10)

        #Imagens logs=os
        width = 400
        height = 400

        # IMAGEM 1
        img = Image.open("logos/logos_unidas.png")
        img = img.resize((width, height), Image.ANTIALIAS)
        self.accurancy = ImageTk.PhotoImage(img)
        canvasroot3.imageList = []
        canvasroot3.pack()
        #canvasroot3.create_image(1055, 300, anchor="e", image=self.accurancy)
        canvasroot3.create_image(1020, 300, anchor="e", image=self.accurancy)
        canvasroot3.imageList.append(self.accurancy)

        # About
        label2 = Label(self.root3, text="About the porject:")
        label2.config(font=('helvetica', 14), bg="#DFEBE9")
        canvasroot3.create_window(180, 100, window=label2)

        #about text in image
        width = 600
        height = 600
        img4 = Image.open("logos/about.png")
        img4 = img4.resize((width, height), Image.ANTIALIAS)

        self.accurancy4 = ImageTk.PhotoImage(img4)
        canvasroot3.imageList = []
        canvasroot3.pack()
        canvasroot3.create_image(670, 380, anchor="e", image=self.accurancy4)
        canvasroot3.imageList.append(self.accurancy4)

    def JanelaAbout(self):
        self.root3 = Toplevel()
        self.tela3()
        self.Tela()

    ############################################### SHOW PAT
    def frames_de_telaShowPat(self):
        self.frame_1 = Frame(self.root4,
                             bd=4,
                             bg='#DFEBE9',
                             highlightbackground='#759fe6',
                             highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.25)

        self.frame_2 = Frame(self.root4, bd=4, bg='#DFEBE9')
        self.frame_2.place(relx=0.02, rely=0.3, relwidth=0.96, relheight=0.65)

    def widgets_frameShowPat(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#DFEBE9')
        self.aba2.configure(background="lightgray")

        self.abas.add(self.aba1, text=" ")
        self.abas.add(self.aba2, text=" ")

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        self.codigo_entry = Entry(self.aba1)
        self.Tipvar1 = StringVar()
        self.Tipvar1.set("Child: 0-18")
        self.age_entry = self.Tipvar1.get()

        self.info_entry = Entry(self.aba1)

        self.Tipvar = StringVar()
        self.Tipvar.set("Male")
        self.gender_entry = self.Tipvar.get()

        self.canvas_bt = Canvas(self.aba1,
                                bd=0,
                                bg='#1e3743',
                                highlightbackground='gray',
                                highlightthickness=5)

        self.canvas_bt.place(relx=0.19,
                             rely=0.2,
                             relwidth=0.32,
                             relheight=0.40)
        ## Criando botao limpar bg="#14787A", fg="#ffffff"
        self.bt_lipar = Button(self.aba1,
                               text="Clean",
                               bd=2,
                               bg="#14787A",
                               activebackground='#108ecb',
                               activeforeground='white',
                               fg="#ffffff",
                               font=('verdana', 9, 'bold'),
                               command=self.limpa_cliente)
        self.bt_lipar.place(relx=0.2, rely=0.24, relwidth=0.1, relheight=0.30)

        ## Criando botao buscar
        self.bt_buscar = Button(self.aba1,
                                text="Search",
                                bd=2,
                                bg="#14787A",
                                activebackground='#108ecb',
                                activeforeground='white',
                                fg="#ffffff",
                                font=('verdana', 9, 'bold'),
                                command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.24, relwidth=0.1, relheight=0.30)

        texto_balao_buscar = "Type in the code field the patient you want to search"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar,
                                      balloonmsg=texto_balao_buscar)

        ## Criando botao apagar
        self.bt_apagar = Button(self.aba1,
                                text="Delete",
                                bd=2,
                                bg='#14787A',
                                activebackground='#108ecb',
                                activeforeground='white',
                                fg='white',
                                font=('verdana', 9, 'bold'),
                                command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.4, rely=0.24, relwidth=0.1, relheight=0.30)

        ## Criação da label e entrada de código
        self.lb_codigo = Label(self.aba1,
                               text="Code",
                               bg="#DFEBE9",
                               fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.10)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.30, relwidth=0.08)

    def lista_frame4(self):
        self.listaCli = ttk.Treeview(self.frame_2,
                                     height=3,
                                     column=("col1", "col2", "col3", "col4",
                                             "col5", "col6", "col7", "col8"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Cod")
        self.listaCli.heading("#2", text="Age")
        self.listaCli.heading("#3", text="Gender")
        self.listaCli.heading("#4", text="Info")
        self.listaCli.heading("#5", text="Accur.")
        self.listaCli.heading("#6", text="Recall")
        self.listaCli.heading("#7", text="Precision")
        self.listaCli.heading("#8", text="File")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=40)
        self.listaCli.column("#2", width=40)
        self.listaCli.column("#3", width=70)
        self.listaCli.column("#4", width=120)
        self.listaCli.column("#5", width=50)
        self.listaCli.column("#6", width=50)
        self.listaCli.column("#7", width=50)
        self.listaCli.column("#8", width=150)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96,
                               rely=0.1,
                               relwidth=0.04,
                               relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def MenusShowPaciente(self):
        menubar = Menu(self.root4)
        self.root4.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu = Menu(menubar)

        def Quit():
            self.root4.destroy()

        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_cascade(label="Reports", menu=filemenu2)
        filemenu.add_command(label="exit", command=Quit)
        filemenu2.add_command(label="Clean", command=self.limpa_cliente)
        filemenu2.add_command(label="Customer File",
                              command=self.gerarRelatorioCliente)

    def tela4(self):
        self.root4.title("Show")
        self.root4.config(bg="#DFEBE9")
        self.root4.geometry("1024x768")
        self.root4.resizable(True, True)
        self.root4.maxsize(width=900, height=700)
        self.root4.minsize(width=500, height=400)
        self.root4.transient(self.root)
        self.root4.focus_force()
        self.root4.grab_set()

    def JanelaShowPaciente(self):
        self.root4 = Toplevel()
        self.tela4()
        self.frames_de_telaShowPat()
        self.widgets_frameShowPat()
        self.lista_frame4()
        self.select_lista()
        self.MenusShowPaciente()

    # JANELA DA CLASSIFICACAO
    def frames_de_telaClassification(self):
        self.frame_1 = Frame(self.root5, bd=4, bg='#DFEBE9')
        self.frame_1.place(relx=0.70, rely=0.02, relwidth=0.27, relheight=0.80)

    def MenusClassification(self):
        menubar = Menu(self.root5)
        self.root5.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit():
            self.root5.destroy()

        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_cascade(label="Reports", menu=filemenu2)
        filemenu.add_command(label="exit", command=Quit)
        filemenu2.add_command(label="Clean", command=self.limpa_cliente)
        filemenu2.add_command(label="Customer File",
                              command=self.gerarRelatorioCliente)

    def tela5(self):
        self.root5.title("Classification")
        self.root5.config(bg="#DFEBE9")
        self.root5.geometry("1024x768")
        self.root5.resizable(True, True)
        self.root5.maxsize(width=900, height=700)
        self.root5.minsize(width=500, height=400)
        self.root5.transient(self.root2)
        self.root5.focus_force()
        self.root5.grab_set()

    def Classificacao(self):
        canvas4 = Canvas(self.root5,
                         width=1000,
                         height=500,
                         relief='raised',
                         bg="#DFEBE9")
        canvas4.pack()
        # ------ Load the trained CNN model
        print(self.existed_model_name.get())
        network_name = self.existed_model_name.get()
        model = tf.keras.models.load_model(network_name)

        # ---- Load data files
        data = self.nomeArquivoEDF
        event = LeituraArquivos.LoadEvento(self.nomeArquivoTSE)
        # print(event)

        # --- read EEG data
        raw = mne.io.read_raw_edf(data, preload=True)
        raw.rename_channels(lambda s: s.strip("."))
        #raw.set_montage("standard_1020")
        #raw.set_eeg_reference("average")
        print(raw)  # print raw data
        print(raw.info)  # print edf info

        # ---- sampling rate
        fs = raw.info['sfreq']  # sampling frequency
        duration = len(
            raw) / fs  # recording duration of hole eeg data in seconds

        # ---- EEG data
        eeg = raw.get_data()

        # ---- Remove 60 Hz noise
        signal_filter = processing.butter_bandstop_filter(eeg, 59, 61, fs, 5)
        signal_filter = signal_filter[0:21, :]  #Limit at 21 channels

        #------ Signal Bands
        delta_teta = processing.butter_bandpass_filter(signal_filter, 1, 7, fs,
                                                       5)
        alpha_beta = processing.butter_bandpass_filter(signal_filter, 8, 30,
                                                       fs, 5)
        gamma = processing.butter_bandpass_filter(signal_filter, 31, 100, fs,
                                                  5)
        # ------ Applied STFT to signal bands
        f, t, Zxx_delta_teta = processing.STFT(delta_teta, fs)
        f, t, Zxx_alpha_beta = processing.STFT(alpha_beta, fs)
        f, t, Zxx_gamma = processing.STFT(gamma, fs)

        # ------- Create event vector 0 and 1
        event_vec = processing.EventVector(event, t)

        # ------- Cut first 1 minute
        Zxx_delta_teta = Zxx_delta_teta[60:, :, :]
        Zxx_alpha_beta = Zxx_alpha_beta[60:, :, :]
        Zxx_gamma = Zxx_gamma[60:, :, :]
        event_vec = event_vec[60:]

        # ------- Create the input network
        Zxx_size = Zxx_delta_teta.shape
        Input_net = np.zeros((Zxx_size[0], Zxx_size[1], Zxx_size[2], 3))
        Input_net[:, :, :, 0] = Zxx_delta_teta
        Input_net[:, :, :, 1] = Zxx_alpha_beta
        Input_net[:, :, :, 2] = Zxx_gamma

        # -------- Classify events
        cm, predictions, precision, recall, f_score = network.classify(
            model, Input_net, event_vec)
        cm_plot_labels = ["Seizure-free", "Seizure"]
        network.plot_confusion_matrix(cm,
                                      cm_plot_labels,
                                      title="Confusion Matrix")

        plt.savefig('Resultado.png')

        TP = cm[1][1]
        TN = cm[0][0]
        FN = cm[1][0]
        FP = cm[0][1]

        #plots.plot_predict(t, event_vec, predictions)
        # -------- metrics
        accuracy = (TP + TN) / (TP + FP + TN + FN) * 100
        formatted_accuracy = "{:.2f}".format(accuracy)
        accuracy = formatted_accuracy

        recall = TP / (TP + FN) * 100  #also know as recall
        specificity = TN / (TN + FP) * 100
        precision = TP / (TP + FP) * 100
        error = (FP + FN) / (TP + FP + TN + FN)
        #F1 = 2 * (precision * recall) / (precision + recall)
        print("acc: ", accuracy)
        print("recall:", recall)
        print("precision:", precision)
        print('F1-score:', f_score)
        #
        #print("spec:", specificity)
        print("error:", error)

        Resultado = "Resultado.png"
        width = 600
        height = 400
        img = Image.open(Resultado)
        img = img.resize((width, height), Image.ANTIALIAS)
        self.accurancy = ImageTk.PhotoImage(img)
        canvas4.imageList = []
        canvas4.pack()
        canvas4.create_image(200, 230, anchor="w", image=self.accurancy)
        canvas4.imageList.append(self.accurancy)

        label2 = Label(self.root5, text='accurancy:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas4.create_window(100, 100, window=label2)
        label4 = Label(self.root5, text=accuracy)
        self.accurancyValue_Entry = accuracy
        formatted_recall = "{:.2f}".format(recall)
        recall = formatted_recall
        formatted_precision = "{:.2f}".format(precision)
        precision = formatted_precision
        self.recallValue_Entry = formatted_recall
        self.precisionValue_Entry = formatted_precision * 100
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas4.create_window(100, 130, window=label4)

        label2 = Label(self.root5, text='recall:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas4.create_window(100, 200, window=label2)
        label4 = Label(self.root5, text=recall)
        self.recallValue_Entry = recall
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas4.create_window(100, 230, window=label4)

        label2 = Label(self.root5, text='precision:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas4.create_window(100, 300, window=label2)
        label4 = Label(self.root5, text=precision)
        self.precisionValue_Entry = precision
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas4.create_window(100, 330, window=label4)

        self.precision = self.precisionValue_Entry
        self.recall = self.recallValue_Entry
        self.accuracy = self.accurancyValue_Entry
        self.nomeArquivo = self.nomeArquivoEDF

        ## Criando botao alterar
        self.Boton_close = Button(self.root5,
                                  text="Close",
                                  font=("AvantGarde", 20, "bold"),
                                  command=self.root5.destroy,
                                  bg="#14787A",
                                  fg="#ffffff",
                                  width="15",
                                  height="1",
                                  cursor="hand2")
        self.Boton_close.place(relx=0.70,
                               rely=0.8,
                               relwidth=0.20,
                               relheight=0.10)

    def JanelaClassificacao(self):
        self.root5 = Toplevel()
        self.tela5()
        self.frames_de_telaClassification()
        self.MenusClassification()
        self.Classificacao()

    # JANELA DO PREDICITION
    def frames_de_telaPrediction(self):
        self.frame_1 = Frame(self.root9, bd=4, bg='#DFEBE9')
        self.frame_1.place(relx=0.70, rely=0.02, relwidth=0.27, relheight=0.80)

        self.Boton_info.place(relx=0.02,
                              rely=0.2,
                              relwidth=0.98,
                              relheight=0.10)

        self.Boton_close.place(relx=0.02,
                               rely=0.8,
                               relwidth=0.98,
                               relheight=0.10)

    def MenusPrediction(self):
        menubar = Menu(self.root9)
        self.root9.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit():
            self.root9.destroy()

        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_cascade(label="Reports", menu=filemenu2)
        filemenu.add_command(label="exit", command=Quit)
        filemenu2.add_command(label="Clean", command=self.limpa_cliente)
        filemenu2.add_command(label="Customer File",
                              command=self.gerarRelatorioCliente)

    def tela6(self):
        self.root9.title("Prediction")
        self.root9.config(bg="#DFEBE9")
        self.root9.geometry("1024x768")
        self.root9.resizable(True, True)
        self.root9.maxsize(width=900, height=700)
        self.root9.minsize(width=500, height=400)
        self.root9.transient(self.root2)
        self.root9.focus_force()
        self.root9.grab_set()

    def Treinamento2(self):
        canvas3 = Canvas(self.root9,
                         width=1000,
                         height=500,
                         relief='raised',
                         bg="#DFEBE9")
        canvas3.pack()

        print("TREINAMENTO2 START ---------------------")
        # ------ Load the trained CNN model
        print(self.existed_model_name.get())
        network_name = self.existed_model_name.get()
        model = tf.keras.models.load_model(network_name)

        # ---- Load data files
        data = self.nomeArquivoEDF
        event = LeituraArquivos.LoadEvento(self.nomeArquivoTSE)
        # print(event)

        # --- read EEG data
        raw = mne.io.read_raw_edf(data, preload=True)
        raw.rename_channels(lambda s: s.strip("."))
        #raw.set_montage("standard_1020")
        #raw.set_eeg_reference("average")
        print(raw)  # print raw data
        print(raw.info)  # print edf info

        # ---- sampling rate
        fs = raw.info['sfreq']  # sampling frequency
        duration = len(
            raw) / fs  # recording duration of hole eeg data in seconds

        # ---- EEG data
        eeg = raw.get_data()

        # ---- Remove 60 Hz noise
        signal_filter = processing.butter_bandstop_filter(eeg, 59, 61, fs, 5)
        signal_filter = signal_filter[0:21, :]  #Limit at 21 channels

        #------ Signal Bands
        delta_teta = processing.butter_bandpass_filter(signal_filter, 1, 7, fs,
                                                       5)
        alpha_beta = processing.butter_bandpass_filter(signal_filter, 8, 30,
                                                       fs, 5)
        gamma = processing.butter_bandpass_filter(signal_filter, 31, 100, fs,
                                                  5)
        # ------ Applied STFT to signal bands
        f, t, Zxx_delta_teta = processing.STFT(delta_teta, fs)
        f, t, Zxx_alpha_beta = processing.STFT(alpha_beta, fs)
        f, t, Zxx_gamma = processing.STFT(gamma, fs)

        # ------- Create event vector 0 and 1
        event_vec = processing.EventVector(event, t)

        # ------- Cut first 1 minute
        Zxx_delta_teta = Zxx_delta_teta[60:, :, :]
        Zxx_alpha_beta = Zxx_alpha_beta[60:, :, :]
        Zxx_gamma = Zxx_gamma[60:, :, :]
        event_vec = event_vec[60:]

        # ------- Create the input network
        Zxx_size = Zxx_delta_teta.shape
        Input_net = np.zeros((Zxx_size[0], Zxx_size[1], Zxx_size[2], 3))
        Input_net[:, :, :, 0] = Zxx_delta_teta
        Input_net[:, :, :, 1] = Zxx_alpha_beta
        Input_net[:, :, :, 2] = Zxx_gamma

        # -------- Classify events
        cm, predictions, precision, recall, f_score = network.classify(
            model, Input_net, event_vec)
        #cm_plot_labels = ["Seizure-free", "Seizure"]
        #network.plot_confusion_matrix(cm,
        #                              cm_plot_labels,
        #                              title="Confusion Matrix")

        #plt.savefig('Resultado.png')

        TP = cm[1][1]
        TN = cm[0][0]
        FN = cm[1][0]
        FP = cm[0][1]

        print(
            "---------------------------- PREDICT IMAGE --------------------")
        plots.plot_predict(t, event_vec, predictions)
        print("---------------------------- IMAGE DONE --------------------")
        # -------- metrics
        accuracy = (TP + TN) / (TP + FP + TN + FN) * 100
        formatted_accuracy = "{:.2f}".format(accuracy)
        accuracy = formatted_accuracy

        recall = TP / (TP + FN) * 100  #also know as recall
        specificity = TN / (TN + FP) * 100
        precision = TP / (TP + FP) * 100
        error = (FP + FN) / (TP + FP + TN + FN)
        #F1 = 2 * (precision * recall) / (precision + recall)
        print("acc: ", accuracy)
        print("recall:", recall)
        print("precision:", precision)
        print('F1-score:', f_score)
        #
        #print("spec:", specificity)
        print("error:", error)

        ## Criando botao alterar
        self.Boton_close = Button(self.root9,
                                  text="Close",
                                  font=("AvantGarde", 20, "bold"),
                                  command=self.root9.destroy,
                                  bg="#14787A",
                                  fg="#ffffff",
                                  width="15",
                                  height="1",
                                  cursor="hand2")
        self.Boton_close.place(relx=0.70,
                               rely=0.8,
                               relwidth=0.20,
                               relheight=0.10)

        ## Criando botao alterar
        #self.canvas_bt = Canvas(self.root9, bd=0, bg='blue')
        #self.canvas_bt.place(relx=0.1, rely=0.8, relwidth=0.02, relheight=0.02)

        ## Criando botao alterar
        #self.canvas_bt = Canvas(self.root9, bd=0, bg='green')
        #self.canvas_bt.place(relx=0.1,
        #                     rely=0.86,
        #                     relwidth=0.02,
        #                     relheight=0.02)

        ## Criando botao alterar
        #self.canvas_bt = Canvas(self.root9, bd=0, bg='red')
        #self.canvas_bt.place(relx=0.1,
        #                     rely=0.92,
        #                     relwidth=0.02,
        #                     relheight=0.02)

        #self.Botao = Button(self.root9,
        #                    text="Normal",
        #                    font=("AvantGarde", 10, "bold"),
        #                    bg='#DFEBE9',
        #                    width="5",
        #                    height="1")
        #self.Botao.place(relx=0.15, rely=0.78, relwidth=0.1, relheight=0.05)

        #self.Botao = Button(self.root9,
        #                    text="Predictions",
        #                    font=("AvantGarde", 10, "bold"),
        #                    bg='#DFEBE9',
        #                    width="5",
        #                    height="1")
        #self.Botao.place(relx=0.15, rely=0.84, relwidth=0.1, relheight=0.05)

        #self.Botao = Button(self.root9,
        #                    text="Ictal",
        #                    font=("AvantGarde", 10, "bold"),
        #                    bg='#DFEBE9',
        #                    width="5",
        #                    height="1")
        #self.Botao.place(relx=0.15, rely=0.91, relwidth=0.1, relheight=0.05)

        #labelNew2 = Label(self.root9, text='Normal')
        #labelNew2.config(font=('helvetica',14),bg="#DFEBE9")
        #canvas3.create_window(2, 10, window=labelNew2)

        #labelNew3 = Label(self.root9, text='Normal')
        #labelNew3.config(font=('helvetica',14),bg="#DFEBE9")
        #canvas3.create_window(2, 10, window=labelNew3)

        Resultado = "Prediction.png"
        width = 600
        height = 400
        img = Image.open(Resultado)
        img = img.resize((width, height), Image.ANTIALIAS)
        self.accurancy = ImageTk.PhotoImage(img)
        canvas3.imageList = []
        canvas3.pack()
        canvas3.create_image(200, 230, anchor="w", image=self.accurancy)
        canvas3.imageList.append(self.accurancy)

        label2 = Label(self.root9, text='Accurancy:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas3.create_window(100, 100, window=label2)
        label4 = Label(self.root9, text=accuracy)
        self.accurancyValue_Entry = accuracy
        formatted_recall = "{:.2f}".format(recall)
        recall = formatted_recall
        formatted_precision = "{:.2f}".format(precision)
        precision = formatted_precision
        self.recallValue_Entry = formatted_recall
        self.precisionValue_Entry = formatted_precision * 100
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas3.create_window(100, 130, window=label4)

        label2 = Label(self.root9, text='Recall:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas3.create_window(100, 200, window=label2)
        label4 = Label(self.root9, text=recall)
        self.recallValue_Entry = recall
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas3.create_window(100, 230, window=label4)

        label2 = Label(self.root9, text='Precision:')
        label2.config(font=("AvantGarde", 18, "bold"),
                      fg="#14787A",
                      bg="#DFEBE9")
        canvas3.create_window(100, 300, window=label2)
        label4 = Label(self.root9, text=precision)
        self.precisionValue_Entry = precision
        label4.config(font=("AvantGarde", 14, "bold"), bg="#DFEBE9")
        canvas3.create_window(100, 330, window=label4)

    def JanelaPrediction(self):
        self.root9 = Toplevel()
        self.tela6()
        self.frames_de_telaPrediction()
        self.MenusPrediction()
        self.Treinamento2()

    # JANELA DO TREINAMENTO
    def TreinamentoModelo(self):
        # 1) Pegar nome do File
        # 2) Conferir se ele existe na pasta
        # 3) Se Não existir e se esperava um File, mandar mensagem
        # 4) Se tiver arquvi ler e passar pelo keras
        # 5) Se não tiver e não precisar criar um novo
        #            print(self.Tipvar.get())
        #    print(self.new_model_name.get())

        network_name = self.new_model_name.get()
        type_network = self.Tipvar.get()
        print("Entrei")
        print(network_name)
        print(self.Tipvar.get())

        if type_network == "Old Model":
            flag = 1
        else:
            flag = 0

        if flag == 0:
            #---- CNN model
            model = network.Model()
            print("New model")
        else:
            model = tf.keras.models.load_model(network_name)
            print("Trained model")

        Zxx_delta_teta_v = []
        Zxx_alpha_beta_v = []
        Zxx_gamma_v = []
        event_vec_v = []

        for i in range(0, 20):
            # ---- Load data files
            #data = load.loadEDF()
            #self.ditArquivoEDF
            diretorioEDF = self.ditArquivoEDF
            diretorioTSE = self.ditArquivoTSE

            arquivoEDF = diretorioEDF + "/train_" + str(i + 1) + ".edf"
            arquivoTSE = diretorioTSE + "/train_" + str(i + 1) + ".tse"

            data_doc = open(arquivoEDF, 'r')
            data = data_doc.name
            f_tse_doc = open(arquivoTSE, 'r')
            event = load.read_event(f_tse_doc.name)
            # print(event)

            # --- read EEG data
            raw = mne.io.read_raw_edf(data, preload=True)
            raw.rename_channels(lambda s: s.strip("."))
            #raw.set_montage("standard_1020")
            #raw.set_eeg_reference("average")
            print(raw)  # print raw data
            print(raw.info)  # print edf info

            # ---- sampling rate
            fs = raw.info['sfreq']  # sampling frequency
            duration = len(
                raw) / fs  # recording duration of hole eeg data in seconds

            # ---- EEG data
            eeg = raw.get_data()

            # ---- Remove 60 Hz noise
            signal_filter = processing.butter_bandstop_filter(
                eeg, 59, 61, fs, 5)
            signal_filter = signal_filter[0:21, :]  #Limit at 21 channels

            #------ Signal Bands
            delta_teta = processing.butter_bandpass_filter(
                signal_filter, 1, 7, fs, 5)
            alpha_beta = processing.butter_bandpass_filter(
                signal_filter, 8, 30, fs, 5)
            gamma = processing.butter_bandpass_filter(signal_filter, 31, 100,
                                                      fs, 5)
            # ------ Applied STFT to signal bands
            f, t, Zxx_delta_teta = processing.STFT(delta_teta, fs)
            f, t, Zxx_alpha_beta = processing.STFT(alpha_beta, fs)
            f, t, Zxx_gamma = processing.STFT(gamma, fs)

            # ------- Create event vector 0 and 1
            event_vec = processing.EventVector(event, t)

            # ------- Cut first 1 minute
            Zxx_delta_teta = Zxx_delta_teta[60:, :, :]
            Zxx_alpha_beta = Zxx_alpha_beta[60:, :, :]
            Zxx_gamma = Zxx_gamma[60:, :, :]
            event_vec = event_vec[60:]

            Zxx_delta_teta_v.append(Zxx_delta_teta)
            Zxx_alpha_beta_v.append(Zxx_alpha_beta)
            Zxx_gamma_v.append(Zxx_gamma)
            event_vec_v.append(event_vec)
            print(i)

        Zxx_delta_teta_total = np.concatenate(
            (Zxx_delta_teta_v[0], Zxx_delta_teta_v[1]), axis=0)
        Zxx_alpha_beta_total = np.concatenate(
            (Zxx_alpha_beta_v[0], Zxx_alpha_beta_v[1]), axis=0)
        Zxx_gamma_total = np.concatenate((Zxx_gamma_v[0], Zxx_gamma_v[1]),
                                         axis=0)
        event_vec_total = (event_vec_v[0] + event_vec_v[1])

        arch_number = len(Zxx_delta_teta_v)

        for i in range(2, arch_number):
            Zxx_delta_teta_total = np.concatenate(
                (Zxx_delta_teta_total, Zxx_delta_teta_v[i]), axis=0)
            Zxx_alpha_beta_total = np.concatenate(
                (Zxx_alpha_beta_total, Zxx_alpha_beta_v[i]), axis=0)
            Zxx_gamma_total = np.concatenate((Zxx_gamma_total, Zxx_gamma_v[i]),
                                             axis=0)
            event_vec_total += event_vec_v[i]

        # ------- Create the input network
        Zxx_size = Zxx_delta_teta_total.shape
        Input_net = np.zeros((Zxx_size[0], Zxx_size[1], Zxx_size[2], 3))
        Input_net[:, :, :, 0] = Zxx_delta_teta_total
        Input_net[:, :, :, 1] = Zxx_alpha_beta_total
        Input_net[:, :, :, 2] = Zxx_gamma_total

        # -------- Train CNN model
        [acc, val_acc, loss1,
         val_loss1], model = network.train(model, Input_net, event_vec_total)
        #os.makedirs('models/')
        model.save(network_name)

        # -------- Learning plots
        #plots.plot_acc_curve(acc, val_acc)
        #plots.plot_loss_curve(loss1, val_loss1)

        # -------- Tela
        sinal_delta_theta = Zxx_delta_teta_total
        sinal_alpha_beta = Zxx_alpha_beta_total
        sinal_gama = Zxx_gamma_total
        delta_theta_dividido = ProcessamentoDoSinal.dividir_sinal(
            sinal_delta_theta, fs)

        alpha_beta_dividido = ProcessamentoDoSinal.dividir_sinal(
            sinal_alpha_beta, fs)
        gama_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_gama, fs)
        AssociaTrechoEvento.associa_trecho_evento(delta_theta_dividido,
                                                  eventos)
        AssociaTrechoEvento.associa_trecho_evento(alpha_beta_dividido, eventos)
        AssociaTrechoEvento.associa_trecho_evento(gama_dividido, eventos)
        dados = CriaImagen.cria_imagens_saidas(gama_dividido,
                                               delta_theta_dividido,
                                               alpha_beta_dividido)

        fft_imagens = []
        for i in range(0, len(dados[0])):
            fft = np.fft.fftn(dados[0][i])
            fft = np.log(np.abs(np.fft.fftshift(fft)**2))
            img_fft = tf.keras.preprocessing.image.array_to_img(fft)
            array_fft = tf.keras.preprocessing.image.img_to_array(img_fft)
            array_fft = array_fft * (1.0 / 255)
            fft_imagens.append(array_fft)

        fft_imagens = np.array(fft_imagens)
        UsaRede.treina_rede(fft_imagens, dados[1])
        cm = UsaRede.classifica_dados(fft_imagens, dados[1])
        predictions = UsaRede.classifica_sem_saidas(fft_imagens)
        cm_plot_labels = ["Normal", "Epilepsy"]
        #ConfusionMatrix.plot_confusion_matrix(cm,
        #                                      cm_plot_labels,
        #                                      title="Confusion Matrix")
        TP = cm[1][1]
        TN = cm[0][0]
        FP = cm[1][0]
        FN = cm[0][1]
        accuracy = (TP + TN) / (TP + FP + TN + FN) * 100
        formatted_accuracy = "{:.2f}".format(accuracy)
        accuracy = formatted_accuracy
        recall = TP / (TP + FN) * 100  # ADD DATASET
        precision = TP / (TP + FP) * 100
        if TP == 0:
            recall = 0
        else:
            recall = TP / (TP + FN) * 100  # ADD DATASET
        predictions = UsaRede.classifica_sem_saidas(fft_imagens)
        predictions = np.array(predictions)
        self.accurancyValue_Entry = accuracy
        formatted_recall = "{:.2f}".format(recall)
        recall = formatted_recall
        formatted_precision = "{:.2f}".format(precision)
        precision = formatted_precision
        self.recallValue_Entry = formatted_recall
        self.precisionValue_Entry = formatted_precision * 100
        self.recallValue_Entry = recall
        self.precisionValue_Entry = precision

    # Janela Treinamento Carregando
    def tela12(self):
        self.root8.title("Training Loading")
        self.root8.config(bg="#DFEBE9")
        self.root8.geometry("1024x768")
        self.root8.resizable(True, True)
        self.root8.maxsize(width=300, height=300)
        self.root8.minsize(width=300, height=300)
        self.root8.transient(self.root2)
        self.root8.focus_force()
        self.root8.grab_set()

    def TelaClassificacaoResults(self):
        canvasroot8 = Canvas(self.root8,
                             width=1000,
                             height=700,
                             relief='raised',
                             bg="#DFEBE9")
        canvasroot8.pack()

        #Imagens logs=os
        width = 500
        height = 200

        # Title
        label2 = Label(
            self.root8,
            text="""The training will take a few minutes, please wait 
            until the confirmation window appears """)
        label2.config(font=('helvetica', 9), bg="#DFEBE9")
        canvasroot8.create_window(145, 40, window=label2)

    def TreinamentoOcorrendo(self):
        self.root8 = Toplevel()
        self.tela12()
        self.TelaClassificacaoResults()


Application()