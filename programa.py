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
from Modulos import LeituraArquivos,ConfusionMatrix, ProcessamentoDoSinal, LeituraEventos, AssociaTrechoEvento, CriaImagen, CNN

# pyinstaller - ver tamanho da iamgem para capa
# conferir pq q não abriu agr ,_,
#

root = tix.Tk()
# FILES
sinal_eeg = []
eventos = []




class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatorioCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.codigo_entry.get()
        self.ageRel = self.age_entry.get()
        self.infoRel = self.info_entry.get()
        self.generoRel = self.genero_entry.get()
        

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Paciente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50,700, 'Código: ')
        self.c.drawString(50,670, 'Age: ')
        self.c.drawString(50,630, 'Genero: ')
        self.c.drawString(50,600, 'Informações: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150,700, self.codigoRel)
        self.c.drawString(150,670, self.ageRel)
        self.c.drawString(150,630, self.generoRel)
        self.c.drawString(200,600, self.infoRel)

        self.c.rect(20, 550, 550, 5, fill=True, stroke=False)


        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.Tipvar1.set('Child: 0-18')
        self.info_entry.delete(0, END)
        self.Tipvar.set('Male')
        self.nomeArquivo = ''

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd();
        print("Conectando ao Banco de Dados")
        ### Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nomeArquivo CHAR(200) NOT NULL,
                info CHAR(200),
                age INTEGER(3),
                genero CHAR(40)
            );
        
        """)
        self.conn.commit();
        print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.age = self.Tipvar1.get()
        self.genero =  self.Tipvar.get()
        self.info =  self.info_entry.get()
        self.nomeArquivo = self.nomeArquivo_entry.get()

    def add_cliente(self):
        self.variaveis()
        if self.nomeArquivo_entry.get()== "":
            msg = "Para cadastrar um novo paciente eh necessario\n"
            msg += "que seja selecionado os arquivos"
            messagebox.showinfo("Cadastro de cliente - Aviso!!!", msg)
        else :

            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (age,genero, info, nomeArquivo)
                VALUES(?, ?, ?, ?) """,(self.age, self.genero, self.info, self.nomeArquivo))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_cliente()
    
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, age, genero , info, nomeArquivo FROM clientes 
            ORDER BY cod;  """)

        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
        
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            col2 = self.age_entry
            col3 = self.gender_entry
            self.info_entry.insert(END, col4)
            self.nomeArquivo_entry.insert(END,col5)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()

    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""  UPDATE clientes SET age = ?, info = ?, genero = ? cod = ?
            WHERE  nomeArquivo = ?  """, (self.age, self.info, self.genero, self.codigo, self.nomeArquivo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        nomeArquivo = self.nomeArquivo_entry
        self.cursor.execute("""  SELECT cod, age, info, genero, nomeArquivo FROM clientes
            WHERE age LIKE '%s' ORDER BY nomeArquivo ASC""" % nomeArquivo)
        buscaCli = self.cursor.fetchall()
        for i in buscaCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()

    def buscar_arquivo(self,sinal_eeg, eventos):
        aux,nomeArquivo = LeituraArquivos.ImportarSinalEEG()
        print(nomeArquivo)
        sinal_eeg.append(aux)
        aux2 = LeituraEventos.importar_evento()
        eventos.append(aux2)
        print("Feito")

#order by title ASC

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_de_tela()
        self.widgets_frame()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(bg='#DFEBE9')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height= 700)
        self.root.minsize(width=500, height= 400)

    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                                highlightbackground='#759fe6',
                                highlightthickness=3)
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                                highlightbackground='#759fe6',
                                highlightthickness=3)
        self.frame_2.place(relx=0.02,rely=0.5,relwidth=0.96,relheight=0.46)

    def widgets_frame(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background="#dfe3ee")
        self.aba2.configure(background="lightgray")

        self.abas.add(self.aba1, text = "Aba 1")
        self.abas.add(self.aba2, text = "Aba 2")

        self.abas.place(relx = 0, rely = 0, relwidth=0.98, relheight=0.98)


        self.canvas_bt = Canvas(self.aba1,bd=0, bg='#1e3743', 
                                highlightbackground = 'gray',
                                highlightthickness=5)

        self.canvas_bt.place(relx = 0.19, rely=0.08, relwidth = 0.22, relheight=0.19)
        ## Criando botao limpar
        self.bt_lipar = Button(self.aba1, text="Limpar", bd=2, bg='#107db2', 
                                activebackground='#108ecb', activeforeground='white', fg = 'white',
                                font = ('verdana',9,'bold'), command= self.limpa_cliente)
        self.bt_lipar.place(relx=0.2, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao buscar
        self.bt_buscar = Button(self.aba1, text="Buscar", bd=2, bg='#107db2', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command = self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1,relheight=0.15)

        texto_balao_buscar = "Digite no campo info o paciente que deseja pesquisar"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg = texto_balao_buscar)
        
        ## Criando botao novo
        self.bt_novo = Button(self.aba1, text="Novo", bd=2, bg='#107db2', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao alterar
        self.bt_alterar = Button(self.aba1, text="Alterar", bd=2, bg='#107db2', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command = self.alterar_cliente )
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao apagar
        self.bt_apagar = Button(self.aba1, text="Apagar", bd=2, bg='#107db2', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao files
        self.bt_files = Button(self.aba1, text="Files", bd=2,
                                font = ('verdana',9,'bold'), command = lambda:self.buscar_arquivo(sinal_eeg, eventos))
        


        self.bt_files.place(relx=0.5, rely=0.43, relwidth=0.1,relheight=0.15)


        ## Criação da label e entrada de código
        self.lb_codigo = Label(self.aba1, text= "Código",bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.15,relwidth=0.08)

        ## Criação da label e entrada da age - 
        self.lb_idade = Label(self.aba1, text= "Age :",bg='#dfe3ee', fg='#107db2')
        self.lb_idade.place(relx=0.05, rely=0.3)

        self.Tipvar1 = StringVar()
        self.TipV1 = ("Child: 0-18","Adult: 19-59","Elderly: 60-")
        self.Tipvar1.set("Child: 0-18")
        self.popupMenu = OptionMenu(self.aba1, self.Tipvar1, *self.TipV1)
        self.popupMenu.place(relx=0.05, rely=0.45,relwidth=0.2)
        self.age_entry = self.Tipvar1.get()
        print("############")
        print(self.Tipvar1)
        print("############")

        ## Criação da label e entrada da genero
        self.lb_genero = Label(self.aba1, text= "Gender :",bg='#dfe3ee', fg='#107db2')
        self.lb_genero.place(relx=0.05, rely=0.68)

        self.Tipvar = StringVar()
        self.TipV = ('Male','Woman')
        self.Tipvar.set("Male")
        self.popupMenu = OptionMenu(self.aba1, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.05, rely=0.80,relwidth=0.3)
        self.gender_entry = self.Tipvar.get()
        print(self.gender_entry)

        ## Criação da label e entrada da File
        self.lb_files = Label(self.aba1, text= "Files :",bg='#dfe3ee', fg='#107db2')
        self.lb_files.place(relx=0.5, rely=0.3)


        ## Criação da label e entrada da Info
        self.lb_info = Label(self.aba1, text= "Info :",bg='#dfe3ee', fg='#107db2')
        self.lb_info.place(relx=0.5, rely=0.6)

        self.info_entry = Entry(self.aba1)
        self.nomeArquivo_entry = self.info_entry
        print(self.info_entry)
        print(self.nomeArquivo_entry)
        self.nomeArquivo_entry.place(relx=0.5, rely=0.75,relwidth=0.4)
        self.info_entry.place(relx=0.5, rely=0.75,relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5"))
        self.listaCli.heading("#0", text ="")
        self.listaCli.heading("#1", text ="Cod")
        self.listaCli.heading("#2", text ="Age")
        self.listaCli.heading("#3", text ="Gender")
        self.listaCli.heading("#4", text ="Info")
        self.listaCli.heading("#5", text ="nomeArquivo")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=100)
        self.listaCli.column("#3", width=70)
        self.listaCli.column("#4", width=170)
        self.listaCli.column("#5", width=250)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95,relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient= 'vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04,relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorios", menu = filemenu2)

        filemenu.add_command(label="Sair", command = Quit)
        filemenu2.add_command(label = "Limpar Cliente", command = self.limpa_cliente)

        filemenu2.add_command(label = "Ficha do cliente", command = self.gerarRelatorioCliente)

    def Janela2(self):
        self.root2 = Toplevel()
        self.root2.title("Janela 2")
        self.root2.configure(bg='#DFEBE9')
        self.root2.geometry("400x200")
        self.root2.resizable(False, False)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()

Application()