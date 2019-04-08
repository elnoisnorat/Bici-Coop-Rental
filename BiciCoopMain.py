import tkinter as tk

from tkinter import ttk, StringVar, font, IntVar, messagebox
#from RFID_test import RFID_Handler

LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)

BACK_GROUND = "green"

#tes = RFID_Handler()

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Alert")
    label = ttk.Label(popup, text=msg, font=MEDIUM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

class Bicicle:
    def __init__(mybicycle,plate, brand, model, tag):
        mybicycle.plate = plate
        mybicycle.brand = brand
        mybicycle.model = model
        mybicycle.tag = tag

    def set_bike(mybicycle,plate, brand, model, tag):
        mybicycle.plate = plate
        mybicycle.brand = brand
        mybicycle.model = model
        mybicycle.tag = tag

    def get_plate(mybicycle):
        return mybicycle.plate

    def get_brand(mybicycle):
        return mybicycle.tag

    def get_model(mybicycle):
        return mybicycle.tag

    def get_tag(mybicycle):
        return mybicycle.tag

myB = Bicicle("","","","")


class BiciCoopRentalapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Container
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "BiciCoop Rental")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # MenuBar
        menubar = tk.Menu(container)
        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Connection", command=lambda: popupmsg("Not supported just yet!"))
        settingsmenu.add_command(label="Administrator", command=lambda: popupmsg("Not supported just yet!"))
        settingsmenu.add_command(label="Layout", command=lambda: popupmsg("Not supported just yet!"))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Getting Started", command=lambda: popupmsg("Not supported just yet!"))
        helpmenu.add_command(label="Summit Feedback", command=lambda: popupmsg("Not supported just yet!"))
        helpmenu.add_command(label="Summit a Bug Report", command=lambda: popupmsg("Not supported just yet!"))
        helpmenu.add_separator()
        helpmenu.add_command(label="About", command=lambda: popupmsg("Not supported just yet!"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.Tk.config(self, menu=menubar)
        # Frames
        self.frames = {}

        for F in (LoginPage, ForgotPage, MainPage, ReceivePage, ReleasePage, InventoryPage, NewBike, EditBike, MaintenancePage, RequestPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background=BACK_GROUND)
            rows = 0
            while rows < 10:
                frame.rowconfigure(rows, weight=1)
                frame.columnconfigure(rows, weight=1)
                rows += 1
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear_widget(event):

            if entry_user == self.focus_get() and entry_user.get() == "Enter Email":
                entry_user.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_user != self.focus_get() and entry_user.get() == "":
                entry_user.insert(0, "Enter Email")

        def clean():
            entry_user.delete(0, 'end')
            entry_user.insert(0, "Enter Email")
            entry_pass.delete(0, 'end')

        def validate(event):

            val = str(entry_user.get())
            if val.find('@') == -1 or val.count("@") != 1:
                messagebox.showwarning("Alert", "Invalid Entry")
            elif val.find(".") == -1 or val.rindex('.') != len(val) - 4:
                messagebox.showwarning("Alert", "Invalid Entry")
            elif len(str(entry_pass.get())) < 8:
                messagebox.showwarning("Alert", "Invalid Entry")
            else: #send to server
                clean()
                controller.show_frame(MainPage)

        label_login = tk.Label(self, text="Login Page", font=LARGE_FONT, bg=BACK_GROUND)
        label_login.grid(row=0, columnspan=10)

        label_user = tk.Label(self, text="User Name:", font=SMALL_FONT, bg=BACK_GROUND)
        label_user.grid(row=3, column=3, sticky='E')

        entry_user = ttk.Entry(self)
        entry_user.insert(0, "Enter Email")
        entry_user.config(width=50)
        entry_user.bind('<FocusIn>', clear_widget)
        entry_user.bind('<FocusOut>', repopulate_defaults)
        entry_user.grid(row=3, column=4, sticky='W')

        label_pass = tk.Label(self, text="Password:", font=SMALL_FONT, bg=BACK_GROUND)
        label_pass.grid(row=4, column=3, sticky='E')
        entry_pass = ttk.Entry(self, show='*')
        entry_pass.insert(0, "")
        entry_pass.config(width=50)
        entry_pass.bind('<FocusIn>', clear_widget)
        entry_pass.bind('<FocusOut>', repopulate_defaults)
        entry_pass.grid(row=4, column=4, sticky='W')

        entry_forgot = tk.Button(self, text="Forgot Password", borderwidth=0, bg=BACK_GROUND,
                                 command=lambda: [clean(), controller.show_frame(ForgotPage)])
        entry_forgot.grid(row=5, columnspan=10)
        f = font.Font(entry_forgot, entry_forgot.cget("font"))
        f.configure(underline=True)
        entry_forgot.config(font=f, foreground="blue")

        button1 = ttk.Button(self, text="Login",
                             command=lambda: validate('<FocusIn>'))
        button1.grid(row=6, columnspan=10)


class ForgotPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear_widget(event):

            if entry_b == self.focus_get() and entry_b.get() == "Email":
                entry_b.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_b != self.focus_get() and entry_b.get() == "":
                entry_b.insert(0, "Email")

        def clean():
            entry_b.delete(0, 'end')
            entry_b.insert(0, "Email")

        def validate(event):

            val = str(entry_b.get())
            if val.find('@') == -1 or val.count("@") != 1:
                messagebox.showwarning("Alert", "Invalid email")
            elif val.find(".") == -1 or val.rindex('.') != len(val) - 4:
                messagebox.showwarning("Alert", "Invalid email")
            else: #send to server
                entry_b.delete(0, 'end')
                entry_b.insert(0, "Email")
                controller.show_frame(LoginPage)

        label_b = ttk.Label(self, text="Recover an account:", font=LARGE_FONT, background=BACK_GROUND)
        label_b.grid(row=1, columnspan=10)

        label_b = ttk.Label(self, text="Enter Email:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_b.grid(row=3, columnspan=5, sticky='E')

        entry_b = ttk.Entry(self)
        entry_b.grid(row=3, column=5, columnspan=4, sticky='W')
        entry_b.config(width=30)
        entry_b.insert(0, "Email")
        entry_b.bind('<FocusIn>', clear_widget)
        entry_b.bind('<FocusOut>', repopulate_defaults)
        entry_b.bind('<Return>', validate)

        button_send = ttk.Button(self, text="Send", command=lambda: validate('<FocusIn>'))
        button_send.grid(row=5, column=4, sticky='E')

        button_back = ttk.Button(self, text="Back", command=lambda: [clean(), controller.show_frame(LoginPage)])
        button_back.grid(row=5, column=5, sticky='E')


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        rootFrame = tk.Frame(self, bg="blue")
        rootFrame.pack(side='top')
        topFrame = tk.Frame(self, bg="red")
        topFrame.pack()
        midrFrame = tk.Frame(self, bg="brown")
        midrFrame.pack(side='right', padx=50)
        midlFrame = tk.Frame(self, bg="purple")
        midlFrame.pack(side='left', padx=50)
        midFrame = tk.Frame(self, bg="green")
        midFrame.pack()
        lowFrame = tk.Frame(self, bg="orange")
        lowFrame.pack(side='bottom')

        button1 = ttk.Button(rootFrame, text="Logout",
                             command=lambda: controller.show_frame(LoginPage))
        button1.pack(pady=10)

        label = tk.Label(topFrame, text="Main", font=LARGE_FONT)
        label.pack(pady=10)

        label_ava = ttk.Label(midlFrame, text="Available:", font=SMALL_FONT, background=BACK_GROUND)
        label_ava.pack(side='top')
        entry_ava = ttk.Entry(midlFrame, width=5)
        entry_ava.pack(side='top')
        label_req = ttk.Label(midlFrame, text="Requested:", font=SMALL_FONT, background=BACK_GROUND)
        label_req.pack(side='top')
        entry_req = ttk.Entry(midlFrame, width=5)
        entry_req.pack(side='top')
        # entry_brand.insert(0, "Brand")
        # entry_brand.bind('<FocusIn>', clear_widget)
        # entry_brand.bind('<FocusOut>', repopulate_defaults)

        label_ser = ttk.Label(midrFrame, text="Services:", font=SMALL_FONT, background=BACK_GROUND)
        label_ser.pack(side='top')
        entry_ser = ttk.Entry(midrFrame, width=5)
        entry_ser.pack(side='top')
        label_man = ttk.Label(midrFrame, text="Maintenance:", font=SMALL_FONT, background=BACK_GROUND)
        label_man.pack(side='top')
        entry_man = ttk.Entry(midrFrame, width=5)
        entry_man.pack(side='top')

        # entry_brand.insert(0, "Brand")
        # entry_brand.bind('<FocusIn>', clear_widget)
        # entry_brand.bind('<FocusOut>', repopulate_defaults)

        button1 = ttk.Button(lowFrame, text="Maintenance",
                             command=lambda: controller.show_frame(MaintenancePage))
        button1.pack(side='left', anchor="nw", pady=30)
        button2 = ttk.Button(lowFrame, text="Inventory",
                             command=lambda: controller.show_frame(InventoryPage))
        button2.pack(side='left', anchor="ne")
        button3 = ttk.Button(lowFrame, text="Receive",
                             command=lambda: controller.show_frame(ReceivePage))
        button3.pack(side='left', anchor='se', pady=20)
        button4 = ttk.Button(lowFrame, text="Release",
                             command=lambda: controller.show_frame(ReleasePage))
        button4.pack(side='left', anchor='sw', pady=30)


class ReceivePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tries = IntVar()
        tag.set("RFID TAG")
        tries.set(0)

        topFrame = tk.Frame(self, bg=BACK_GROUND)
        topFrame.pack(side='top', fill='both', pady=50)
        miduFrame = tk.Frame(self, bg=BACK_GROUND)
        miduFrame.pack(fill='both')
        middFrame = tk.Frame(self, bg=BACK_GROUND)
        middFrame.pack(fill='both', pady=30)
        lowFrame = tk.Frame(self, bg=BACK_GROUND)
        lowFrame.pack(side='bottom')

        def identify():

            if tries.get() == 4:
                entry_con.lift()
            else:
                cmp = str(tes.scanRFID())
                if cmp == "Verify and try again":
                    tries.set(tries.get() + 1)
                    tag.set(cmp + " (" + str(tries.get()) + ")")
                elif len(cmp) == 21:
                    tries.set(0)
                    tag.set(cmp[2:20])
                else:
                    tag.set("NPI")

        def clear_widget(event):

            if entry_con == self.focus_get() and entry_con.get() == "Insert Plate":
                entry_con.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_con != self.focus_get() and entry_con.get() == "":
                entry_con.insert(0, "Insert Plate")

        def clean():
            entry_con.lower()
            entry_con.delete(0, 'end')
            entry_con.insert(0, "Insert Plate")
            tag.set("RFID TAG")
            tries.set(0)

        label = ttk.Label(topFrame, text="Receive Bicycle", font=LARGE_FONT, background=BACK_GROUND)
        label.pack(side='top')

        entry_con = tk.Entry(self, font=MEDIUM_FONT)
        entry_con.pack(in_=miduFrame)
        entry_con.insert(0, "Insert Plate")
        entry_con.bind('<FocusIn>', clear_widget)
        entry_con.bind('<FocusOut>', repopulate_defaults)
        entry_con.lower()

        button_scan = ttk.Button(middFrame, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.pack()
        label2 = tk.Label(middFrame, textvariable=tag, background=BACK_GROUND, font=SMALL_FONT, width=30)
        label2.pack()

        button_send = ttk.Button(lowFrame, text="Send",
                                 command=lambda: [clean(), controller.show_frame(MainPage)])
        button_send.pack(side='left', padx=55, pady=20)
        button_cancel = ttk.Button(lowFrame, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MainPage)])
        button_cancel.pack(side='left', padx=55, pady=20)


class ReleasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tries = IntVar()
        tag.set("RFID TAG")
        tries.set(0)

        def identify():

            cmp = str(tes.scanRFID())
            if cmp == "Verify and try again":
                tries.set(tries.get() + 1)
                tag.set(cmp + " (" + str(tries.get()) + ")")
            elif len(cmp) == 21:
                tries.set(0)
                tag.set(cmp[2:20])
            else:
                tag.set("NPI")

        def clear_widget(event):

            if entry_con == self.focus_get() and entry_con.get() == "Confirmation Code":
                entry_con.delete(0, 'end')
            #######RFID

        def repopulate_defaults(event):

            if entry_con != self.focus_get() and entry_con.get() == "":
                entry_con.insert(0, "Confirmation Code")
            #######RFID

        def clean():
            entry_con.delete(0, 'end')
            entry_con.insert(0, "Confirmation Code")
            tag.set("RFID TAG")
            tries.set(0)

        def validate():
            if entry_con.get() == "Confirmation Code":
                messagebox.showwarning("Alert", "Insert Confirmation Code")
            else:
                # to server.....
                clean()
                controller.show_frame(MainPage)



        label = ttk.Label(self, text="Release a Bicycle", font=LARGE_FONT, background=BACK_GROUND)
        label.grid(row=1, columnspan=10)

        entry_con = tk.Entry(self, font=MEDIUM_FONT)
        entry_con.grid(row=3, columnspan=10)
        entry_con.insert(0, "Confirmation Code")
        entry_con.bind('<FocusIn>', clear_widget)
        entry_con.bind('<FocusOut>', repopulate_defaults)

        button_scan = ttk.Button(self, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.grid(row=6, columnspan=10, sticky='N')
        label2 = tk.Label(self, textvariable=tag, background=BACK_GROUND, font=SMALL_FONT, width=30)
        label2.grid(row=6, columnspan=10, sticky='S')

        button_send = ttk.Button(self, text="Send",
                                 command=lambda: [validate()])
        button_send.grid(row=9, column=4, sticky='W')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MainPage)])
        button_cancel.grid(row=9, column=6, sticky='W')


class InventoryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        rootFrame = tk.Frame(self, bg="blue")
        rootFrame.pack(side='top')
        topFrame = tk.Frame(self, bg="red")
        topFrame.pack(pady=20)
        midrFrame = tk.Frame(self, bg="brown")
        midrFrame.pack(side='right', padx=50)
        midlFrame = tk.Frame(self, bg="purple")
        midlFrame.pack(side='left', padx=50)
        midFrame = tk.Frame(self, bg="green")
        midFrame.pack()
        lowFrame = tk.Frame(self, bg="orange")
        lowFrame.pack(side='bottom', pady=10)

        def active(event):
            button2.configure(state='enable')

        def disable():
            button2.configure(state='disable')

        def populate():
            myB.set_bike("mogo", "loco", "cas", "tid")
            controller.show_frame(EditBike)

        def popup():
            popup = tk.Tk()
            popup.wm_title("New Bike")
            popup.geometry("300x100")
            rows = 0
            while rows < 4:
                popup.rowconfigure(rows, weight=1)
                popup.columnconfigure(rows, weight=1)
                rows += 1
            popup.rowconfigure(5, weight=1)
            label_b = ttk.Label(popup, text=entry_brand.get() + " " + entry_model.get()
                                            + " " + entry_plate.get(), font=MEDIUM_FONT)
            label_b.grid(row=1, columnspan=4)
            # toserver
            button_send_p = ttk.Button(popup, text="Send", command=lambda: [popup.destroy(), clean(),
                                                                            controller.show_frame(InventoryPage)])
            button_send_p.grid(row=4, column=1)
            button_cancel_p = ttk.Button(popup, text="Cancel", command=popup.destroy)
            button_cancel_p.grid(row=4, column=2)
            popup.mainloop()

        label = tk.Label(topFrame, text="Inventory", font=LARGE_FONT,  bg=BACK_GROUND)
        label.pack()

        label_aval = tk.Label(midFrame, text="Available", font=SMALL_FONT)
        label_aval.pack(side='top', fill='both')

        tree = ttk.Treeview(midFrame, columns=('Plate', 'Brand', 'Model', 'Tag'), height=8, selectmode='browse')
        tree.heading('#0', text='Plate')
        tree.heading('#1', text='Brand')
        tree.heading('#2', text='Model')
        tree.heading('#3', text='Tag')
        tree.column('#0', stretch=tk.NO, width=80)
        tree.column('#1', stretch=tk.NO, width=135)
        tree.column('#2', stretch=tk.NO, width=135)
        tree.column('#3', stretch=tk.NO, width=235)

        for line in range(100):
            tree.insert('', tk.END, text=line, values=("Model", "Brand", "RFID_Tag"))

        tree.pack(side='left', fill='both')
        scrollbar = ttk.Scrollbar(midFrame, orient="vertical", command=tree.yview)
        scrollbar.place(x=581, y=0, height=210)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind('<FocusIn>', active)
        # tree.delete(*tree.get_children())


        button1 = ttk.Button(self, text="New", width=10, padding=15,
                             command=lambda: [disable(), controller.show_frame(NewBike)])
        button1.pack(side='left', padx=90)
        button2 = ttk.Button(self, text="Edit", width=10, padding=15, state='disable',
                             command=lambda: [populate(), disable()])
        button2.pack(side='right', padx=90)

        button_back = ttk.Button(lowFrame, text="Back", width=10,
                                 command=lambda: [disable(), controller.show_frame(MainPage)])
        button_back.pack()


