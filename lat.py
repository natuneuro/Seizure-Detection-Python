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


Imagem1 = "ufmg _logo.png"

# pyinstaller - ver tamanho da iamgem para capa
# colocar as imagens para aparecer nos box : página resultados
# tentar criar uma barra de progresso estilo do tutorial

# Escrever textos:
#   - Pagina about
#   - Mudar pro inglês
#   - Aba sobre o que tem q ser cadastrado
# Melhorar aparencia:
#   - Valor acuracia  
#   - Retangulo azul da borda (tá feio)
#
# Dataset:
#   - salvar valor acuracia
#   - arrumar botão de alteração
#   - criar versoes do botão buscar e colocar as opções no Mostrar Pac.
#   - Conferir se tem q salvar mais algo
#
#  Imagens:
#   - Pegar o código do Art. e add novas imagens no código de apresentação
#   - Deixar o box criado
#


root = tix.Tk()
# FILES


class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatorioCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.codigo_entry.get()
        self.ageRel = self.age_entry
        self.infoRel = self.info_entry.get()
        self.generoRel = self.gender_entry
        #self.nomeArquivo = self.arquivo_name
        #self.accuracy = self.accuracy_entry
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Paciente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50,700, 'Código: ')
        self.c.drawString(50,670, 'Age: ')
        self.c.drawString(50,630, 'Genero: ')
        self.c.drawString(50,600, 'Informações: ')
        self.c.drawString(50,570, 'Nome Arquivo: ')
        self.c.drawString(50,530, 'Dados do treinamento: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150,700, self.codigoRel)
        self.c.drawString(150,670, self.ageRel)


        self.c.drawString(150,630, self.generoRel)
        self.c.drawString(200,600, self.infoRel)
        #self.c.drawString(200,570, self.nomeArquivo)
        #self.c.drawString(200,530, self.accuracy)
        self.c.rect(20, 300, 550, 5, fill=True, stroke=False)

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
        #self.accuracy = ''

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd();
        ### Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nomeArquivo CHAR(200) NOT NULL,
                info CHAR(200),
                age CHAR(50),
                genero CHAR(40)
            );
        
        """)
        # ADD  acurracy CHAR(40)
        self.conn.commit()
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.age = self.Tipvar1.get()
        self.genero =  self.Tipvar.get()
        self.info =  self.info_entry.get()
        self.nomeArquivo = self.nomeArquivo
#        self.accuracy = self.accuracy.get()

    def add_cliente(self):
        self.variaveis()
        if self.nomeArquivo == "":
            msg = "To register a new patient,\n"
            msg += "it is necessary to select the files"
            messagebox.showinfo("Customer registration - Warning !!!", msg)
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
            self.nomeArquivo.insert(END,col5)

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
        self.cursor.execute("""  UPDATE clientes SET age = ?, info = ?, genero = ?, cod = ?
            WHERE  nomeArquivo = ?  """, (self.age, self.info, self.genero, self.codigo, self.nomeArquivo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()

#    def add_accuracy(self):
#        self.variaveis()
#        self.conecta_bd()
#        self.cursor.execute("""  UPDATE clientes SET age = ?, info = ?, genero = ?, nomeArquivo = ?, accuracy = ?
#            WHERE  codigo = ?  """, (self.age, self.info, self.genero, self.nomeArquivo, self.accuracy, self.codigo))
#        self.conn.commit()
#        self.desconecta_bd()
#        self.select_lista()
#        self.limpa_cliente()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        codigo = self.codigo_entry.get()
        print(codigo)
        self.cursor.execute("""  SELECT cod, age, info, genero, nomeArquivo FROM clientes
            WHERE cod LIKE '%s' ORDER BY cod ASC""" % codigo)
        buscaCli = self.cursor.fetchall()
        for i in buscaCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()



#order by title ASC

