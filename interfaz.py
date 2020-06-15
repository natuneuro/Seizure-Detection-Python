from tkinter import *
from PIL import Image, ImageTk



# ------------  HOME SCREEN   ---------------------------------------------
class MainWindow():
    
    def __init__(self,master,title,size):
        self.master = master
        self.title = title
        self.resizable = (0,0)
        self.size = size
        self.master.title(self.title)
        self.master.geometry(self.size)
        self.master.config(bg="#DFEBE9")
        self.canvas = 0
        #self.master.iconbitmap("logos/icono.ico")
        self.img = ImageTk.PhotoImage(Image.open("logos/cerebrito.png"))
        Label(self.master, image=self.img, bg="#DFEBE9").place(x=64, y=55)
   

        self.logo_ufmg= Image.open("logos/ufmg _logo.png")
        self.resized_ufmg= self.logo_ufmg.resize((100,42), Image.ANTIALIAS)
        self.logo_ufmg_resized=ImageTk.PhotoImage(self.resized_ufmg)
        Label(self.master, image=self.logo_ufmg_resized,bg="#DFEBE9").place(x=670,y=691)

        self.logo_labbio = Image.open("logos/labbio_logo.png")
        self.resized_labbio = self.logo_labbio.resize((100, 52), Image.ANTIALIAS)
        self.logo_labbio_resized = ImageTk.PhotoImage(self.resized_labbio)
        Label(self.master, image=self.logo_labbio_resized, bg="#DFEBE9").place(x=840, y=686)


        self.quitMainWindow = Button(self.master,
                                text="Close",
                                width=15, height=1,
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                cursor="hand2", 
                                command=self.on_cancel).place(x=700, y=488)


        self.aboutWindow = Button(self.master, 
                                text="Abaut",
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                width="15", height="1", cursor="hand2",
                                command= self.aboutButtonClicked).place(x=700, y=101)

        self.NewPacientWindow = Button(self.master,
                                text="Add Pacient",
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                width="15", height="1", cursor="hand2",
                                command = self.newPacientButtonClicked).place(x=700, y=230)

        self.OpenPacientWindow =Button(self.master, 
                                text="Open Patient", 
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff", 
                                width="15", height="1", cursor="hand2",
                                command = self.openPacientButtonClicked).place(x=700, y=359)

        # self. Boton_close = Button(self.master, text="Close", command=raiz.quit,
        #                         font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
        #                         width="15", height="1", cursor="hand2").place(x=700, y=488)


    def aboutButtonClicked(self):   
        pageAbout = AboutWindow()

    def newPacientButtonClicked(self):   
        pageNew =  NewPacientWindow()

    
    def openPacientButtonClicked(self):   
        pagePacient =  OpenPacientWindow()


                    

    def on_cancel(self):
        self.master.destroy()


# ------------------ Information Screen ------------
class AboutWindow(Toplevel):
    def __init__(self):
        super().__init__(name='about page')
        self.parent = "second window",
        self.title("About")
        self.config(bg="#DFEBE9")
        self.size = "1024x768"
        self.geometry("1024x768")

        self.logo_cerebro_solo = Image.open("logos/cerebro_solo.png")
        self.resized_cerebro = self.logo_cerebro_solo.resize((400, 400), Image.ANTIALIAS)
        self.logo_cerebro_resized = ImageTk.PhotoImage(self.resized_cerebro)
        Label(self, image=self.logo_cerebro_resized, bg="#DFEBE9").place(x=550, y=55)

        self.logo_ufmg= Image.open("logos/ufmg _logo.png")
        self.resized_ufmg= self.logo_ufmg.resize((150,63), Image.ANTIALIAS)
        self.logo_ufmg_resized=ImageTk.PhotoImage(self.resized_ufmg)
        Label(self, image=self.logo_ufmg_resized,bg="#DFEBE9").place(x=709, y=465)

        self.logo_labbio = Image.open("logos/labbio_logo.png")
        self.resized_labbio = self.logo_labbio.resize((150, 78), Image.ANTIALIAS)
        self.logo_labbio_resized = ImageTk.PhotoImage(self.resized_labbio)
        Label(self, image=self.logo_labbio_resized, bg="#DFEBE9").place(x=709, y=574)

        
        titulo_info = Label(self, text="About Project",
                            font=("AvantGarde", 40, "bold"), bg="#DFEBE9",
                            fg="#14787A").place(x=10, y=20)

        self.gobackButton = Button(self,
                                text="Home",
                                width=15, height=1,
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                cursor="hand2", 
                                command=self.on_cancel).place(x=700, y=700)
        

    def on_cancel(self):
        self.destroy()