class NewBike(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear_widget(event):

            if entry_brand == self.focus_get() and entry_brand.get() == "Brand":
                entry_brand.delete(0, 'end')
            elif entry_model == self.focus_get() and entry_model.get() == "Model":
                entry_model.delete(0, 'end')
            elif entry_plate == self.focus_get() and entry_plate.get() == "Plate":
                entry_plate.delete(0, 'end')
            #######RFID

        def repopulate_defaults(event):

            if entry_brand != self.focus_get() and entry_brand.get() == "":
                entry_brand.insert(0, "Brand")
            elif entry_model != self.focus_get() and entry_model.get() == "":
                entry_model.insert(0, "Model")
            elif entry_plate != self.focus_get() and entry_plate.get() == "":
                entry_plate.insert(0, "Plate")
            #######RFID

        def clean():
            entry_brand.delete(0, 'end')
            entry_brand.insert(0, "Brand")
            entry_model.delete(0, 'end')
            entry_model.insert(0, "Model")
            entry_plate.delete(0, 'end')
            entry_plate.insert(0, "Plate")
            #######RFID

        def validate():

            if entry_brand.get() == "Brand":
                messagebox.showwarning("Alert", "Insert Brand")
            elif entry_model.get() == "Model":
                messagebox.showwarning("Alert", "Insert Model")
            elif entry_plate.get() == "Plate":
                messagebox.showwarning("Alert", "Insert Plate")
            else:  # Send to server
                anw = messagebox.askokcancel("Confirm entries", entry_brand.get() + " " + entry_model.get()
                                    + " " + entry_plate.get() + "\n" + tag.get())
                if anw == True: #To server
                    clean()
                    controller.show_frame(InventoryPage)


        tag = StringVar()
        tag.set("     RFID TAG     ")

        label = ttk.Label(self, text="New Bicycle:", font=LARGE_FONT, background=BACK_GROUND)
        label.grid(row=1, columnspan=10)

        label_brand = ttk.Label(self, text="Brand:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_brand.grid(row=3, column=3, sticky='E')
        entry_brand = ttk.Entry(self)
        entry_brand.grid(row=3, column=4, sticky='W')
        entry_brand.insert(0, "Brand")
        entry_brand.bind('<FocusIn>', clear_widget)
        entry_brand.bind('<FocusOut>', repopulate_defaults)

        label_model = ttk.Label(self, text="Model:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_model.grid(row=3, column=5, sticky='E')
        entry_model = ttk.Entry(self)
        entry_model.grid(row=3, column=6, sticky='W')
        entry_model.insert(0, "Model")
        entry_model.bind('<FocusIn>', clear_widget)
        entry_model.bind('<FocusOut>', repopulate_defaults)

        label_plate = ttk.Label(self, text="Plate:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_plate.grid(row=4, column=4, sticky='E')
        entry_plate = ttk.Entry(self)
        entry_plate.grid(row=4, column=5, sticky='W')
        entry_plate.insert(0, "Plate")
        entry_plate.bind('<FocusIn>', clear_widget)
        entry_plate.bind('<FocusOut>', repopulate_defaults)

        button_scan = ttk.Button(self, text="Scan",
                                 command=lambda: scanRFID())
        button_scan.grid(row=6, column=4, sticky='E')

        label2 = tk.Label(self, textvariable=tag, background=BACK_GROUND)
        label2.grid(row=6, column=5, sticky='W')

        button_send = ttk.Button(self, text="Add",
                                 command=lambda: validate())
        button_send.grid(row=9, column=4, sticky='E')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(InventoryPage)])
        button_cancel.grid(row=9, column=5, sticky='E')


class EditBike(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear_widget(event):

            if entry_brand == self.focus_get() and entry_brand.get() == "Brand":
                entry_brand.delete(0, 'end')
            elif entry_model == self.focus_get() and entry_model.get() == "Model":
                entry_model.delete(0, 'end')
            elif entry_plate == self.focus_get() and entry_plate.get() == "Plate":
                entry_plate.delete(0, 'end')
            #######RFID

        def repopulate_defaults(event):

            if entry_brand != self.focus_get() and entry_brand.get() == "":
                entry_brand.insert(0, "Brand")
            elif entry_model != self.focus_get() and entry_model.get() == "":
                entry_model.insert(0, "Model")
            elif entry_plate != self.focus_get() and entry_plate.get() == "":
                entry_plate.insert(0, "Plate")
            #######RFID

        def clean():
            entry_brand.delete(0, 'end')
            entry_brand.insert(0, "Brand")
            entry_model.delete(0, 'end')
            entry_model.insert(0, "Model")
            entry_plate.delete(0, 'end')
            entry_plate.insert(0, "Plate")
            #######RFID

        def popup_msg():
            popup = tk.Tk()
            popup.wm_title("New Bike")
            popup.geometry("300x100")
            rows = 0
            while rows < 4:
                popup.rowconfigure(rows, weight=1)
                popup.columnconfigure(rows, weight=1)
                rows += 1
            popup.rowconfigure(5, weight=1)

            if entry_brand.get() == "Brand" or entry_model.get() == "Model" \
                    or entry_plate.get() == "Plate":

                label_b = ttk.Label(popup, text="Invalid Entry", font=LARGE_FONT)
                label_b.grid(row=1, columnspan=4)
                button_back = ttk.Button(popup, text="Back", command=popup.destroy)
                button_back.grid(row=3, columnspan=4)
            else:  # Send to server
                label_b = ttk.Label(popup, text=entry_brand.get() + " " + entry_model.get()
                                                + " " + entry_plate.get(), font=MEDIUM_FONT)
                label_b.grid(row=1, columnspan=4)
                button_send_p = ttk.Button(popup, text="Send", command=lambda: [popup.destroy(), clean(),
                                                                                controller.show_frame(InventoryPage)])
                button_send_p.grid(row=4, column=1)
                button_cancel_p = ttk.Button(popup, text="Cancel", command=popup.destroy)
                button_cancel_p.grid(row=4, column=2)

            popup.mainloop()

        def refresh():
            entry_plate.delete(0,'end')
            entry_plate.insert(0,myB.get_plate())

        label = ttk.Label(self, text="Edit Bicycle:", font=LARGE_FONT, background="yellow")
        label.grid(row=1, columnspan=10)

        label_brand = ttk.Label(self, text="Brand:", font=MEDIUM_FONT, background="yellow")
        label_brand.grid(row=3, column=3, sticky='E')
        entry_brand = ttk.Entry(self)
        entry_brand.grid(row=3, column=4, sticky='W')
        entry_brand.insert(0, myB.get_plate())
        entry_brand.bind('<FocusIn>', clear_widget)
        entry_brand.bind('<FocusOut>', repopulate_defaults)

        label_model = ttk.Label(self, text="Model:", font=MEDIUM_FONT, background="yellow")
        label_model.grid(row=3, column=5, sticky='E')
        entry_model = ttk.Entry(self)
        entry_model.grid(row=3, column=6, sticky='W')
        entry_model.insert(0, "Model")
        entry_model.bind('<FocusIn>', clear_widget)
        entry_model.bind('<FocusOut>', repopulate_defaults)

        label_plate = ttk.Label(self, text="Plate:", font=MEDIUM_FONT, background="yellow")
        label_plate.grid(row=4, column=4, sticky='E')
        entry_plate = ttk.Entry(self)
        entry_plate.grid(row=4, column=5, sticky='W')
        entry_plate.insert(0, "Plate")
        entry_plate.bind('<FocusIn>', clear_widget)
        entry_plate.bind('<FocusOut>', repopulate_defaults)

        button_scan = ttk.Button(self, text="Scan",
                                 command=lambda: scanRFID())
        button_scan.grid(row=6, column=4, sticky='E')
        tag = StringVar()
        tag.set("     RFID TAG     ")
        label2 = tk.Label(self, textvariable=tag, background="yellow")
        label2.grid(row=6, column=5, sticky='W')

        button_send = ttk.Button(self, text="Add",
                                 command=lambda: refresh())
        button_send.grid(row=9, column=4, sticky='E')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(InventoryPage)])
        button_cancel.grid(row=9, column=5, sticky='E')


class MaintenancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        rootFrame = tk.Frame(self, bg="blue")
        rootFrame.pack(side='top')
        topFrame = tk.Frame(self, bg="red")
        topFrame.pack(pady=20)
        midrFrame = tk.Frame(self, bg="brown")
        midrFrame.pack(side='right', padx=50)
        midlFrame = tk.Frame(self, bg="purple")
        midlFrame.pack(side='left', padx=50)
        midFrame = tk.Frame(self, bg="green")
        midFrame.pack()
        lowFrame = tk.Frame(self, bg="orange")
        lowFrame.pack(side='bottom', pady=10)

        def active(event):
            button2.configure(state='enable')

        def disable():
            button2.configure(state='disable')

        label = tk.Label(topFrame, text="Maintenance", font=LARGE_FONT, bg=BACK_GROUND)
        label.pack()

        label_aval = tk.Label(midFrame, text="Service Request", font=SMALL_FONT)
        label_aval.pack(side='top', fill='both')

        tree = ttk.Treeview(midFrame, columns=('Plate', 'Brand', 'Model', 'Service'), height=8, selectmode='browse')
        tree.heading('#0', text='Plate')
        tree.heading('#1', text='Brand')
        tree.heading('#2', text='Model')
        tree.heading('#3', text='Service')
        tree.column('#0', stretch=tk.NO, width=80)
        tree.column('#1', stretch=tk.NO, width=135)
        tree.column('#2', stretch=tk.NO, width=135)
        tree.column('#3', stretch=tk.NO, width=235)

        for line in range(100):
            tree.insert('', tk.END, text="Plate", values=("Model", "Brand", "Service"))

        tree.pack(side='left', fill='both')
        scrollbar = ttk.Scrollbar(midFrame, orient="vertical", command=tree.yview)
        scrollbar.place(x=581, y=0, height=210)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind('<FocusIn>', active)
        # tree.delete(*tree.get_children())

        button1 = ttk.Button(self, text="Request", width=10, padding=15,
                             command=lambda: [disable(), controller.show_frame(RequestPage)])
        button1.pack(side='left', padx=90)
        button2 = ttk.Button(self, text="Report", width=10, padding=15, state='disable',
                             command=lambda: [disable()])
        button2.pack(side='right', padx=90)

        button_back = ttk.Button(lowFrame, text="Back", width=10,
                                 command=lambda: [disable(), controller.show_frame(MainPage)])
        button_back.pack()


class RequestPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tag.set("RFID TAG")

        topFrame = tk.Frame(self, bg=BACK_GROUND)
        topFrame.pack(side='top', fill='both', pady=50)
        miduFrame = tk.Frame(self, bg=BACK_GROUND)
        miduFrame.pack(fill='both')
        midrFrame = tk.Frame(self, bg=BACK_GROUND)
        midrFrame.pack(side='right', fill='both', pady=30)
        midlFrame = tk.Frame(self, bg=BACK_GROUND)
        midlFrame.pack(side='left', fill='both', pady=30)
        lowFrame = tk.Frame(self, bg=BACK_GROUND)
        lowFrame.pack(side='bottom')

        def identify():
            cmp = str(tes.scanRFID())
            if cmp == "Verify and try again":
                tag.set(cmp)
            elif len(cmp) == 21:
                tag.set(cmp[2:20])
            else:
                tag.set("NPI")

        def clear_widget(event):

            if entry_pla == self.focus_get() and entry_pla.get() == "Plate":
                entry_pla.delete(0, 'end')
            #######RFID

        def repopulate_defaults(event):

            if entry_pla != self.focus_get() and entry_pla.get() == "":
                entry_pla.insert(0, "Plate")
            #######RFID

        def clean():
            service_chosen.current(0)
            tag.set("RFID TAG")
            entry_pla.delete(0, 'end')
            entry_pla.insert(0,"Plate")

        def validate():
            if service_chosen.get() == "Choose One" or service_chosen.get() == "":
                messagebox.showwarning("Alert", "Choose a service")
            elif (tag.get() == "RFID TAG" or tag.get() == "Verify and try again") and entry_pla.get() == "Plate":
                messagebox.showwarning("Alert", "Identify a Bicycle")
            else:
                # to server.....
                print(entry_pla.get() + service_chosen.get() + tag.get())
                clean()
                controller.show_frame(MaintenancePage)

        label = ttk.Label(topFrame, text="Request Maintenance", font=LARGE_FONT, background=BACK_GROUND)
        label.pack(side='top')

        ttk.Label(miduFrame, text="Choose a service:", font=MEDIUM_FONT,background=BACK_GROUND).pack()
        service = tk.StringVar()
        service_chosen = ttk.Combobox(miduFrame, width=20, textvariable=service, font=SMALL_FONT, state='readonly')
        service_chosen['values'] = ('Choose One', 'Cleanup', 'Tuneup', 'Flat Tire',
                                  'Break adjustment', 'Maneuver adjustment', 'Pedal adjustment',
                                  'Transmission Adjustment', 'New Tire', 'New Break', "New Tag")
        service_chosen.current(0)
        service_chosen.pack()
        service_chosen.current(0)

        button_scan = ttk.Button(midlFrame, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.pack()
        label2 = tk.Label(midlFrame, textvariable=tag, background=BACK_GROUND, font=SMALL_FONT, width=20)
        label2.pack(padx=20)
        entry_pla = tk.Entry(midrFrame, font=MEDIUM_FONT,width=10)
        entry_pla.pack(pady=45, padx=60)
        entry_pla.insert(0, "Plate")
        entry_pla.bind('<FocusIn>', clear_widget)
        entry_pla.bind('<FocusOut>', repopulate_defaults)

        label3 = tk.Label(lowFrame, text="Scan or insert plate", background=BACK_GROUND, font=MEDIUM_FONT, width=30)
        label3.pack(pady=60)
        button_send = ttk.Button(lowFrame, text="Send",
                                 command=lambda: [validate()])
        button_send.pack(side='left', padx=55, )
        button_cancel = ttk.Button(lowFrame, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MaintenancePage)])
        button_cancel.pack(side='left', padx=55, pady=20)

app = BiciCoopRentalapp()
app.geometry("800x400")
app.resizable(width=False, height=False)
app.mainloop()