class Application(Funcs, Relatorios):


    def __init__(self):
        self.root = root
        self.root2 = root
        self.sinal_eeg = []
        self.eventos = []
        self.nomeArquivo = ''
        self.tela()
        self.frames_de_tela()
        self.widgets_frame()
        self.montaTabelas()
        
        root.mainloop()

    def buscar_arquivo(self):
        aux,self.nomeArquivo = LeituraArquivos.ImportarSinalEEG()
        print(self.nomeArquivo)
        self.sinal_eeg.append(aux)
        aux2 = LeituraEventos.importar_evento()
        self.eventos.append(aux2)

    
    def tela(self):
        self.root.title("Epilepsy Detection")
        self.root.config(bg="#DFEBE9")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height= 700)
        self.root.minsize(width=500, height= 400)
        self.logo_cerebro = PhotoImage(file="logos/cerebrito.png")
        label = Label(image=self.logo_cerebro,bg="#DFEBE9")
        label.image = self.logo_cerebro # keep a reference!
        label.pack(side=LEFT, padx=64, pady=55)

        self.logo_ufmg = Image.open("logos/ufmg _logo.png")
        self.resized_ufmg= self.logo_ufmg.resize((100,42), Image.ANTIALIAS)
        self.logo_ufmg_resized=ImageTk.PhotoImage(self.resized_ufmg)
        label = Label(image=self.logo_ufmg_resized,bg="#DFEBE9")
        label.image = self.logo_ufmg_resized # keep a reference!
        label.pack(side=LEFT, anchor=SE, padx=30, pady=30)

        self.logo_labbio = Image.open("logos/labbio_logo.png")
        self.resized_labbio= self.logo_labbio.resize((100,42), Image.ANTIALIAS)
        self.logo_labbio_resized=ImageTk.PhotoImage(self.resized_labbio)
        label = Label(image=self.logo_labbio_resized,bg="#DFEBE9")
        label.image = self.logo_labbio_resized # keep a reference!
        label.pack(side=LEFT, anchor=SE, padx=1, pady=30)



    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#DFEBE9')
        self.frame_1.place(relx=0.70,rely=0.02,relwidth=0.27,relheight=0.80)


    def widgets_frame(self):
        ## Criando botao limpar
        self.Boton_info = Button(self.frame_1, text="Abaut",
                    font=("AvantGarde", 20, "bold"), command = self.JanelaAbout, bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2")

        self.Boton_info.place(relx=0.02, rely=0.2, relwidth=0.98,relheight=0.10)

        ## Criando botao buscar
        self.Boton_add = Button(self.frame_1, text="Add Patient",
                   font=("AvantGarde", 20, "bold"), command = self.JanelaAddPaciente, bg="#14787A", fg="#ffffff",
                   width="15", height="1", cursor="hand2")
        self.Boton_add.place(relx=0.02, rely=0.4, relwidth=0.98,relheight=0.10)

        ## Criando botao novo
        self.Boton_open = Button(self.frame_1, text="Open Patient",
                   font=("AvantGarde", 20, "bold"), command = self.JanelaShowPaciente, bg="#14787A", fg="#ffffff",
                   width="15", height="1", cursor="hand2")
        self.Boton_open.place(relx=0.02, rely=0.6, relwidth=0.98,relheight=0.10)

        ## Criando botao alterar
        self.Boton_close = Button(self.frame_1, text="Close",
                     font=("AvantGarde", 20, "bold"), command= self.root.quit, bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2")
        self.Boton_close.place(relx=0.02, rely=0.8, relwidth=0.98,relheight=0.10)



    ################################# ADD PAT ###########################################
    def frames_de_telaAddPat(self):
        self.frame_1 = Frame(self.root2, bd=4, bg='#DFEBE9',
                                highlightbackground='#759fe6',
                                highlightthickness=3)
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.46)

        self.frame_2 = Frame(self.root2, bd=4, bg='#DFEBE9')
        self.frame_2.place(relx=0.02,rely=0.5,relwidth=0.96,relheight=0.46)

    def widgets_frameAddPat(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#DFEBE9')
        self.aba2.configure(background='#DFEBE9')

        self.abas.add(self.aba1, text = "Aba 1")
        self.abas.add(self.aba2, text = "Aba 2")

        self.abas.place(relx = 0, rely = 0, relwidth=0.98, relheight=0.98)


        self.canvas_bt = Canvas(self.aba1,bd=0, bg='#1e3743', 
                                highlightbackground = 'gray',
                                highlightthickness=5)

        self.canvas_bt.place(relx = 0.19, rely=0.08, relwidth = 0.22, relheight=0.19)
        ## Criando botao limpar
        self.bt_lipar = Button(self.aba1, text="Clean", bd=2, bg='#14787A', 
                                activebackground='#108ecb', activeforeground='white', fg = 'white',
                                font = ('verdana',9,'bold'), command= self.limpa_cliente)
        self.bt_lipar.place(relx=0.2, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao buscar
        self.bt_buscar = Button(self.aba1, text="Search", bd=2, bg='#14787A', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command = self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1,relheight=0.15)

        texto_balao_buscar = "Type in the info field the patient you want to search"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg = texto_balao_buscar)
        
        ## Criando botao novo
        self.bt_novo = Button(self.aba1, text="New", bd=2, bg='#14787A', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao alterar
        self.bt_alterar = Button(self.aba1, text="Change", bd=2, bg='#14787A', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command = self.alterar_cliente )
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao apagar
        self.bt_apagar = Button(self.aba1, text="Delete", bd=2, bg='#14787A', 
                                activebackground='#108ecb', activeforeground='white',fg = 'white',
                                font = ('verdana',9,'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao Treinamento
        self.bt_treinamento = Button(self.aba1, text="Classify", bd=2, bg='#00FFFF', 
                                activebackground='yellow', activeforeground='black',fg = 'black',
                                font = ('verdana',9,'bold'), command=self.JanelaClassificacao)             
        self.bt_treinamento.place(relx=0.5, rely=0.1, relwidth=0.1,relheight=0.15)

        ## Criando botao files
        self.bt_files = Button(self.aba1, text="Files", bd=2,
                                font = ('verdana',9,'bold'), command = lambda:self.buscar_arquivo()) 
        self.bt_files.place(relx=0.5, rely=0.43, relwidth=0.1,relheight=0.15)


        ## Criação da label e entrada de código
        self.lb_codigo = Label(self.aba1, text= "Código",bg="#DFEBE9", fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.15,relwidth=0.08)

        ## Criação da label e entrada da age - 
        self.lb_idade = Label(self.aba1, text= "Age :",bg="#DFEBE9", fg='#107db2')
        self.lb_idade.place(relx=0.05, rely=0.3)

        self.Tipvar1 = StringVar()
        self.TipV1 = ("Child: 0-18","Adult: 19-59","Elderly: 60-")
        self.Tipvar1.set("Child: 0-18")
        self.popupMenu = OptionMenu(self.aba1, self.Tipvar1, *self.TipV1)
        self.popupMenu.place(relx=0.05, rely=0.45,relwidth=0.2)
        self.age_entry = self.Tipvar1.get()



        ## Criação da label e entrada da genero
        self.lb_genero = Label(self.aba1, text= "Gender :",bg="#DFEBE9", fg='#107db2')
        self.lb_genero.place(relx=0.05, rely=0.68)

        self.Tipvar = StringVar()
        self.TipV = ('Male','Woman')
        self.Tipvar.set("Male")
        self.popupMenu = OptionMenu(self.aba1, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx=0.05, rely=0.80,relwidth=0.3)
        self.gender_entry = self.Tipvar.get()


        ## Criação da label e entrada da File
        self.lb_files = Label(self.aba1, text= "Files :",bg="#DFEBE9", fg='#107db2')
        self.lb_files.place(relx=0.5, rely=0.3)
        #self.nomeArquivo_entry =  self.nomeArquivo
        #self.nomeArquivo_entry.place(relx=0.5, rely=0.75,relwidth=0.4)

        ## Criação da label e entrada da Info
        self.lb_info = Label(self.aba1, text= "Info :",bg="#DFEBE9", fg='#107db2')
        self.lb_info.place(relx=0.5, rely=0.6)
        self.info_entry = Entry(self.aba1)
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
        menubar = Menu(self.root2)
        self.root2.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root2.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorios", menu = filemenu2)
        filemenu.add_command(label="Sair", command = Quit)
        filemenu2.add_command(label = "Limpar Cliente", command = self.limpa_cliente)
        filemenu2.add_command(label = "Ficha do cliente", command = self.gerarRelatorioCliente)
       

    def tela2(self):
        self.root2.title("Add Patient")
        self.root2.config(bg="#DFEBE9")
        self.root2.geometry("1024x768")
        self.root2.resizable(True, True)
        self.root2.maxsize(width=900, height= 700)
        self.root2.minsize(width=500, height= 400)
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
        canvasroot3 = Canvas(self.root3, width = 1000, height = 500,  relief = 'raised', bg="#DFEBE9")
        canvasroot3.pack()

        self.Boton_close = Button(self.root3, text="Close",
                     font=("AvantGarde", 20, "bold"), command= self.root.quit, bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2")
        self.Boton_close.place(relx=0.70, rely=0.8, relwidth=0.20,relheight=0.10)


        width = 200
        height = 200
        img = Image.open("logos/cerebrito.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        print(nomeArquivo)

        self.accurancy  = ImageTk.PhotoImage(img)
        canvasroot3.imageList = []
        canvasroot3.pack()
        canvasroot3.create_image(900, 200, anchor="e", image=self.accurancy)
        canvasroot3.imageList.append(self.accurancy)
        label2 = Label(self.root3, text='Sobre o Projeto:')
        label2.config(font=('helvetica',14),bg="#DFEBE9")
        canvasroot3.create_window(100, 100, window=label2)

        canvasroot3.create_text(200,200,fill="darkblue",font=('verdana',9,'bold'),
                        text="Trabalho Desenvolvido pelo laboratório LABBIO")


    def JanelaAbout(self):
        self.root3 = Toplevel()
        self.tela3()
        self.Tela()





    ############################################### SHOW PAT
    def frames_de_telaShowPat(self):
        self.frame_1 = Frame(self.root4, bd=4, bg='#DFEBE9',
                                highlightbackground='#759fe6',
                                highlightthickness=3)
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.25)

        self.frame_2 = Frame(self.root4, bd=4, bg='#DFEBE9')
        self.frame_2.place(relx=0.02,rely=0.3,relwidth=0.96,relheight=0.65)

    def widgets_frameShowPat(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#DFEBE9')
        self.aba2.configure(background="lightgray")

        self.abas.add(self.aba1, text = "Aba 1")
        self.abas.add(self.aba2, text = "Aba 2")

        self.abas.place(relx = 0, rely = 0, relwidth=0.98, relheight=0.98)

        self.codigo_entry = Entry(self.aba1)
        self.Tipvar1 = StringVar()
        self.Tipvar1.set("Child: 0-18")
        self.age_entry = self.Tipvar1.get()

        self.Tipvar = StringVar()
        self.Tipvar.set("Male")
        self.gender_entry = self.Tipvar.get()

        self.canvas_bt = Canvas(self.aba1,bd=0, bg='#1e3743', 
                                highlightbackground = 'gray',
                                highlightthickness=5)

        self.canvas_bt.place(relx = 0.19, rely=0.06, relwidth = 0.22, relheight=0.40)
        ## Criando botao limpar bg="#14787A", fg="#ffffff"
        self.bt_lipar = Button(self.aba1, text="Limpar", bd=2, bg="#14787A",
                                activebackground='#108ecb', activeforeground='white', fg="#ffffff",
                                font = ('verdana',9,'bold'), command= self.limpa_cliente)
        self.bt_lipar.place(relx=0.2, rely=0.1, relwidth=0.1,relheight=0.30)

        ## Criando botao buscar
        self.bt_buscar = Button(self.aba1, text="Buscar", bd=2, bg="#14787A", 
                                activebackground='#108ecb', activeforeground='white',fg="#ffffff",
                                font = ('verdana',9,'bold'), command = self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1,relheight=0.30)

        texto_balao_buscar = "Digite no campo info o paciente que deseja pesquisar"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg = texto_balao_buscar)
        
        ## Criação da label e entrada de código
        self.lb_codigo = Label(self.aba1, text= "Código",bg="#DFEBE9", fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.10)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.30,relwidth=0.08)


    def lista_frame4(self):
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

    def MenusShowPaciente(self):
        menubar = Menu(self.root4)
        self.root4.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu = Menu(menubar)

        def Quit(): self.root4.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorios", menu = filemenu2)
        filemenu.add_command(label="Sair", command = Quit)
        filemenu2.add_command(label = "Limpar Cliente", command = self.limpa_cliente)
        filemenu2.add_command(label = "Ficha do cliente", command = self.gerarRelatorioCliente)
       

    def tela4(self):
        self.root4.title("Show")
        self.root4.config(bg="#DFEBE9")
        self.root4.geometry("1024x768")
        self.root4.resizable(True, True)
        self.root4.maxsize(width=900, height= 700)
        self.root4.minsize(width=500, height= 400)
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

    ############################################ TREINAMENTO
    
    def frames_de_telaClassification(self):
        self.frame_1 = Frame(self.root5, bd=4, bg='#DFEBE9')
        self.frame_1.place(relx=0.70,rely=0.02,relwidth=0.27,relheight=0.80)

    def widgets_frameClassification(self):
        ## Criando botao limpar
        self.Boton_info = Button(self.frame_1, text="Next Image",
                    font=("AvantGarde", 20, "bold"), command = self.JanelaAbout, bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2")

        self.Boton_info.place(relx=0.02, rely=0.2, relwidth=0.98,relheight=0.10)

        ## Criando botao alterar
        self.Boton_close = Button(self.frame_1, text="Close",
                     font=("AvantGarde", 20, "bold"), command= self.root.quit, bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2")
        self.Boton_close.place(relx=0.02, rely=0.8, relwidth=0.98,relheight=0.10)


    def MenusClassification(self):
        menubar = Menu(self.root5)
        self.root5.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root5.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu)
        menubar.add_cascade(label = "Relatorio Paciente", menu = filemenu2)
        filemenu.add_command(label="Sair", command = Quit)
        filemenu2.add_command(label = "Ficha do client", command = self.gerarRelatorioCliente)
       

    def tela5(self):
        self.root5.title("Classification")
        self.root5.config(bg="#DFEBE9")
        self.root5.geometry("1024x768")
        self.root5.resizable(True, True)
        self.root5.maxsize(width=900, height= 700)
        self.root5.minsize(width=500, height= 400)
        self.root5.transient(self.root2)
        self.root5.focus_force()
        self.root5.grab_set()        

    def Treinamento(self):
        canvas3 = Canvas(self.root5, width = 1000, height = 500,  relief = 'raised', bg="#DFEBE9")
        canvas3.pack()

        #self.abas = ttk.Notebook(canvas3)
        #self.aba1 = Frame(self.abas)
        #self.aba2 = Frame(self.abas)

        #self.aba1.configure(background='#DFEBE9')
        #self.aba2.configure(background="lightgray")

        #self.abas.add(self.aba1, text = "Aba 1")
        #self.abas.add(self.aba2, text = "Aba 2")

        #self.abas.place(relx = 0, rely = 0, relwidth=0.1, relheight=0.1)

       # Recebe código do arthur e executa
        sinal_eeg = self.sinal_eeg[0]
        eventos = self.eventos[0]

        fs = sinal_eeg.frequencia_de_amostragem

        sinal_delta_theta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([1, 7])
        sinal_alpha_beta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([8, 30])
        sinal_gama = sinal_eeg.decomporSinalEmFaixaDeFrequencia([31, 100])

        delta_theta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_delta_theta, fs)
        alpha_beta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_alpha_beta, fs)
        gama_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_gama, fs)

        AssociaTrechoEvento.associa_trecho_evento(delta_theta_dividido, eventos)
        AssociaTrechoEvento.associa_trecho_evento(alpha_beta_dividido, eventos)
        AssociaTrechoEvento.associa_trecho_evento(gama_dividido, eventos)

        dados = CriaImagen.cria_imagens_saidas(gama_dividido, delta_theta_dividido, alpha_beta_dividido)

        classification_info = CNN.CNN_fit(dados[0], dados[1])
        cm_plot_labels = ["Normal", "Epilepsy"]
        ConfusionMatrix.plot_confusion_matrix(classification_info[2], cm_plot_labels, title="Confusion Matrix")


        ## Criando botao alterar
        self.Boton_close = Button(self.root5, text="Close",
                     font=("AvantGarde", 20, "bold"), command= self.root.quit, bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2")
        self.Boton_close.place(relx=0.70, rely=0.8, relwidth=0.20,relheight=0.10)


        Resultado = "Resultado.png"
        width = 600
        height = 400
        img = Image.open(Resultado)
        img = img.resize((width,height), Image.ANTIALIAS)
        self.accurancy  = ImageTk.PhotoImage(img)
        canvas3.imageList = []
        canvas3.pack()
        canvas3.create_image(200, 230, anchor="w", image=self.accurancy)
        canvas3.imageList.append(self.accurancy)

        label2 = Label(self.root5, text='Accurancy:')
        label2.config(font=('helvetica',14),bg="#DFEBE9")
        canvas3.create_window(100, 100, window=label2)
        label4 = Label(self.root5, text=classification_info[0])
        label4.config(font=('helvetica',14),bg="#DFEBE9")
        canvas3.create_window(100, 130, window=label4)




    def JanelaClassificacao(self):
        self.root5 = Toplevel()
        self.tela5()
        self.frames_de_telaClassification()
        self.widgets_frameClassification()
        self.MenusClassification()
        self.Treinamento()





Application()