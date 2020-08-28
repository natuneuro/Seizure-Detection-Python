import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfile, askopenfilename
from PIL import Image, ImageTk
import sqlite3
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
from Modulos import LeituraArquivos,ConfusionMatrix, ProcessamentoDoSinal, LeituraEventos, AssociaTrechoEvento, CriaImagen, CNN

LARGE_FONT = ("Verdana", 12)



class Application(tk.Tk):

    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Epilepsy Detection")  

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.von_ueberall_erreichbar = 0
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def getVUE(self):
        return self.von_ueberall_erreichbar

    def raiseVUE(self, targetFrame):
        self.von_ueberall_erreichbar += 1           
        self.frames[targetFrame].label2.config(text=self.getVUE())

    def show_frame(self, targetFrame):
        frame = self.frames[targetFrame]
        self.frames[targetFrame].label2.config(text=self.getVUE())
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #status bar
        self.bar = Frame(root, relief=RIDGE, borderwidth=5)
        self.bar.pack(side=TOP)
        self.iconPath = 'logos/cerebrito.png'
        logo_cerebro = ImageTk.PhotoImage(Image.open(self.iconPath))   
        Label(self, image=logo_cerebro, bg="#DFEBE9").place(x=64, y=55)
        
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.label2 = ttk.Label(self, text=controller.getVUE(), font=LARGE_FONT)
        self.label2.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="+1",
                            command=lambda: controller.raiseVUE(StartPage))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.label2 = ttk.Label(self, text=controller.getVUE(), font=LARGE_FONT)
        self.label2.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="+1",
                            command=lambda: controller.raiseVUE(PageOne))
        button3.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.label2 = ttk.Label(self, text=controller.getVUE(), font=LARGE_FONT)
        self.label2.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = ttk.Button(self, text="+1",
                            command=lambda: controller.raiseVUE(PageTwo))
        button3.pack()
        


app = Application()




# set window size
app.geometry("1024x768")
app.resizable(0, 0)
app.config(bg="#DFEBE9")

# init menubar
menubar = tk.Menu(app)

# creating the menus
menuManage = tk.Menu(menubar, tearoff=0)

# list of menubar elements
menubar.add_cascade(menu=menuManage, label="Frame")

# menu: manage
menuManage.add_command(label="P1", command=lambda: app.show_frame(PageOne))
menuManage.add_command(label="P2", command=lambda: app.show_frame(PageTwo))
menuManage.add_command(label="Start", command=lambda: app.show_frame(StartPage))

# attach menubar
app.config(menu=menubar) 


app.mainloop()