from tkinter import *
from PIL import Image

#------------  PANTALLA INICIAL   ---------------------------------------------

raiz=Tk()
raiz.title("Epilepsy Detection")
raiz.resizable(0,0)
#raiz.iconbitmap("/home/naty/Pictures/cerebro_azul_icono.ico")
raiz.geometry("1024x768")
raiz.config(bg="#DFEBE9")

#def home(raiz)


#-----------------  Abrir Pantalla de informacion ------------------------------
def info():
    raiz.withdraw()
    Ventana_info =Toplevel()
    Ventana_info.geometry("1024x768")
    Ventana_info.config(bg="#DFEBE9")
    Ventana_info.title("About")
    logo_info = PhotoImage(file="/home/naty/Pictures/cerebro_azulpeque.png")
    Label(Ventana_info, image=logo_info, bg="#DFEBE9").place(x=64, y=55)
    titulo_info = Label(Ventana_info, text="About Project",
                        font=("AvantGarde",40,"bold"),bg="#DFEBE9").place(x=10,y=20)
    Boton_regresar= Button(Ventana_info, text="Home",
      font=("AvantGarde",20,"bold"),bg="#14787A" , fg="#ffffff",
                width="15", height="1",cursor="hand2").place(x=700,y=700)

def add_patient():
    raiz.withdraw()
    Ventana_add = Toplevel()
    Ventana_add.geometry("1024x768")
    Ventana_add.config(bg="#DFEBE9")
    Ventana_add.title("Add Patient")
    Boton_regresar = Button(Ventana_add, text="Home",
                            font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                            width="15", height="1", cursor="hand2").place(x=700, y=700)

#---------------  Botones  ----------------------------------------------------


Boton_info=Button(raiz, text="Abaut", command=info,
      font=("AvantGarde",20,"bold"),bg="#14787A" , fg="#ffffff",
                width="15", height="1",cursor="hand2").place(x=700,y=101)

Boton_add= Button(raiz, text="Add Pacient", command=add_patient,
      font=("AvantGarde",20,"bold"),bg="#14787A" , fg="#ffffff",
                width="15", height="1",cursor="hand2").place(x=700,y=230)

Boton_open=Button(raiz, text="Open Patient",
      font=("AvantGarde",20,"bold"),bg="#14787A" , fg="#ffffff",
                width="15", height="1",cursor="hand2").place(x=700,y=359)

Boton_close=Button(raiz, text="Close",
      font=("AvantGarde",20,"bold"),bg="#14787A", fg="#ffffff",
                width="15", height="1",cursor="hand2").place(x=700,y=488)


#--------------------  IMAGENES Y LOGOTIPOS  -----------------------------------
logo=PhotoImage(file="/home/naty/Pictures/cerebrito.png")
ufmg=PhotoImage(file="/home/naty/Pictures/ufmg_logo.png")
labbio=PhotoImage(file="/home/naty/Pictures/labbio_logo.png")
Label(raiz, image=logo,bg="#DFEBE9").place(x=64,y=55)
Label(raiz, image=ufmg,bg="#DFEBE9").place(x=670,y=691)
Label(raiz, image=labbio,bg="#DFEBE9").place(x=840,y=686)

raiz.mainloop()




