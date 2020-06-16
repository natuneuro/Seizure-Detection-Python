from tkinter import *
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