# -----------------  Add Patient Screen ------------------------------
class NewPacientWindow(Toplevel):
    def __init__(self):
        super().__init__(name='new pacient window')
        self.parent = "second window",
        self.title("About")
        self.config(bg="#DFEBE9")
        self.size = "1024x768"
        self.geometry("1024x768")

        #Label(self, image=logo_cerebro_resized, bg="#DFEBE9").place(x=550, y=55)
        #Label(self, image=logo_ufmg_resized2, bg="#DFEBE9").place(x=709, y=465)
        #Label(self, image=logo_labbio_resized2, bg="#DFEBE9").place(x=709, y=574)
        titulo_info = Label(self, text="New Pacient",
                            font=("AvantGarde", 40, "bold"), bg="#DFEBE9",
                            fg="#14787A").place(x=10, y=20)

        self.gobackButton = Button(self,
                                text="Home",
                                width=15, height=1,
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                cursor="hand2", 
                                command=self.on_cancel).place(x=700, y=600)
        

    def on_cancel(self):
        self.destroy()



class OpenPacientWindow(Toplevel):
    def __init__(self):
        super().__init__(name='open pacients')
        self.parent = "second window",
        self.title("About")
        self.config(bg="#DFEBE9")
        self.size = "1024x768"
        self.geometry("1024x768")

        #Label(self, image=logo_cerebro_resized, bg="#DFEBE9").place(x=550, y=55)
        #Label(self, image=logo_ufmg_resized2, bg="#DFEBE9").place(x=709, y=465)
        #Label(self, image=logo_labbio_resized2, bg="#DFEBE9").place(x=709, y=574)
        titulo_info = Label(self, text="Open list pacients",
                            font=("AvantGarde", 40, "bold"), bg="#DFEBE9",
                            fg="#14787A").place(x=10, y=20)

        self.gobackButton = Button(self,
                                text="Home",
                                width=15, height=1,
                                font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                                cursor="hand2", 
                                command=self.on_cancel).place(x=700, y=600)
        

    def on_cancel(self):
        self.destroy()



if __name__ == "__main__":
    mainWindow = Tk()
    mainFenster = MainWindow(mainWindow, "Epilepsy Detection", "1024x768")
    mainWindow.mainloop()




# ------------------ Images and logos into Information Screen ------------

# logo_cerebro_solo = Image.open("logos/cerebro_solo.png")
# resized_cerebro = logo_cerebro_solo.resize((400, 400), Image.ANTIALIAS)
# logo_cerebro_resized = ImageTk.PhotoImage(resized_cerebro)

# resized_ufmg2= logo_ufmg.resize((150,63), Image.ANTIALIAS)
# logo_ufmg_resized2=ImageTk.PhotoImage(resized_ufmg2)


# resized_labbio2 = logo_labbio.resize((150, 78), Image.ANTIALIAS)
# logo_labbio_resized2 = ImageTk.PhotoImage(resized_labbio2)

# -----------------  Open Information Screen ------------------------------


# -----------------  Open Information Screen ------------------------------
def info():
    raiz.withdraw()
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
    Boton_home = Button(Ventana_info, text="Home", command=Ventana_info.quit,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=660, y=700)


# -----------------  Open Add Patient Screen ------------------------------
def add_patient():
    raiz.withdraw()
    Ventana_add = Toplevel()
    Ventana_add.geometry("1024x768")
    Ventana_add.config(bg="#DFEBE9")
    Ventana_add.title("Add Patient")
    Boton_home = Button(Ventana_add, text="Home", command=open_patient,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)


# -----------------  Open Open Patient Screen ------------------------------
def open_patient():
    raiz.withdraw()
    Ventana_open = Toplevel()
    Ventana_open.geometry("1024x768")
    Ventana_open.config(bg="#DFEBE9")
    Ventana_open.title("Open Patient")
    Boton_home = Button(Ventana_open, text="Home", command=raiz,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)






