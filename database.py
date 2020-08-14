
import tkinter as tk
from tkinter.messagebox import showinfo
import sqlite3

LARGE_FONT= ("Verdana", 12)
#Database
def addentry(ID, EEG_FILE_NAME, AGE) :

       db = sqlite3.connect("LibManagment.db")
       cur=db.cursor()
       cur.execute('INSERT INTO Add_lib2 VALUES (?, ?, ?);', (ID, EEG_FILE_NAME, AGE))
       print("Entry Added To Database")
       db.commit()
       showinfo( title = "Librarian Add", message = "Data inserted To table")


class Myproj(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Adminlogin, Liblogin, Adsection, Addlib, Viewlib):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Library Managment system", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Admin Login",
                            command=lambda: controller.show_frame(Adminlogin))
        button.pack()

        button2 = tk.Button(self, text="Lib Login",
                            command=lambda: controller.show_frame(Liblogin))
        button2.pack()


class Adminlogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        name_label = tk.Label(self, text="User ID:", font=LARGE_FONT)
        name_label.pack(pady=10,padx=10)
        name_lable = tk.Entry(self)
        name_lable.pack(pady=10,padx=10)
        pwd_label = tk.Label(self, text="Password", font=LARGE_FONT)
        pwd_label.pack(pady=10,padx=10)
        pwd_lable = tk.Entry(self, show="*")
        pwd_lable.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame(Adsection))
        button2.pack()


class Liblogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Lname_label = tk.Label(self, text="User ID:", font=LARGE_FONT)
        Lname_label.pack(pady=10,padx=10)
        Lname_lable = tk.Entry(self)
        Lname_lable.pack(pady=10,padx=10)
        Lpwd_label = tk.Label(self, text="Password", font=LARGE_FONT)
        Lpwd_label.pack(pady=10,padx=10)
        Lpwd_lable = tk.Entry(self, show="*")
        Lpwd_lable.pack(pady=10,padx=10)


        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame(Adminlogin))
        button2.pack()
        
class Adsection(tk.Frame):

# if name_lable.get() == Admin and pwd_lable.get() == Admin:

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            button1 = tk.Button(self, text="Add Librarian",
                                command=lambda: controller.show_frame(Addlib))
            button1.pack()

            button2 = tk.Button(self, text="View Librarian",
                                command=lambda: controller.show_frame(Viewlib))
            button2.pack()

            button3 = tk.Button(self, text="Delete Librarian",
                                command=lambda: controller.show_frame(StartPage))
            button3.pack()

            button4 = tk.Button(self, text="Logout",
                                command=lambda: controller.show_frame(StartPage))
            button4.pack()



class Addlib(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Libname_label = tk.Label(self, text="Name:", font=LARGE_FONT)
        Libname_label.pack(pady=10,padx=10)
        namevar = tk.StringVar()
        Libname_lable = tk.Entry(self, textvariable=namevar)
        Libname_lable.pack(pady=10,padx=10)
        Libpass_label = tk.Label(self, text="Password:", font=LARGE_FONT)
        Libpass_label.pack(pady=10,padx=10)
        pwdvar = tk.StringVar()
        Libpass_label = tk.Entry(self, show ='*', textvariable=pwdvar)
        Libpass_label.pack(pady=10,padx=10)
        Libemail_label = tk.Label(self, text="Email:", font=LARGE_FONT)
        Libemail_label.pack(pady=10,padx=10)
        emailvar = tk.StringVar()
        Libemail_label = tk.Entry(self, textvariable=emailvar)
        Libemail_label.pack(pady=10,padx=10)
        LibAddres_label = tk.Label(self, text="Address:", font=LARGE_FONT)
        LibAddres_label.pack(pady=10,padx=10)
        addressvar = tk.StringVar()
        LibAddres_label = tk.Entry(self, textvariable=addressvar)
        LibAddres_label.pack(pady=10,padx=10)
        Libcity_label = tk.Label(self, text="City:", font=LARGE_FONT)
        Libcity_label.pack(pady=10,padx=10)
        cityvar = tk.StringVar()
        Libcity_label = tk.Entry(self, textvariable=cityvar)
        Libcity_label.pack(pady=10,padx=10)
        Libcontect_label = tk.Label(self, text="Contect:", font=LARGE_FONT)
        Libcontect_label.pack(pady=10,padx=10)
        contectvar =tk.StringVar()
        Libcontect_label = tk.Entry(self, textvariable=contectvar)
        Libcontect_label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Add Libraian", command=lambda: addentry(namevar.get(), pwdvar.get(), emailvar.get(), addressvar.get(), cityvar.get(), contectvar.get()))
        button1.pack()
        button4 = tk.Button(self, text='BACK',
                                command=lambda: controller.show_frame(Adsection))
                        
        button4.pack()


class Viewlib(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        db = sqlite3.connect("LibManagment.db")
        cur=db.cursor()
        cur.execute("SELECT * from Add_lib2")
        for row in cur:
            Libcontect_label = tk.Label(self, text= row  ,font=LARGE_FONT)
            Libcontect_label.pack(pady=10,padx=10)
        #return cur.fetchall()
        #cur.close()

app = Myproj()
app.mainloop()
