from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import sqlite3
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile

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
    Ventana_add.title("Patient Registration Form")
    
    
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
    Fullname = StringVar()
    Email = StringVar()

    # conn = sqlite3.connect('Form.db')
    # with conn:
    #     cursor = conn.cursor()

    # def database():
    #     name = Fullname.get()
    #     email = Email.get()
    #     gender = var.get()
    #     branch = c.get()
    #     prog = var1.get()+var2.get()+var3.get()
    #     cursor.execute('CREATE TABLE IF NOT EXISTS Patient ( Fullname TEXT,Email TEXT,Gender TEXT,Branch TEXT,Programming TEXT)')
    #     cursor.execute('INSERT INTO Patient (Fullname,Email,Gender,Branch,Programming) VALUES(?,?,?,?,?)',(name,email,gender,branch,prog))
    #     conn.commit()
    #     showinfo( title = "Patient Reacord", message = "Data inserted sucessfully")

    # def display():
    #     cursor.execute('SELECT * FROM Patient')
    #     data = cursor.fetchall()
    #     print(data)
    #     output = ''
    #     for x in data:
    #         output = output+x[0]+'  '+x[1]+'  '+x[2]+'  '+x[3]+'  '+x[4]+'\n'
    #     print(output)
    #     return output

    # def delete(conn,task):
    #     sql ='DELETE FROM Patient WHERE Fullname =?'
    #     cursor = conn.cursor()
    #     cursor.execute(sql,task)
    #     conn.commit()
    #     showinfo( title = "Patient Reacord", message = "Data deleted sucessfully")
    
    # def update(task):
    #     sql = 'UPDATE Patient SET Email=?, Gender=?, Branch=?, Programming=? WHERE Fullname = ?'
    #     cursor.execute(sql,task)
    #     conn.commit()
    #     showinfo( title = "Patient Reacord", message = "Data updated sucessfully")
        
    # def main():
    #     name = Fullname.get()
    #     email = Email.get()
    #     gender = var.get()
    #     branch = c.get()
    #     prog = var1.get()+var2.get()+var3.get()    
    #     update(name,email,gender,branch,prog)

    # def delete_task():
    #     database = r"Form.db"
    #     conn = sqlite3.connect(database)
    #     name = Fullname.get()
    #     with conn:
    #         delete_task(conn, name)

    Boton_home = Button(Ventana_open, text="Home", command=Ventana_open.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)

    # canvas1 = tk.Canvas(root, width = 1000, height = 500,  relief = 'raised', bg="white")
    # canvas1.pack()

    # label1 = tk.Label(root, text='Registration Form')
    # label1.config(font=("bold", 18),bg="white")
    # canvas1.create_window(250, 30, window=label1)

    # label2 = tk.Label(root, text='Fullname :')
    # label2.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(65, 90, window=label2)

    # entry1 = tk.Entry(root, textvar = Fullname, font = (14), borderwidth=2, width = 30)
    # canvas1.create_window(320, 90, window=entry1)

    # label3 = tk.Label(root, text='E-mail :')
    # label3.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(65, 140, window=label3)

    # entry2 = tk.Entry (root, textvar = Email, font = (14), borderwidth=2, width = 30) 
    # canvas1.create_window(320, 140, window=entry2)

    # label4 = tk.Label(root, text='Gender :')
    # label4.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(65, 190, window=label4)

    # var = StringVar()
    # rd1 = tk.Radiobutton(root ,text="Male" ,padx = 5, variable = var, value = "Male  ")
    # rd1.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(200,190, window = rd1)

    # rd2 = tk.Radiobutton(root ,text="Female" ,padx = 20, variable = var, value = "Female")
    # rd2.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(350,190, window = rd2)

    # label5 = tk.Label(root, text='Age :')
    # label5.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(65, 240, window=label5)

    # list1 = ['0-21','22-45','46-70','71-']
    # c=StringVar()
    # droplist = tk.OptionMenu(root,c,*list1)
    # droplist.config(font=('helvetica',14),bg="white",width = 27)
    # c.set('Select age')
    # canvas1.create_window(320,240, window = droplist)

    # label6 = tk.Label(root, text='Update file :')
    # label6.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(65, 300, window=label6)

    # var = StringVar()
    # rd3 = tk.Button(root ,text="File" ,padx = 5, command = lambda:open_file())
    # rd3.config(font=('helvetica',14),bg="white")
    # canvas1.create_window(200,300, window = rd3)


    # def open_file(): 
    #     file = askopenfile(mode ='r', filetypes =[('EGG', '*.py')]) 
    #     if file is not None: 
    #         content = file.read() 
    #         print(content)
    


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