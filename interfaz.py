from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

# ------------  HOME SCREEN   ---------------------------------------------
raiz = Tk()
raiz.title("Epilepsy Detection")
raiz.resizable(0, 0)
# raiz.iconbitmap("logos/icono.ico")
raiz.geometry("1024x768")
raiz.config(bg="#DFEBE9")

# ------------------ IMAGES AND LOGOS INTO HOME SCREEN -------------------


logo_cerebro = PhotoImage(file="logos/cerebrito.png")
Label(raiz, image=logo_cerebro, bg="#DFEBE9").place(x=64, y=55)

logo_ufmg= Image.open("logos/ufmg _logo.png")
resized_ufmg= logo_ufmg.resize((100,42), Image.ANTIALIAS)
logo_ufmg_resized=ImageTk.PhotoImage(resized_ufmg)
Label(raiz, image=logo_ufmg_resized,bg="#DFEBE9").place(x=670,y=691)

logo_labbio = Image.open("logos/labbio_logo.png")
resized_labbio = logo_labbio.resize((100, 52), Image.ANTIALIAS)
logo_labbio_resized = ImageTk.PhotoImage(resized_labbio)
Label(raiz, image=logo_labbio_resized, bg="#DFEBE9").place(x=840, y=686)

# ------------------ Images and logos into Information Screen ------------

logo_cerebro_solo = Image.open("logos/cerebro_solo.png")
resized_cerebro = logo_cerebro_solo.resize((400, 400), Image.ANTIALIAS)
logo_cerebro_resized = ImageTk.PhotoImage(resized_cerebro)

resized_ufmg2= logo_ufmg.resize((150,63), Image.ANTIALIAS)
logo_ufmg_resized2=ImageTk.PhotoImage(resized_ufmg2)


resized_labbio2 = logo_labbio.resize((150, 78), Image.ANTIALIAS)
logo_labbio_resized2 = ImageTk.PhotoImage(resized_labbio2)



# -----------------  Open Information Screen ------------------------------
def info():
    #raiz.withdraw()
    Ventana_info = Toplevel()
    Ventana_info.geometry("1024x768")
    Ventana_info.config(bg="#DFEBE9")
    Ventana_info.title("About")
    Label(Ventana_info, image=logo_cerebro_resized, bg="#DFEBE9").place(x=550, y=55)
    Label(Ventana_info, image=logo_ufmg_resized2, bg="#DFEBE9").place(x=709, y=465)
    Label(Ventana_info, image=logo_labbio_resized2, bg="#DFEBE9").place(x=709, y=574)
    titulo_info = Label(Ventana_info, text="About Project",
                        font=("AvantGarde", 40, "bold"), bg="#DFEBE9",
                        fg="#14787A").place(x=10, y=20)
    Boton_home = Button(Ventana_info, text="Home", command=Ventana_info.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=660, y=700)


# -----------------  Open Add Patient Screen ------------------------------
def add_patient():
    #raiz.withdraw()
    Ventana_add = Toplevel()
    Ventana_add.geometry("1024x768")
    Ventana_add.config(bg="#DFEBE9")
    Ventana_add.title("Add Patient")
    #create a Form label 
    heading = Label(Ventana_add, text="Form",font=("AvantGarde", 40, "bold")) 
    a = Label(Ventana_add ,text = "File Name",font=("AvantGarde", 20, "bold")).grid(row = 2,column = 6)
    b = Label(Ventana_add ,text = "Patient Age",font=("AvantGarde", 20, "bold")).grid(row = 6,column = 6)
    c = Label(Ventana_add ,text = "F or M",font=("AvantGarde", 20, "bold")).grid(row = 10,column = 6)
    d = Label(Ventana_add ,text = "Another information",font=("AvantGarde", 20, "bold")).grid(row = 16,column = 6)
    heading.grid(row=1, column=8) 
    a1 = Entry(Ventana_add).grid(row = 2,column = 14)
    b1 = Entry(Ventana_add).grid(row = 6,column = 14)
    c1 = Entry(Ventana_add).grid(row = 10,column = 14)
    d1 = Entry(Ventana_add).grid(row = 16,column = 14)
    btn2 = ttk.Button(Ventana_add ,text="Submit").grid(row=40,column=8)
    #btn2 = ttk.Button(Ventana_add, text ='Open', command = lambda:open_file(),
    #                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
    #                width="15", height="1", cursor="hand2").place(x=700, y=359)
   # btn.pack(side = TOP, pady = 10) 
    def clicked():
        res = "Welcome to " + txt.get()
        lbl.configure(text= res)
    # This function will be used to open 
    # file in read mode and only Python files 
    # will be opened 
    def open_file(): 
        file = askopenfile(mode ='r', filetypes =[('EGG', '*.py')]) 
        if file is not None: 
            content = file.read() 
            print(content) 
    
    btn = ttk.Button(Ventana_add ,text="Add file", command = lambda:open_file())
    Boton_home = Button(Ventana_add, text="Home", command=Ventana_add.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)


# -----------------  Open Open Patient Screen ------------------------------
def open_patient():
    #raiz.withdraw()
    Ventana_open = Toplevel()
    Ventana_open.geometry("1024x768")
    Ventana_open.config(bg="#DFEBE9")
    Ventana_open.title("Open Patient")
    Boton_home = Button(Ventana_open, text="Home", command=Ventana_open.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)


# ---------------  Buttons into home screen ----------------------------------


Boton_info = Button(raiz, text="Abaut", command=info,
                    font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2").place(x=700, y=101)

Boton_add = Button(raiz, text="Add Pacient", command=add_patient,
                   font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                   width="15", height="1", cursor="hand2").place(x=700, y=230)

Boton_open = Button(raiz, text="Open Patient", command=open_patient,
                    font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2").place(x=700, y=359)

Boton_close = Button(raiz, text="Close", command=raiz.quit,
                     font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2").place(x=700, y=488)






raiz.mainloop()
