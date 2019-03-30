import tkinter as tk

from tkinter import ttk, StringVar, font

# import serial

LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)

BACK_GROUND = "yellow"

# ser = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1.0)
ping = "0108000304FF0000"  # ping
SRequest = "010C00030410002101000000"  # Send Request
SAGCTogle = "0109000304F0000000"  # Send AGC Toggle
SAmPmToggle = "0109000304F1FF0000"  # Send AM/PM Toggle
R_ISO = "0109000304A0010000"  # Read ISO14443A


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=MEDIUM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


class BiciCoopRentalapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        #Container
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "BiciCoop Rental")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #MenuBar
        menubar = tk.Menu(container)
        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Connection", command = lambda: popupmsg("Not supported just yet!"))
        settingsmenu.add_command(label="Administrator", command = lambda: popupmsg("Not supported just yet!"))
        settingsmenu.add_command(label="Layout", command = lambda: popupmsg("Not supported just yet!"))
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
        #Frames
        self.frames = {}

        for F in (LoginPage, ForgotPage, MainPage, ReceivePage, ReleasePage, InventoryPage, NewBike):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background=BACK_GROUND)
            rows = 0
            while rows < 10:
                frame.rowconfigure(rows, weight=1)
                frame.columnconfigure(rows, weight=1)
                rows += 1
        self.show_frame(LoginPage)

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

        def popup_validate(event):

            popup = tk.Tk()
            popup.wm_title("Notification")
            popup.geometry("300x100")
            rows = 0

            while rows < 4:
                popup.rowconfigure(rows, weight=1)
                popup.columnconfigure(rows, weight=1)
                rows += 1

            val = str(entry_user.get())
            if val.find('@') != -1 and val.count("@") == 1 and val.find(".") != -1 and val.rindex('.') == len(val)-4\
                    and len(str(entry_pass.get()))>=8:
                print("bingo")
                    #send to server
                label = ttk.Label(popup, text="bingo", font=MEDIUM_FONT)
                label.grid(row=1, columnspan=4)
                B1 = ttk.Button(popup, text="Okay", command=lambda:[popup.destroy(), controller.show_frame(MainPage)])
                B1.grid(row=3, columnspan=4)
                entry_user.delete(0, 'end')
                entry_user.insert(0, "Enter Email")
                entry_pass.delete(0, 'end')
            else:
                label = ttk.Label(popup, text="Verify Entry", font=MEDIUM_FONT)
                label.grid(row=1, columnspan=4)
                B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
                B1.grid(row=3, columnspan=4)

            popup.mainloop()

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

        entry_forgot = tk.Button(self, text="Forgot Password", borderwidth=0,bg=BACK_GROUND,
                             command=lambda: controller.show_frame(ForgotPage))
        entry_forgot.grid(row=5, columnspan=10)
        f = font.Font(entry_forgot, entry_forgot.cget("font"))
        f.configure(underline=True)
        entry_forgot.config(font=f, foreground="blue")

        button1 = ttk.Button(self, text="Login",
                             command=lambda: popup_validate('<FocusIn>'))
        button1.grid(row=6, columnspan=10)


class ForgotPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear_widgetw(event):

            if entry_b == self.focus_get() and entry_b.get() == "Email":
                entry_b.delete(0, 'end')

        def repopulate_defaultsw(event):

            if entry_b != self.focus_get() and entry_b.get() == "":
                entry_b.insert(0, "Email")

        def clean():
            entry_b.delete(0, 'end')
            entry_b.insert(0, "Email")

        def popup_validate(event):

            popup = tk.Tk()
            popup.wm_title("Notification")
            popup.geometry("300x100")
            rows = 0

            while rows < 4:
                popup.rowconfigure(rows, weight=1)
                popup.columnconfigure(rows, weight=1)
                rows += 1

            val = str(entry_b.get())
            if val.find('@') != -1 and val.count("@") == 1:
                if val.find(".") != -1 and val.rindex('.') == len(val)-4:
                    print("bingo")
                    #send to server
                    label = ttk.Label(popup, text="bingo", font=MEDIUM_FONT)
                    label.grid(row=1, columnspan=4)
                    B1 = ttk.Button(popup, text="Okay", command=lambda:[popup.destroy(), controller.show_frame(LoginPage)])
                    B1.grid(row=3, columnspan=4)
                    entry_b.delete(0, 'end')
                    entry_b.insert(0, "Email")
                else:
                    print("invalid.")
                    label = ttk.Label(popup, text="Invalid Format", font=MEDIUM_FONT)
                    label.grid(row=1, columnspan=4)
                    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
                    B1.grid(row=3, columnspan=4)
            else:
                print("invalid@")
                label = ttk.Label(popup, text="Invalid Format", font=MEDIUM_FONT)
                label.grid(row=1, columnspan=4)
                B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
                B1.grid(row=3, columnspan=4)

            popup.mainloop()

        label_b = ttk.Label(self, text= "Recover an account:", font=LARGE_FONT, background="yellow")
        label_b.grid(row=1, columnspan=10)

        label_b = ttk.Label(self, text="Enter Email:", font=MEDIUM_FONT, background="yellow")
        label_b.grid(row=3, columnspan=5, sticky='E')

        entry_b = ttk.Entry(self)
        entry_b.grid(row=3, column = 5, columnspan=4, sticky='W')
        entry_b.config(width=30)
        entry_b.insert(0, "Email")
        entry_b.bind('<FocusIn>', clear_widgetw)
        entry_b.bind('<FocusOut>', repopulate_defaultsw)
        entry_b.bind('<Return>', popup_validate)

        button_send = ttk.Button(self, text="Send", command=lambda: popup_validate('<FocusIn>'))
        button_send.grid(row=5, column=4, sticky='E')

        button_back = ttk.Button(self, text="Back", command=lambda: [clean(), controller.show_frame(LoginPage)])
        button_back.grid(row=5, column=5, sticky='E')


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main", font=LARGE_FONT)
        label.grid()
#        print(worker + "i")
        button1 = ttk.Button(self, text="Logout",
                             command=lambda: controller.show_frame(LoginPage))
        button1.grid()

        button2 = ttk.Button(self, text="Inventory",
                             command=lambda: controller.show_frame(InventoryPage))
        button2.grid()

        button3 = ttk.Button(self, text="Receive",
                             command=lambda: controller.show_frame(ReceivePage))
        button3.grid()

        button4 = ttk.Button(self, text="Release",
                             command=lambda: controller.show_frame(ReleasePage))
        button4.grid()


class ReceivePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # def scanRFID():
        #      ser.write(ping.encode())
        #      print(ping.encode())
        #      rcv1 = ser.read(17)
        #      print(rcv1)
        #      ser.write(SRequest.encode())
        #      rcv1 = ser.read(27)
        #      print(rcv1)
        #      ser.write(SAGCTogle.encode())
        #      rcv1 = ser.read(12)
        #      print(rcv1)
        #      ser.write(SAmPmToggle.encode())
        #      rcv1 = ser.read(14)
        #      print(rcv1)
        #
        #      ser.write(R_ISO.encode())
        #      rcv1 = ser.read(15) #Notag
        #      rcv1 = ser.read(18)
        #
        #      if len(rcv1) < 16:
        #         print("No RFID")
        #         tag.set("No RFID")
        #      else:
        #         print(rcv1)
        #         tag.set(rcv1)

        def clean():
            entry_notification.delete("1.0", tk.END)
            print(entry_notification.get("1.0", tk.END))
            #######RFID

        label = ttk.Label(self, text="Receive Bicycle", font=LARGE_FONT, background="yellow")
        label.grid(row=1, columnspan=10)

        label = ttk.Label(self, text="Notify if any abnormal situation(optional)", font=MEDIUM_FONT, background="yellow")
        label.grid(row=2, columnspan=10,sticky='S')

        entry_notification = tk.Text(self, font=SMALL_FONT, width=30, height=6)
        entry_notification.grid(row=3, rowspan=2,columnspan=10, sticky='N')


        button_scan = ttk.Button(self, text="Scan",
                                 command=lambda: scanRFID())
        button_scan.grid(row=6, column=4, sticky='E')
        tag = StringVar()
        tag.set("     RFID TAG     ")
        label2 = tk.Label(self, textvariable=tag, background="yellow")
        label2.grid(row=6, column=5, sticky='W')

        button_send = ttk.Button(self, text="Send",
                                 command=lambda: [clean(), controller.show_frame(MainPage)])
        button_send.grid(row=9, column=4, sticky='W')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MainPage)])
        button_cancel.grid(row=9, column=6,sticky='W')


class ReleasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # def scanRFID():
        #      ser.write(ping.encode())
        #      print(ping.encode())
        #      rcv1 = ser.read(17)
        #      print(rcv1)
        #      ser.write(SRequest.encode())
        #      rcv1 = ser.read(27)
        #      print(rcv1)
        #      ser.write(SAGCTogle.encode())
        #      rcv1 = ser.read(12)
        #      print(rcv1)
        #      ser.write(SAmPmToggle.encode())
        #      rcv1 = ser.read(14)
        #      print(rcv1)
        #
        #      ser.write(R_ISO.encode())
        #      rcv1 = ser.read(15) #Notag
        #      rcv1 = ser.read(18)
        #
        #      if len(rcv1) < 16:
        #         print("No RFID")
        #         tag.set("No RFID")
        #      else:
        #         print(rcv1)
        #         tag.set(rcv1)

        def clean():
            entry_notification.delete(0, 'end')
            #######RFID

        label = ttk.Label(self, text="Release Bicycle", font=LARGE_FONT, background="yellow")
        label.grid(row=1, columnspan=10)

        entry_notification = tk.Entry(self, font=MEDIUM_FONT)
        entry_notification.grid(row=3,columnspan=10)
        entry_notification.insert(0,"    Confirmation Code")

        button_scan = ttk.Button(self, text="Scan",
                                 command=lambda: scanRFID())
        button_scan.grid(row=6, column=4, sticky='E')
        tag = StringVar()
        tag.set("     RFID TAG     ")
        label2 = tk.Label(self, textvariable=tag, background="yellow")
        label2.grid(row=6, column=5, sticky='W')

        button_send = ttk.Button(self, text="Send",
                                 command=lambda: [clean(), controller.show_frame(MainPage)])
        button_send.grid(row=9, column=4, sticky='W')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MainPage)])
        button_cancel.grid(row=9, column=6,sticky='W')

class InventoryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Inventory", font=LARGE_FONT)
        label.grid()

        button1 = ttk.Button(self, text="New",
                             command=lambda: controller.show_frame(NewBike))
        button1.grid()
        button_back = ttk.Button(self, text="Back",
                                 command=lambda: controller.show_frame(MainPage))
        button_back.grid(row=9, columnspan=10)


class NewBike(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # def scanRFID():
        #      ser.write(ping.encode())
        #      print(ping.encode())
        #      rcv1 = ser.read(17)
        #      print(rcv1)
        #      ser.write(SRequest.encode())
        #      rcv1 = ser.read(27)
        #      print(rcv1)
        #      ser.write(SAGCTogle.encode())
        #      rcv1 = ser.read(12)
        #      print(rcv1)
        #      ser.write(SAmPmToggle.encode())
        #      rcv1 = ser.read(14)
        #      print(rcv1)
        #
        #      ser.write(R_ISO.encode())
        #      rcv1 = ser.read(15) #Notag
        #      rcv1 = ser.read(18)
        #
        #      if len(rcv1) < 16:
        #         print("No RFID")
        #         tag.set("No RFID")
        #      else:
        #         print(rcv1)
        #         tag.set(rcv1)

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

        label = ttk.Label(self, text="New Bicycle:", font=LARGE_FONT, background="yellow")
        label.grid(row=1, columnspan=10)

        label_brand = ttk.Label(self, text="Brand:", font=MEDIUM_FONT, background="yellow")
        label_brand.grid(row=3, column=3, sticky='E')
        entry_brand = ttk.Entry(self)
        entry_brand.grid(row=3, column=4, sticky='W')
        entry_brand.insert(0, "Brand")
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
                                 command=lambda: popup_msg())
        button_send.grid(row=9, column=4, sticky='E')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(InventoryPage)])
        button_cancel.grid(row=9, column=5, sticky='E')

app = BiciCoopRentalapp()
app.geometry("800x600")
app.resizable(width=False, height=False)
app.mainloop()