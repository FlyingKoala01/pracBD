import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
from PIL import ImageTk, Image
from tkinter import filedialog

import queries
import input_manager
_script = os.path.abspath(__file__)

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light' 


_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    style.configure('Vertical.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    style.configure('Horizontal.TScrollbar',  background=_bgcolor,
        arrowcolor= _fgcolor)
    style.configure('Treeview',  font="TkDefaultFont")
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("800x500+346+136")
        top.resizable(0,  0)
        top.title("Dipse Gestor de Contactes")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.Button1 = tk.Button(self.top,command=self.spawn_top_level_3)
        self.Button1.place(relx=0.013, rely=0.899, height=24, width=147)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="Blue")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Eliminar Seleccionat''')
        self.Button2 = tk.Button(self.top, command=self.spawn_top_level_2)
        self.Button2.place(relx=0.513, rely=0.893, height=24, width=185)
        self.Button2.configure(activebackground="beige")
        self.Button2.configure(activeforeground="black")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(compound='left')
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="blue")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Modificar seleccionat''')
        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.628, rely=0.029, relheight=0.346
                , relwidth=0.369)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(relx=0.04, rely=0.167, height=24, width=71)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="blue")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Nom:''')
        self.Label3 = tk.Label(self.Frame1)
        self.Label3.place(relx=0.04, rely=0.333, height=39, width=64)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="blue")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Telèfon:''')
        self.Label7 = tk.Label(self.Frame1)
        self.Label7.place(relx=0.04, rely=0.620, height=24, width=44)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(anchor='w')
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(compound='left')
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(foreground="blue")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Imatge:''')
        self.Button7 = tk.Button(self.Frame1, command=self.browse_file)
        self.Button7.place(relx=0.7, rely=0.62, height=26, width=75)
        self.Button7.configure(activebackground="beige")
        self.Button7.configure(activeforeground="black")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="blue")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Browse...''')

        self.Text1 = tk.Text(self.Frame1)
        self.Text1.place(relx=0.283, rely=0.167, relheight=0.11, relwidth=0.474)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(wrap="word")
        self.Text2 = tk.Text(self.Frame1)
        self.Text2.place(relx=0.283, rely=0.417, relheight=0.11, relwidth=0.478)
        self.Text2.configure(background="white")
        self.Text2.configure(font="TkTextFont")
        self.Text2.configure(foreground="black")
        self.Text2.configure(highlightbackground="#d9d9d9")
        self.Text2.configure(highlightcolor="black")
        self.Text2.configure(insertbackground="black")
        self.Text2.configure(selectbackground="#c4c4c4")
        self.Text2.configure(selectforeground="black")
        self.Text2.configure(wrap="word")
        self.Text3 = tk.Text(self.Frame1, state="disabled")
        self.Text3.place(relx=0.283, rely=0.617, relheight=0.11, relwidth=0.400)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(foreground="black")
        self.Text3.configure(highlightbackground="#d9d9d9")
        self.Text3.configure(highlightcolor="black")
        self.Text3.configure(insertbackground="black")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(selectforeground="black")
        self.Text3.configure(wrap="word")
        self.Button5 = tk.Button(self.Frame1, command=self.afegir_contacte)
        self.Button5.place(relx=0.545, rely=0.800, height=24, width=120)
        self.Button5.configure(activebackground="beige")
        self.Button5.configure(activeforeground="black")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(compound='left')
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="blue")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Afegir Contacte''')
        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.673, rely=0.0, height=24, width=90)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="blue")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Nou Registre''')
        _style_code()
        self.Scrolledtreeview1 = ScrolledTreeView(self.top)
        self.Scrolledtreeview1.bind("<<TreeviewSelect>>", self.treeview_select)
        self.Scrolledtreeview1.place(relx=0.300, rely=0.403, relheight=0.478
                , relwidth=0.500)
        self.Scrolledtreeview1.configure(columns=("ID", "Nom", "Tel"))
        self.Scrolledtreeview1.column("#0", width=0, stretch=tk.NO)
        self.Scrolledtreeview1.configure(selectmode="browse") 
        # build_treeview_support starting.
        self.Scrolledtreeview1.column("ID",width=0, stretch=False)
        self.Scrolledtreeview1.heading("Nom",text="Nom")
        self.Scrolledtreeview1.heading("Nom",anchor="center")
        self.Scrolledtreeview1.column("Nom",width="120")
        self.Scrolledtreeview1.column("Nom",stretch="1")
        self.Scrolledtreeview1.column("Nom",anchor="w")
        self.Scrolledtreeview1.heading("Tel",text="Tel.")
        self.Scrolledtreeview1.heading("Tel",anchor="center")
        self.Scrolledtreeview1.column("Tel",width="120")
        self.Scrolledtreeview1.column("Tel",stretch="1")
        self.Scrolledtreeview1.column("Tel",anchor="w")

        self.Canvas1 = tk.Canvas(self.top)
        self.Canvas1.place(relx=0.012, rely=0.429, relheight=0.346, relwidth=0.200)
        self.Canvas1.configure(background="white")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")

        self.Canvas2 = tk.Canvas(self.top)
        self.Canvas2.place(relx=0.045, rely=0.029, relheight=0.245
                , relwidth=0.522)
        self.Canvas2.configure(background="#d9d9d9")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(highlightbackground="#d9d9d9")
        self.Canvas2.configure(highlightcolor="black")
        self.Canvas2.configure(insertbackground="black")
        self.Canvas2.configure(relief="ridge")
        self.Canvas2.configure(selectbackground="#c4c4c4")
        self.Canvas2.configure(selectforeground="black")
        self.Button4 = tk.Button(self.top, command=self.sortir)
        self.Button4.place(relx=0.882, rely=0.893, height=24, width=67)
        self.Button4.configure(activebackground="beige")
        self.Button4.configure(activeforeground="black")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(compound='left')
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="blue")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Sortir''')
        self.Message1 = tk.Message(self.top)
        self.Message1.place(relx=0.807, rely=0.432, relheight=0.314, relwidth=0.179)

        self.Message1.configure(background="#d9d9d9")
        self.Message1.configure(highlightbackground="#d9d9d9")
        self.Message1.configure(highlightcolor="black")
        self.Message1.configure(padx="1")
        self.Message1.configure(pady="1")
        self.Message1.configure(width=120)

        image_file = os.path.join(os.path.dirname(__file__), "upc.png")
        self.img1 = Image.open(image_file)
        self.img1 = self.img1.resize((420, 122), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.Canvas2.create_image(0, 0, anchor=NW, image=self.img1)

        self.mostrar_contactes()

    def afegir_contacte(self):
        nom = self.Text1.get('1.0', 'end').rstrip('\n')
        tel = self.Text2.get('1.0', 'end').rstrip('\n')
        filename = self.Text3.get('1.0', 'end').rstrip('\n')
        if (input_manager.valid_name(nom) and input_manager.valid_phone(tel)) and (filename == "" or input_manager.valid_image(filename)):
            if not queries.exists(nom, tel):
                queries.insert_contact(nom, tel, filename if filename!='' else None)
                self.Message1.configure(text='Contacte Afegit: \n' + 'Nom: ' + nom + '\n' + 'Tel: ' +  tel, foreground='red')
            else:
                self.Message1.configure(text='Combinacio nom-tel existent', foreground='red')
        else:
            self.Message1.configure(text='Format Incorrecte', foreground='red')

        self.Text1.delete('1.0', END)
        self.Text2.delete('1.0', END)
        self.Text3.configure(state="normal")
        self.Text3.delete('1.0', tk.END)
        self.Text3.configure(state="disabled")
        self.mostrar_contactes()

    def mostrar_contactes(self):
        for row in self.Scrolledtreeview1.get_children():
            self.Scrolledtreeview1.delete(row)

        contacts = queries.show_contacts()
        for contact in contacts:
            new_name = contact[1].replace(" ", "\ ")
            new_tel = contact[2].replace(" ", "\ ")
            self.Scrolledtreeview1.insert('', 'end', values=f"{contact[0]}\t{new_name}\t{new_tel}")

    def browse_file(self):
        filepath = filedialog.askopenfilename(title="Select file", filetypes=[("Image files", "*.jpg *.png")])
        if filepath:
            self.Text3.configure(state="normal")
            self.Text3.delete("1.0", tk.END)
            self.Text3.insert("1.0", filepath)
            self.Text3.configure(state="disabled")

    def treeview_select(self, event):
        #Get the selected item
        selection = self.Scrolledtreeview1.selection()
        if selection:
            contact_id, _, _ = _w1.Scrolledtreeview1.item(selection, 'values')

            filename = queries.get_image_from_id(contact_id)

            if filename == None:
                self.Canvas1.create_image(0, 0, anchor='nw', image=None)
                self.Canvas1.image = None
                return

            # Get the image path
            image_path = os.path.join(queries._images, filename)
            #Load the image
            image = Image.open(image_path)
            image.thumbnail((175, 175))
            #Convert the image to Tkinter format
            photo = ImageTk.PhotoImage(image)
            #Display the image on the canvas
            self.Canvas1.create_image(0, 0, anchor='nw', image=photo)
            self.Canvas1.image = photo


    def sortir(self):
        self.top.destroy()
    

    # Modify contact
    def spawn_top_level_2(self):
        selected_item = self.Scrolledtreeview1.selection()
        if selected_item:
            # Creates a toplevel widget.
            global _top2, _w2
            _top2 = tk.Toplevel(root)
            _w2 = Toplevel2(_top2)


    # Delete contact
    def spawn_top_level_3(self):
        selected_item = self.Scrolledtreeview1.selection()
        if selected_item:
            # Creates a toplevel widget.
            global _top3, _w3
            _top3 = tk.Toplevel(root)
            _w3 = Toplevel3(_top3)

    
class Toplevel2:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("300x140+720+540")
        top.resizable(0,  0)
        top.title("Modificar Contacte")
        top.configure(background="#d9d9d9")

        self.top = top

        contact = _w1.Scrolledtreeview1.selection()
        id, name, phone = _w1.Scrolledtreeview1.item(contact, 'values')

        self.Label4 = tk.Label(self.top)
        self.Label4.place(relx=0.036, rely=0.083, height=21, width=64)
        self.Label4.configure(anchor='w')
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="blue")
        self.Label4.configure(text='''Name:''')
        self.Label5 = tk.Label(self.top)
        self.Label5.place(relx=0.036, rely=0.25, height=21, width=77)
        self.Label5.configure(anchor='w')
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(compound='left')
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="blue")
        self.Label5.configure(text='''Telèfon antic:''')
        self.Label6 = tk.Label(self.top)
        self.Label6.place(relx=0.036, rely=0.417, height=21, width=72)
        self.Label6.configure(anchor='w')
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(compound='left')
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(foreground="blue")
        self.Label6.configure(text='''Nou telèfon:''')
        self.Label7 = tk.Label(self.top)
        self.Label7.place(relx=0.036, rely=0.583, height=21, width=90)
        self.Label7.configure(anchor='w')
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(compound='left')
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(foreground="blue")
        self.Label7.configure(text='''Imatge:''')

        self.Text3 = tk.Text(self.top, state="disabled")
        self.Text3.place(relx=0.36, rely=0.583, relheight=0.14, relwidth=0.332)
        self.Text3.configure(background="white")
        self.Text3.configure(font="TkTextFont")
        self.Text3.configure(foreground="black")
        self.Text3.configure(highlightbackground="#d9d9d9")
        self.Text3.configure(highlightcolor="black")
        self.Text3.configure(insertbackground="black")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(selectforeground="black")
        self.Text3.configure(wrap="word")

        self.Button7 = tk.Button(self.top, command=self.browse_file)
        self.Button7.place(relx=0.7, rely=0.583, height=23, width=65)
        self.Button7.configure(activebackground="beige")
        self.Button7.configure(activeforeground="black")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(compound='left')
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="blue")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Browse...''')

        self.Message3 = tk.Message(self.top)
        self.Message3.place(relx=0.36, rely=0.083, relheight=0.158
                , relwidth=0.432)
        self.Message3.configure(background="#d9d9d9")
        self.Message3.configure(foreground="#000000")
        self.Message3.configure(highlightbackground="#d9d9d9")
        self.Message3.configure(highlightcolor="black")
        self.Message3.configure(padx="1")
        self.Message3.configure(pady="1")
        self.Message3.configure(text=f'{name}')
        self.Message3.configure(width=120)
        self.Message4 = tk.Message(self.top)
        self.Message4.place(relx=0.36, rely=0.25, relheight=0.158
                , relwidth=0.432)
        self.Message4.configure(background="#d9d9d9")
        self.Message4.configure(foreground="#000000")
        self.Message4.configure(highlightbackground="#d9d9d9")
        self.Message4.configure(highlightcolor="black")
        self.Message4.configure(padx="1")
        self.Message4.configure(pady="1")
        self.Message4.configure(text=f'{phone}')
        self.Message4.configure(width=120)
        self.Text4 = tk.Text(self.top)
        self.Text4.place(relx=0.36, rely=0.417, relheight=0.14, relwidth=0.482)
        self.Text4.configure(background="white")
        self.Text4.configure(font="TkTextFont")
        self.Text4.configure(foreground="black")
        self.Text4.configure(highlightbackground="#d9d9d9")
        self.Text4.configure(highlightcolor="black")
        self.Text4.configure(insertbackground="black")
        self.Text4.configure(selectbackground="#c4c4c4")
        self.Text4.configure(selectforeground="black")
        self.Text4.configure(wrap="word")
        self.Button6 = tk.Button(self.top, command=lambda: self.modify_contact(id, name))
        self.Button6.place(relx=0.60, rely=0.80, height=24, width=117)
        self.Button6.configure(activebackground="beige")
        self.Button6.configure(activeforeground="black")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(compound='left')
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="blue")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''Modificar Contacte''')
    
    def modify_contact(self, id, name):
        new_phone = self.Text4.get('1.0', 'end-1c')
        new_image_path = self.Text3.get('1.0', 'end-1c')
        if input_manager.valid_phone(new_phone) and not queries.exists(name, new_phone):
            queries.modify_phone(id,new_phone)
        if input_manager.valid_image(new_image_path):
            queries.modify_image(id, new_image_path)
        _w1.mostrar_contactes()
        self.top.destroy()

    def browse_file(self):
        filepath = filedialog.askopenfilename(title="Select file", filetypes=[("Image files", "*.jpg *.png")])
        if filepath:
            self.Text3.configure(state="normal")
            self.Text3.delete("1.0", tk.END)
            self.Text3.insert("1.0", filepath)
            self.Text3.configure(state="disabled")


class Toplevel3:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("283x136+381+536")
        top.minsize(120, 1)
        top.maxsize(3844, 1061)
        top.resizable(1,  1)
        top.title("Eliminar Contacte")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Button7 = tk.Button(self.top, command=self.delete_contact)
        self.Button7.place(relx=0.177, rely=0.662, height=34, width=64)
        self.Button7.configure(activebackground="beige")
        self.Button7.configure(activeforeground="black")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(compound='left')
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="red")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Eliminar''')
        self.Message6 = tk.Message(self.top)
        self.Message6.place(relx=0.283, rely=0.147, relheight=0.36
                , relwidth=0.495)
        self.Message6.configure(background="#d9d9d9")
        self.Message6.configure(foreground="#000000")
        self.Message6.configure(highlightbackground="#d9d9d9")
        self.Message6.configure(highlightcolor="black")
        self.Message6.configure(padx="1")
        self.Message6.configure(pady="1")
        self.Message6.configure(text='''Hey! Estas segur de eliminar aquest contacte?''')
        self.Message6.configure(width=140)
        self.Button8 = tk.Button(self.top, command=self.sortir)
        self.Button8.place(relx=0.53, rely=0.662, height=34, width=100)
        self.Button8.configure(activebackground="beige")
        self.Button8.configure(activeforeground="black")
        self.Button8.configure(background="#d9d9d9")
        self.Button8.configure(compound='left')
        self.Button8.configure(disabledforeground="#a3a3a3")
        self.Button8.configure(foreground="Blue")
        self.Button8.configure(highlightbackground="#d9d9d9")
        self.Button8.configure(highlightcolor="black")
        self.Button8.configure(pady="0")
        self.Button8.configure(text='''Torna al menu''')
    
    def delete_contact(self):
        contact = _w1.Scrolledtreeview1.selection()
        id,_,_ = _w1.Scrolledtreeview1.item(contact, 'values')
        queries.delete_contact(id)
        _w1.mostrar_contactes()
        self.top.destroy()

    def sortir(self):
        self.top.destroy()


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


def start_up():
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)

    root.mainloop()



