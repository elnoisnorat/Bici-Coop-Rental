# ---------------------------------------------------------------#
# Name:BiciCoop Rental Main
#
# This code containg the GUI for the Workstation Module.
# The inner class containg the diferrent page in the program.
# This classes areLoginPage, ForgotPage, MainPage, ReceivePage,
# ReleasePage, InventoryPage, NewBike and EditBike,MaintenancePage,
# ViewUser, NewPass, RequestPage, ReportPage.
# Inside some classes contain a basic validation method tha validate
# data before send request to the server
#
# Credits: Harrison@pythonprogramming.net,
# https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
# Author: Angel L. Rodriguez Ortolaza
# Revised by: Victor Lugo
# ---------------------------------------------------------------#

import tkinter as tk
from tkinter import ttk, StringVar, font, IntVar, messagebox
# import requests
# from RFID_test import RFID_Handler
# import traceback

# Font setup
LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)

BACK_GROUND = '#F2E68F'

# RFID Setup
# tes = RFID_Handler()
# tes.initRFID()
##test rfid here

# Network setup
# ses = requests.Session()
# link = 'http://e2f00ed0.ngrok.io'


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Alert")
    label = ttk.Label(popup, text=msg, font=MEDIUM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def logout():
    # r = ses.post(link + '/logout')
    # print(r.text)
    print('dummy')


class Worker:
    def __init__(myworker, name, last, email, phone):
        myworker.name = name
        myworker.last = last
        myworker.email = email
        myworker.phone = phone

    def set_worker(myworker, name, last, email, phone):
        myworker.name = name
        myworker.last = last
        myworker.email = email
        myworker.phone = phone

    def set_phone(myworker, phone):
        myworker.phone = phone

    def set_name(myworker, name):
        myworker.name = name

    def get_full_name(myworker):
        return myworker.name + " " + myworker.last

    def get_name(myworker):
        return myworker.name

    def get_last(myworker):
        return myworker.last

    def get_email(myworker):
        return myworker.email

    def get_phone(myworker):
        return myworker.phone


class Bicycle:
    def __init__(mybicycle, brand, model, plate, tag):
        mybicycle.plate = plate
        mybicycle.brand = brand
        mybicycle.model = model
        mybicycle.tag = tag
        mybicycle.service = ""
        mybicycle.worker = ""

    def set_bike(mybicycle, brand, model, plate, tag):
        mybicycle.plate = plate
        mybicycle.brand = brand
        mybicycle.model = model
        mybicycle.tag = tag

    def get_plate(mybicycle):
        return mybicycle.plate

    def get_brand(mybicycle):
        return mybicycle.brand

    def get_model(mybicycle):
        return mybicycle.model

    def get_tag(mybicycle):
        return mybicycle.tag

    def get_service(mybicycle):
        return mybicycle.service

    def set_service(mybicycle, service):
        mybicycle.service = service

    def get_worker(mybicycle):
        return mybicycle.worker

    def set_worker(mybicycle, worker):
        mybicycle.worker = worker


newBicycle = Bicycle("", "", "", "")
newOldBicycle = Bicycle("", "", "", "")
editBicycle = Bicycle("", "", "", "")
editOldBicycle = Bicycle("", "", "", "")
editedBicycle = Bicycle("", "", "", "")
editedOldBicycle = Bicycle("", "", "", "")
mainBicycle = Bicycle("", "", "", "")
mainOldBicycle = Bicycle("", "", "", "")
repairBicycle = Bicycle("", "", "", "")
repairOldBicycle = Bicycle("", "", "", "")
repairedBicycle = Bicycle("", "", "", "")
repairedOldBicycle = Bicycle("", "", "", "")

newWorker = Worker("", "", "", "")
newOldWorker = Worker("", "", "", "")
editWorker = Worker("", "", "", "")
editOldWorker = Worker("", "", "", "")


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

        for F in (
                LoginPage, ForgotPage, MainPage, ReceivePage, ReleasePage, InventoryPage, NewBike, EditBike,
                MaintenancePage, ViewUser, EditUser, NewPass, RequestPage, ReportPage):

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

        def validate(event):  # toserver

            val = str(entry_user.get())
            if val.find('@') == -1 or val.count("@") != 1:
                messagebox.showwarning("Alert", "Invalid Email Format")
                entry_user.focus()
            elif val.find(".") == -1 or len(val) - val.rindex('.') <= 2:
                messagebox.showwarning("Alert", "Invalid Email Format")
                entry_user.focus()
            elif len(str(entry_pass.get())) < 8:
                messagebox.showwarning("Alert", "Invalid Entry")
                entry_pass.focus()
            else:  # send to server
                newWorker.set_worker("Angel", "Rodriguez", entry_user.get(), "7876015466")
                editWorker.set_phone("7876015466")
                clean()
                #loading
                controller.show_frame(MainPage)

                # try:
                #     r = ses.get(link + '/workerLogin', json={"Email": entry_user.get(), "password": entry_pass.get()})
                #     # in tunnel not found????
                #     print(r.text)
                #
                #     if 'Error' in r.json():
                #         mese = r.json()["Error"]
                #         messagebox.showwarning("Alert", mese)
                #     else:
                #         t = r.json()["info"]
                #         newWorker.set_worker(t["Name"], t["Last Name"], t["Email"], t["Phone Number"])
                #         clean()
                #         controller.show_frame(MainPage)
                #
                # except:
                #
                #     traceback.print_exc()

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
        entry_pass.bind('<Return>', validate)
        entry_pass.grid(row=4, column=4, sticky='W')

        button_forgot = tk.Button(self, text="Forgot Password", borderwidth=0, bg=BACK_GROUND,
                                  command=lambda: [clean(), controller.show_frame(ForgotPage)])
        button_forgot.grid(row=5, columnspan=10)
        f = font.Font(button_forgot, button_forgot.cget("font"))
        f.configure(underline=True)
        button_forgot.config(font=f, foreground="blue")

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

        def validate(event):  # toserver

            val = str(entry_b.get())
            if val.find('@') == -1 or val.count("@") != 1:
                messagebox.showwarning("Alert", "  Invalid Email Format  ")
            elif val.find(".") == -1 or val.rindex('.') != len(val) - 4:
                messagebox.showwarning("Alert", "  Invalid Email Format  ")
            else:  # send to server
                # here (entry_b.get())
                messagebox.showinfo("Success", "        Email sent        ")
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

        def new_worker():
            if newWorker.get_email() != newOldWorker.get_email():
                worker.set(newWorker.get_full_name())
                newOldWorker.set_worker(newWorker.get_name(), newWorker.get_last(),
                                        newWorker.get_email(), "")
            self.after(300, new_worker)

        worker = StringVar()
        worker.set("Worker Full Name")
        s = ttk.Style()
        s.map("Big.TButton", background=[('active', '#C8D1E0')])
        s.configure('Big.TButton', font=("Verdana", 10), background='white')

        button_user = ttk.Button(self, textvariable=worker, width=20,
                                 command=lambda: controller.show_frame(ViewUser))
        button_user.grid(row=0, column=1, columnspan=5, sticky='W')

        button1 = ttk.Button(self, text="Logout",
                             command=lambda: [logout(), controller.show_frame(LoginPage)])
        button1.grid(row=0, column=9)

        label = tk.Label(self, text="Home Page", font=LARGE_FONT, background=BACK_GROUND)
        label.grid(row=1, columnspan=10)

        button2 = ttk.Button(self, text="Inventory", padding=20, style="Big.TButton",
                             command=lambda: controller.show_frame(InventoryPage))
        button2.grid(row=3, columnspan=5)
        button1 = ttk.Button(self, text="Maintenance", padding=20, style="Big.TButton",
                             command=lambda: controller.show_frame(MaintenancePage))
        button1.grid(row=6, columnspan=5)
        button3 = ttk.Button(self, text="Receive", padding=20, style="Big.TButton",
                             command=lambda: controller.show_frame(ReceivePage))
        button3.grid(row=3, column=5, columnspan=5)
        button4 = ttk.Button(self, text="Release", padding=20, style="Big.TButton",
                             command=lambda: controller.show_frame(ReleasePage))
        button4.grid(row=6, column=5, columnspan=5)
        self.after(300, new_worker)


class ViewUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def new_worker():
            if newWorker.get_phone() != newOldWorker.get_phone():
                full_name.set(newWorker.get_full_name())
                email.set(newWorker.get_email())
                phone = str(newWorker.get_phone())
                phone_number.set("(" + phone[0:3] + ")" + "-" + phone[3:6] + "-" + phone[6:10])
                newOldWorker.set_phone(newWorker.get_phone())
            self.after(300, new_worker)

        full_name = StringVar()
        email = StringVar()
        phone_number = StringVar()
        full_name.set("Full Name")
        email.set("Email@mail.com")
        phone_number.set("0123456789")

        button_logout = ttk.Button(self, text="Logout",
                                   command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_logout.grid(row=0, column=9)

        label_tittle = ttk.Label(self, text="Worker Profile:", font=LARGE_FONT, background=BACK_GROUND)
        label_tittle.grid(row=1, columnspan=10)

        label_full = ttk.Label(self, text="Full Name:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_full.grid(row=3, columnspan=5)
        label_fulled = tk.Label(self, textvariable=full_name, background=BACK_GROUND, font=SMALL_FONT)
        label_fulled.grid(row=4, columnspan=5, sticky='N')

        label_email = ttk.Label(self, text="Email:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_email.grid(row=3, column=5, columnspan=5)
        label_emailed = tk.Label(self, textvariable=email, background=BACK_GROUND, font=SMALL_FONT)
        label_emailed.grid(row=4, column=5, columnspan=5, sticky='N')

        label_phone = ttk.Label(self, text="Phone Number:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_phone.grid(row=5, columnspan=10)
        label_phoned = tk.Label(self, textvariable=phone_number, background=BACK_GROUND, font=SMALL_FONT)
        label_phoned.grid(row=6, columnspan=10, sticky='N')


        button_scan = ttk.Button(self, text=" Change\nPassword", padding=20,
                                 command=lambda: controller.show_frame(NewPass))
        button_scan.grid(row=7, column=6)

        button_send = ttk.Button(self, text="  Edit\nPhone", padding=20,
                                 command=lambda: controller.show_frame(EditUser))
        button_send.grid(row=7, column=4)
        button_cancel = ttk.Button(self, text="Back",
                                   command=lambda: [controller.show_frame(MainPage)])
        button_cancel.grid(row=9, columnspan=10)
        self.after(300, new_worker)


class EditUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def edit_worker():
            if editWorker.get_phone() != editOldWorker.get_phone():

                entry_phone.delete(0, 'end')
                entry_phone.insert(0, editWorker.get_phone())
                editOldWorker.set_phone(editWorker.get_phone())

            self.after(400, edit_worker)

        def onValidate(S):

            if S.isnumeric():
                return True
            else:
                return False

        str_phone = StringVar()
        def character_limit(str_phone):
            if len(str_phone.get()) > 0:
                str_phone.set(str_phone.get()[:10])
        str_phone.trace("w", lambda *args: character_limit(str_phone))

        def clean():
            str_phone.set(newWorker.get_phone())

        def validate(event):
            if len(str_phone.get()) < 10:
                messagebox.showwarning("Alert", "  Phone number must contain ten digits ")
            else:
                if str_phone.get() == newWorker.get_phone():
                    messagebox.showwarning("Alert", "  No change edits not allowed  ")
                else: #toserver
                    print("Phone Changed")
                    newWorker.set_phone(str_phone.get())
                    newOldWorker.set_worker("", "", "", "")
                    label_phone.focus()
                    controller.show_frame(ViewUser)

        button_logout = ttk.Button(self, text="Logout",
                                   command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_logout.grid(row=0, column=9)

        label_tittle = ttk.Label(self, text="Edit Phone Number:", font=LARGE_FONT, background=BACK_GROUND)
        label_tittle.grid(row=1, columnspan=10)

        # label_full = ttk.Label(self, text="Name:", font=MEDIUM_FONT, background=BACK_GROUND)
        # label_full.grid(row=3, columnspan=5)
        # entry_fulled = tk.Entry(self, font=MEDIUM_FONT, width=13)
        # entry_fulled.grid(row=4, columnspan=5, sticky='N')
        #
        # label_email = ttk.Label(self, text="Last:", font=MEDIUM_FONT, background=BACK_GROUND)
        # label_email.grid(row=3, column=5, columnspan=5)
        # entry_email = tk.Entry(self, font=MEDIUM_FONT, width=13)
        # entry_email.grid(row=4, column=5, columnspan=5, sticky='N')

        label_phone = ttk.Label(self, text="Phone Number:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_phone.grid(row=5, columnspan=5, sticky='NE')
        vcmd = (self.register(onValidate), '%S')
        entry_phone = ttk.Entry(self, font=MEDIUM_FONT, textvariable =str_phone,  width=13,validate = "key", validatecommand=vcmd)
        entry_phone.grid(row=5, column=5, columnspan=5, sticky='NW')
        entry_phone.bind('<Return>', validate)


        button_cancel = ttk.Button(self, text="Edit",
                                   command=lambda: [validate('<FocusIn>')])
        button_cancel.grid(row=9, column=4)

        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(ViewUser)])
        button_cancel.grid(row=9, column=6)
        self.after(400, edit_worker)


class NewPass(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clean():
            entry_old.delete(0, 'end')
            entry_new.delete(0, 'end')
            entry_ret.delete(0, 'end')

        def validate(event):  # toserver
            # 8char len(), alphanumeric isalnum(), mayuscula isupper() y minuscula islower()

            if entry_old.get() == entry_new.get():  # Old and New are the same?
                messagebox.showwarning("Alert", "Same Password not allowed")
                clean()
                entry_old.focus()
            else:
                new = str(entry_new.get())
                ver = ""
                if len(new) <= 7:
                    ver = ver + "Password must contain at least 8 characters\n"
                if any(i.isnumeric() for i in new) is False or any(i.isalpha() for i in new) is False:
                    ver = ver + "Password must contain at least a character and a number\n"
                if any(i.isupper() for i in new) is False or any(i.islower() for i in new) is False:
                    ver = ver + "Password must contain upper and lower characters\n"
                if new != str(entry_ret.get()):
                    ver = ver + "Password need to match"

                if ver == "":
                    print("Bingo")
                    entry_old.focus()
                    clean()
                    controller.show_frame(ViewUser)
                else:
                    messagebox.showwarning("Alert", ver)
                    entry_ret.delete(0, 'end')
                    entry_new.focus()


            # if len(new) >= 8:
            #     if any(i.isnumeric() for i in new) and any(i.isalpha() for i in new):
            #         if any(i.isupper() for i in new) and any(i.islower() for i in new):
            #             if new == str(entry_ret.get()):
            #                 print("Bingo")
            #                 clean()
            #                 controller.show_frame(ViewUser)
            #
            #                 # try:
            #                 #     t = ses.put(link + '/updatePassword', json={"oldPassword": str(entry_old.get()),
            #                 #                                                 "newPassword": str(entry_new.get()),
            #                 #                                                 "confirmPassword": str(entry_ret.get())})
            #                 #     print(t.text)
            #                 #     clean()
            #                 #     controller.show_frame(ViewUser)
            #                 # except:
            #                 #     traceback.print_exc()
            #                 #     clean()
            #
            #
            #             else:
            #                 messagebox.showwarning("Alert", "New and confim dont match")
            #                 clean()
            #
            #         else:
            #             messagebox.showwarning("Alert", "Password must contain upper and lower characters")
            #             clean()
            #
            #
            #     else:
            #         messagebox.showwarning("Alert", "Password must contain a character and a number")
            #         clean()
            #
            # else:
            #     messagebox.showwarning("Alert", "Password must contain at least 8 characters")
            #     clean()

        button_logout = ttk.Button(self, text="Logout",
                                   command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_logout.grid(row=0, column=9)

        label_reset = ttk.Label(self, text="Reset Password:", font=LARGE_FONT, background=BACK_GROUND)
        label_reset.grid(row=1, columnspan=10)

        label_old = ttk.Label(self, text="Current Password:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_old.grid(row=3, columnspan=5, sticky='E')
        entry_old = ttk.Entry(self, show='*', width=30)
        entry_old.grid(row=3, column=5, columnspan=4, sticky='W')

        label_new = ttk.Label(self, text="New Password:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_new.grid(row=5, columnspan=5, sticky='E')
        entry_new = ttk.Entry(self, show='*', width=30)
        entry_new.grid(row=5, column=5, columnspan=4, sticky='W')

        label_ret = ttk.Label(self, text="Confirm Password:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_ret.grid(row=6, columnspan=5, sticky='E')
        entry_ret = ttk.Entry(self, show='*', width=30)
        entry_ret.grid(row=6, column=5, columnspan=4, sticky='W')
        entry_ret.bind('<Return>', validate)

        button_send = ttk.Button(self, text="Change", command=lambda: validate('<FocusIn>'))
        button_send.grid(row=9, column=4, sticky='E')

        button_back = ttk.Button(self, text="Cancel", command=lambda: [controller.show_frame(ViewUser)])
        button_back.grid(row=9, column=6, sticky='E')


class ReceivePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tries = IntVar()
        tag.set("RFID TAG")
        tries.set(0)
        rootFrame = tk.Frame(self, bg=BACK_GROUND)
        rootFrame.pack(side='top', fill='both', pady=10, padx=31)
        topFrame = tk.Frame(self, bg=BACK_GROUND)
        topFrame.pack(side='top', fill='both', pady=10)
        miduFrame = tk.Frame(self, bg=BACK_GROUND, pady=30)
        miduFrame.pack(fill='both')
        middFrame = tk.Frame(self, bg=BACK_GROUND)
        middFrame.pack(fill='both', pady=30)
        lowFrame = tk.Frame(self, bg=BACK_GROUND)
        lowFrame.pack(side='bottom')

        def identify():

            if tries.get() == 4:
                entry_con.lift()
            else:
                cmp = str(tes.single_read())
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

        def validate():

            if entry_con.get() == "Insert Plate" and (tag.get() == "RFID TAG" or tag.get().startswith("Verify")):
                messagebox.showwarning("Alert", "Identify a Bicicle")
            else:  # send to server
                clean()
                controller.show_frame(MainPage)

        button_log = ttk.Button(rootFrame, text="Logout",
                                command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_log.pack(side='right')

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
                                 command=lambda: [validate()])
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

            cmp = str(tes.single_read())
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

        def repopulate_defaults(event):

            if entry_con != self.focus_get() and entry_con.get() == "":
                entry_con.insert(0, "Confirmation Code")

        def clean():
            entry_con.delete(0, 'end')
            entry_con.insert(0, "Confirmation Code")
            tag.set("RFID TAG")
            tries.set(0)

        def validate():
            if entry_con.get() == "Confirmation Code":
                messagebox.showwarning("Alert", "Insert Confirmation Code")
            elif tag.get() == "RFID TAG" or tag.get().startswith("Verify"):
                messagebox.showwarning("Alert", "Identify a Bicicle")
            else:
                # to server.....
                clean()
                controller.show_frame(MainPage)

        button_logout = ttk.Button(self, text="Logout",
                                   command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_logout.grid(row=0, column=9)

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
        button_send.grid(row=9, column=1, columnspan=4, sticky='NE')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MainPage)])
        button_cancel.grid(row=9, columnspan=5, column=6, sticky='NW')


class InventoryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        val = StringVar()

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
            try:
                val.set(tree.selection()[0])
                button2.configure(state='enable')
            except:
                children = tree.get_children()
                try:
                    child = children[0]
                    tree.selection_set(child)
                    button2.configure(state='enable')
                except:
                    button2.configure(state='disable')

        def disable():
            tree.selection_remove(tree.focus())
            button2.configure(state='disable')

        def populate():
            val.set(tree.selection()[0])
            editBicycle.set_bike(tree.item(val.get())['values'][0], tree.item(val.get())['values'][1],
                                 tree.item(val.get())['text'], tree.item(val.get())['values'][2])
            controller.show_frame(EditBike)

        def new_one():
            if newBicycle.get_plate() != newOldBicycle.get_plate():
                tree.insert('', tk.END, text=newBicycle.get_plate(),
                            values=(newBicycle.get_brand(), newBicycle.get_model(), newBicycle.get_tag()))
                newOldBicycle.set_bike(newBicycle.get_brand(), newBicycle.get_model(),
                                       newBicycle.get_plate(), newBicycle.get_tag())

            self.after(100, new_one)

        def edit_one():
            if editedBicycle.get_plate() != editedOldBicycle.get_plate() or \
                    editedBicycle.get_brand() != editedOldBicycle.get_brand() or \
                    editedBicycle.get_model() != editedOldBicycle.get_model() or \
                    editedBicycle.get_tag() != editedOldBicycle.get_tag():
                tree.item(val.get(), text=editedBicycle.get_plate(),
                          values=(editedBicycle.get_brand(), editedBicycle.get_model(), editedBicycle.get_tag()))
                editedOldBicycle.set_bike(editedBicycle.get_brand(), editedBicycle.get_model(),
                                          editedBicycle.get_plate(), editedBicycle.get_tag())

            self.after(100, edit_one)

        def main_one():
            if mainBicycle.get_plate() != mainOldBicycle.get_plate() or \
                    mainBicycle.get_tag() != mainOldBicycle.get_tag():
                if search_plate(str(mainBicycle.get_plate())) == None and \
                        search_tag(str(mainBicycle.get_tag())) == None:
                    print('None search')
                    mainBicycle.set_bike("None", "", mainBicycle.get_plate(), mainBicycle.get_tag())
                    mainOldBicycle.set_bike("None", "", mainBicycle.get_plate(), mainBicycle.get_tag())
                else:
                    print('Find search')
                    mainBicycle.set_bike(tree.item(val.get())['values'][0], tree.item(val.get())['values'][1],
                                         tree.item(val.get())['text'], tree.item(val.get())['values'][2])
                    mainOldBicycle.set_bike(tree.item(val.get())['values'][0], tree.item(val.get())['values'][1],
                                            tree.item(val.get())['text'], tree.item(val.get())['values'][2])
                    tree.delete(val.get())

            self.after(10, main_one)

        def rep_one():
            if repairedBicycle.get_plate() != repairedOldBicycle.get_plate():
                tree.insert('', tk.END, text=repairedBicycle.get_plate(),
                            values=(
                            repairedBicycle.get_brand(), repairedBicycle.get_model(), repairedBicycle.get_tag()))
                # to server bike available
                repairedBicycle.set_bike("", "", "", "")
                repairedBicycle.set_service("")
                repairedBicycle.set_worker("")

            self.after(100, rep_one)

        def search_plate(find, item=''):
            children = tree.get_children(item)
            for child in children:
                text = tree.item(child, 'text')
                if text == find:
                    tree.selection_set(child)
                    tree.see(child)
                    posi = tree.selection()[0]
                    val.set(posi)
                    return True
                else:
                    res = search_plate(find, child)
                    if res:
                        return True

        def search_tag(find, item=''):
            children = tree.get_children(item)
            for child in children:
                value = tree.item(child, 'values')
                if value[2].lower() == find.lower():
                    tree.selection_set(child)
                    tree.see(child)
                    posi = tree.selection()[0]
                    val.set(posi)
                    return True
                else:
                    res = search_tag(find, child)
                    if res:
                        return True

        label = tk.Label(topFrame, text="Inventory", font=LARGE_FONT, bg=BACK_GROUND)
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

        tree.insert('', tk.END, text="7949", values=("OFO", "YELLOW", "045CA0703A6C5E8189"))

        tree.pack(side='left', fill='both')
        scrollbar = ttk.Scrollbar(midFrame, orient="vertical", command=tree.yview)
        scrollbar.place(x=584, y=0, height=210)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind('<FocusIn>', active)

        button1 = ttk.Button(self, text="New", width=10, padding=15,
                             command=lambda: [disable(), controller.show_frame(NewBike)])
        button1.pack(side='left', padx=90)
        button2 = ttk.Button(self, text="Edit", width=10, padding=15, state='disable',
                             command=lambda: [populate(), disable()])
        button2.pack(side='right', padx=90)

        button_back = ttk.Button(lowFrame, text="Back", width=10,
                                 command=lambda: [disable(), controller.show_frame(MainPage)])
        button_back.pack()

        # button_find = ttk.Button(lowFrame, text="FIND", width=10,
        #                          command=lambda: print(search_tag("045CA0703A6C5E8189")))
        # button_find.pack()
        self.after(500, new_one)
        self.after(500, edit_one)
        self.after(10, main_one)
        self.after(200, rep_one)


class NewBike(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tries = IntVar()
        tag.set("RFID TAG")
        tries.set(0)

        def identify():

            cmp = str(tes.single_read())
            if cmp == "Verify and try again":
                tries.set(tries.get() + 1)
                tag.set(cmp + " (" + str(tries.get()) + ")")
            elif len(cmp) == 21:
                tries.set(0)
                tag.set(cmp[2:20])
            else:
                tag.set("NPI")

        def clear_widget(event):

            if entry_brand == self.focus_get() and entry_brand.get() == "Brand":
                entry_brand.delete(0, 'end')
            elif entry_model == self.focus_get() and entry_model.get() == "Model":
                entry_model.delete(0, 'end')
            elif entry_plate == self.focus_get() and entry_plate.get() == "Plate":
                entry_plate.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_brand != self.focus_get() and entry_brand.get() == "":
                entry_brand.insert(0, "Brand")
            elif entry_model != self.focus_get() and entry_model.get() == "":
                entry_model.insert(0, "Model")
            elif entry_plate != self.focus_get() and entry_plate.get() == "":
                entry_plate.insert(0, "Plate")

        def clean():
            entry_brand.delete(0, 'end')
            entry_brand.insert(0, "Brand")
            entry_model.delete(0, 'end')
            entry_model.insert(0, "Model")
            entry_plate.delete(0, 'end')
            entry_plate.insert(0, "Plate")
            tag.set("RFID TAG")

        def validate():

            if entry_brand.get() == "Brand":
                messagebox.showwarning("Alert", "Insert Brand")
            elif entry_model.get() == "Model":
                messagebox.showwarning("Alert", "Insert Model")
            elif entry_plate.get() == "Plate":
                messagebox.showwarning("Alert", "Insert Plate")
            elif tag.get() == "RFID TAG" or tag.get().startswith("Verify"):
                messagebox.showwarning("Alert", "Identify a Bicicle")
            else:  # Send to server
                anw = messagebox.askokcancel("Confirm entries", entry_brand.get() + " " + entry_model.get()
                                             + " " + entry_plate.get() + "\n" + tag.get())
                if anw == True:  # To server
                    clean()
                    controller.show_frame(InventoryPage)

                    # try:
                    #     r = ses.post(link + '/bicycle', json={"lp": str(entry_plate.get()), "rfid": str(tag.get()),
                    #                                           "model": str(entry_model.get()),
                    #                                           "brand": entry_brand.get()})
                    #     newBicycle.set_bike(entry_brand.get(), entry_model.get(), entry_plate.get(), tag.get())
                    #     clean()
                    #     controller.show_frame(InventoryPage)
                    #
                    # except:
                    #     traceback.print_exc()

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

        button_scan = ttk.Button(self, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.grid(row=6, columnspan=10, sticky='S')

        label2 = tk.Label(self, textvariable=tag, background=BACK_GROUND)
        label2.grid(row=7, columnspan=10, sticky='N')

        button_send = ttk.Button(self, text="Add",
                                 command=lambda: validate())
        button_send.grid(row=9, column=4, sticky='E')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(InventoryPage)])
        button_cancel.grid(row=9, column=5, sticky='E')


class EditBike(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tries = IntVar()
        tag.set("RFID TAG")
        tries.set(0)

        def identify():

            cmp = str(tes.single_read())
            if cmp == "Verify and try again":
                tries.set(tries.get() + 1)
                tag.set(cmp + " (" + str(tries.get()) + ")")
            elif len(cmp) == 21:
                tries.set(0)
                tag.set(cmp[2:20])
            else:
                tag.set("NPI")

        def validate():
            if entry_brand.get() != editBicycle.get_brand() or entry_model.get() != editBicycle.get_model() or \
                    entry_plate.get() != editBicycle.get_plate() or tag.get() != editBicycle.get_tag():

                if tag.get().startswith("Verify"):
                    messagebox.showwarning("Alert", "Identify a Bicicle")
                else:
                    editedBicycle.set_bike(entry_brand.get(), entry_model.get(), entry_plate.get(), tag.get())
                    controller.show_frame(InventoryPage)

            else:
                controller.show_frame(InventoryPage)

        def update_label():

            if editBicycle.get_plate() != editOldBicycle.get_plate():
                entry_brand.delete(0, 'end')
                entry_model.delete(0, 'end')
                entry_plate.delete(0, 'end')
                entry_brand.insert(0, editBicycle.get_brand())
                entry_plate.insert(0, editBicycle.get_plate())
                entry_model.insert(0, editBicycle.get_model())
                tag.set(editBicycle.get_tag())
                editOldBicycle.set_bike(editBicycle.get_brand(), editBicycle.get_model(),
                                        editBicycle.get_plate(), editBicycle.get_tag())

            self.after(100, update_label)

        def back():
            entry_brand.delete(0, 'end')
            entry_model.delete(0, 'end')
            entry_plate.delete(0, 'end')
            entry_brand.insert(0, editBicycle.get_brand())
            entry_model.insert(0, editBicycle.get_model())
            entry_plate.insert(0, editBicycle.get_plate())
            tag.set(editBicycle.get_tag())

        label = ttk.Label(self, text="Edit Bicycle:", font=LARGE_FONT, background=BACK_GROUND)
        label.grid(row=1, columnspan=10)

        label_brand = ttk.Label(self, text="Brand:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_brand.grid(row=3, column=3, sticky='E')
        entry_brand = ttk.Entry(self)
        entry_brand.grid(row=3, column=4, sticky='W')
        entry_brand.insert(0, "Brand")

        label_model = ttk.Label(self, text="Model:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_model.grid(row=3, column=5, sticky='E')
        entry_model = ttk.Entry(self)
        entry_model.grid(row=3, column=6, sticky='W')
        entry_model.insert(0, "Model")

        label_plate = ttk.Label(self, text="Plate:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_plate.grid(row=4, column=4, sticky='E')
        entry_plate = ttk.Entry(self)
        entry_plate.grid(row=4, column=5, sticky='W')
        entry_plate.insert(0, "Plate")

        button_scan = ttk.Button(self, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.grid(row=6, columnspan=10, sticky='S')

        label2 = tk.Label(self, textvariable=tag, background=BACK_GROUND)
        label2.grid(row=7, columnspan=10, sticky='N')

        button_send = ttk.Button(self, text="Save",
                                 command=lambda: validate())
        button_send.grid(row=9, column=4, sticky='E')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [back(), controller.show_frame(InventoryPage)])
        button_cancel.grid(row=9, column=5, sticky='E')
        self.after(500, update_label)


class MaintenancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        val = StringVar()

        rootFrame = tk.Frame(self, bg=BACK_GROUND)
        rootFrame.pack(side='top', fill='both', pady=10, padx=31)
        topFrame = tk.Frame(self, bg="red")
        topFrame.pack(pady=5)
        midrFrame = tk.Frame(self, bg="brown")
        midrFrame.pack(side='right', padx=50)
        midlFrame = tk.Frame(self, bg="purple")
        midlFrame.pack(side='left', padx=50)
        midFrame = tk.Frame(self, bg="green")
        midFrame.pack()
        lowFrame = tk.Frame(self, bg="orange")
        lowFrame.pack(side='bottom', pady=10)

        def active(event):
            try:
                val.set(tree.selection()[0])
                button2.configure(state='enable')
            except:
                children = tree.get_children()
                try:
                    child = children[0]
                    tree.selection_set(child)
                    button2.configure(state='enable')
                except:
                    button2.configure(state='disable')

        def disable():
            tree.selection_remove(tree.focus())
            button2.configure(state='disable')

        def populate():
            val.set(tree.selection()[0])
            repairBicycle.set_bike(tree.item(val.get())['values'][0], tree.item(val.get())['values'][1],
                                   tree.item(val.get())['text'], tree.item(val.get())['values'][3])
            repairBicycle.set_service(tree.item(val.get())['values'][2])
            repairOldBicycle.set_service(repairBicycle.get_service())
            controller.show_frame(ReportPage)

        def new_one():

            if mainBicycle.get_service() != mainOldBicycle.get_service():

                if mainBicycle.get_brand() == "None":
                    if search_plate(str(mainBicycle.get_plate())) == None and \
                            search_tag(str(mainBicycle.get_tag())) == None:
                        print('None found')
                        messagebox.showwarning("Alert", "Bike not found")
                        mainBicycle.set_bike("", "", "", "")
                        mainOldBicycle.set_bike("", "", "", "")
                        mainBicycle.set_service("")
                    else:
                        print('Find found')
                        tree.insert('', tk.END, text=str(tree.item(val.get())['text']),
                                    values=(tree.item(val.get())['values'][0], tree.item(val.get())['values'][1],
                                            mainBicycle.get_service(), tree.item(val.get())['values'][3]))
                        mainBicycle.set_service("")
                        mainBicycle.set_bike("", "", "", "")
                        mainOldBicycle.set_bike("", "", "", "")

                else:
                    if mainBicycle.get_brand() == "":
                        messagebox.showwarning("Alert", "Bike error")
                        mainBicycle.set_service("")
                        mainBicycle.set_bike("", "", "", "")
                        mainOldBicycle.set_bike("", "", "", "")
                    else:
                        tree.insert('', tk.END, text=str(mainBicycle.get_plate()),
                                    values=(mainBicycle.get_brand(), mainBicycle.get_model(), mainBicycle.get_service(),
                                            mainBicycle.get_tag()))
                        mainBicycle.set_service("")
                        mainBicycle.set_bike("", "", "", "")
                        mainOldBicycle.set_bike("", "", "", "")
            self.after(100, new_one)

        def rep_one():
            if repairBicycle.get_service() != repairOldBicycle.get_service():
                ####################
                plate = repairBicycle.get_plate()
                tree.delete(val.get())

                if search_plate(str(plate)) is True:
                    # send to server service done more service required
                    repairBicycle.set_bike("", "", "", "")
                    repairOldBicycle.set_bike("", "", "", "")
                    repairBicycle.set_service("")
                else:
                    # service done to available invetory
                    repairedBicycle.set_bike(repairBicycle.get_brand(), repairBicycle.get_model(),
                                             repairBicycle.get_plate(), repairBicycle.get_tag())
                    repairedBicycle.set_service(repairBicycle.get_service())
                    repairedBicycle.set_worker(repairBicycle.get_worker())
                    repairBicycle.set_bike("", "", "", "")
                    repairOldBicycle.set_bike("", "", "", "")
                    repairBicycle.set_service("")

            self.after(100, rep_one)

        def search_plate(find, item=''):
            children = tree.get_children(item)
            for child in children:
                text = tree.item(child, 'text')
                if text == find:
                    tree.selection_set(child)
                    tree.see(child)
                    posi = tree.selection()[0]
                    val.set(posi)
                    return True
                else:
                    res = search_plate(find, child)
                    if res:
                        return True

        def search_tag(find, item=''):
            children = tree.get_children(item)
            for child in children:
                value = tree.item(child, 'values')
                if value[3].lower() == find.lower():
                    tree.selection_set(child)
                    tree.see(child)
                    posi = tree.selection()[0]
                    val.set(posi)
                    return True
                else:
                    res = search_tag(find, child)
                    if res:
                        return True

        button_log = ttk.Button(rootFrame, text="Logout",
                                command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_log.pack(side='right')

        label = tk.Label(topFrame, text="Maintenance", font=LARGE_FONT, bg=BACK_GROUND)
        label.pack()

        label_aval = tk.Label(midFrame, text="Service Request", font=SMALL_FONT)
        label_aval.pack(side='top', fill='both')

        tree = ttk.Treeview(midFrame, columns=('Plate', 'Brand', 'Model', 'Service', 'tag'), height=7,
                            selectmode='browse')
        tree.heading('#0', text='Plate')
        tree.heading('#1', text='Brand')
        tree.heading('#2', text='Model')
        tree.heading('#3', text='Service')
        tree.heading('#4', text='Tag')

        tree.column('#0', stretch=tk.NO, width=80)
        tree.column('#1', stretch=tk.NO, width=135)
        tree.column('#2', stretch=tk.NO, width=135)
        tree.column('#3', stretch=tk.NO, width=235)
        tree.column('#4', stretch=tk.NO, width=235)

        # for line in range(5):
        #     tree.insert('', tk.END, text="Plate", values=("Model", "Brand", "Service"))
        # tree.insert('', tk.END, text="1234", values=("OFO", "Yellow", "Cleanup","123456789"))

        tree.pack(side='left', fill='both')
        scrollbar = ttk.Scrollbar(midFrame, orient="vertical", command=tree.yview)
        scrollbar.place(x=584, y=0, height=210)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind('<FocusIn>', active)
        # tree.delete(*tree.get_children())

        button1 = ttk.Button(self, text="Request", width=10, padding=15,
                             command=lambda: [disable(), controller.show_frame(RequestPage)])
        button1.pack(side='left', padx=90)
        button2 = ttk.Button(self, text="Report", width=10, padding=15, state='disable',
                             command=lambda: [populate(), disable()])
        button2.pack(side='right', padx=90)

        button_back = ttk.Button(lowFrame, text="Back", width=10,
                                 command=lambda: [disable(), controller.show_frame(MainPage)])
        button_back.pack()

        # button_find = ttk.Button(lowFrame, text="FIND", width=10,
        #                          command=lambda: print(search_plate("7949")))
        # button_find.pack()

        self.after(100, new_one)
        self.after(200, rep_one)


class RequestPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tag = StringVar()
        tag.set("RFID TAG")

        rootFrame = tk.Frame(self, bg=BACK_GROUND)
        rootFrame.pack(side='top', fill='both', pady=10, padx=31)
        topFrame = tk.Frame(self, bg="red")
        topFrame.pack(pady=5)
        miduFrame = tk.Frame(self, bg=BACK_GROUND)
        miduFrame.pack(fill='both', pady=10)
        middFrame = tk.Frame(self, bg=BACK_GROUND)
        middFrame.pack()
        midlFrame = tk.Frame(self, bg=BACK_GROUND)
        midlFrame.pack(fill='both')
        lowFrame = tk.Frame(self, bg=BACK_GROUND)
        lowFrame.pack(side='bottom')

        def identify():
            cmp = str(tes.single_read())
            if cmp == "Verify and try again":
                tag.set(cmp)
            elif len(cmp) == 21:
                tag.set(cmp[2:20])
            else:
                tag.set("NPI")

        def clear_widget(event):

            if entry_pla == self.focus_get() and entry_pla.get() == "Plate":
                entry_pla.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_pla != self.focus_get() and entry_pla.get() == "":
                entry_pla.insert(0, "Plate")

        def clean():
            service_chosen.set('')
            service_chosen.current(0)
            tag.set("RFID TAG")
            entry_pla.delete(0, 'end')
            entry_pla.insert(0, "Plate")

        def validate(event):

            if service_chosen.get() == "Choose One":
                messagebox.showwarning("Alert", "Choose a service")
            elif (tag.get() == "RFID TAG" or tag.get() == "Verify and try again") and entry_pla.get() == "Plate":
                messagebox.showwarning("Alert", "Identify a Bicycle")
            else:
                mainBicycle.set_bike("", "", entry_pla.get(), tag.get())
                mainBicycle.set_service(service_chosen.get())
                clean()
                controller.show_frame(MaintenancePage)

        button_log = ttk.Button(rootFrame, text="Logout",
                                command=lambda: [logout(), controller.show_frame(LoginPage)])
        button_log.pack(side='right')

        label = ttk.Label(topFrame, text="Request Maintenance", font=LARGE_FONT, background=BACK_GROUND)
        label.pack(side='top')

        ttk.Label(miduFrame, text="Choose a service:", font=MEDIUM_FONT, background=BACK_GROUND).pack()
        service_chosen = ttk.Combobox(miduFrame, width=20, font=SMALL_FONT, state='readonly')
        service_chosen['values'] = ('Choose One', 'Cleanup', 'Tuneup', 'Flat Tire',
                                    'Break adjustment', 'Maneuver adjustment', 'Pedal adjustment',
                                    'Transmission Adjustment', 'New Tire', 'New Break', "New Tag",
                                    'Request Decommission')
        service_chosen.current(0)
        service_chosen.pack()

        label3 = tk.Label(miduFrame, text="Scan or insert plate.", background=BACK_GROUND, font=MEDIUM_FONT, width=30)
        label3.pack(pady=20)

        button_scan = ttk.Button(middFrame, text="Scan", padding=20,
                                 command=lambda: identify())
        button_scan.pack(side='left', padx=100)
        label2 = tk.Label(midlFrame, textvariable=tag, background=BACK_GROUND, font=SMALL_FONT, width=20)
        label2.pack(side='left', padx=165)
        entry_pla = tk.Entry(middFrame, font=MEDIUM_FONT, width=10)
        entry_pla.pack(side='left', padx=100)
        entry_pla.insert(0, "Plate")
        entry_pla.bind('<FocusIn>', clear_widget)
        entry_pla.bind('<FocusOut>', repopulate_defaults)
        entry_pla.bind('<Return>', validate)

        button_send = ttk.Button(lowFrame, text="Send",
                                 command=lambda: [validate('<FocusIn>')])
        button_send.pack(side='left', padx=55, )
        button_cancel = ttk.Button(lowFrame, text="Cancel",
                                   command=lambda: [clean(), controller.show_frame(MaintenancePage)])
        button_cancel.pack(side='left', padx=55, pady=20)


class ReportPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        pla = StringVar()
        ser = StringVar()

        def clear_widget(event):

            if entry_worker == self.focus_get() and entry_worker.get() == "Worker":
                entry_worker.delete(0, 'end')

        def repopulate_defaults(event):

            if entry_worker != self.focus_get() and entry_worker.get() == "":
                entry_worker.insert(0, "Worker")

        def clean():
            txt.delete(1.0, 'end')
            entry_worker.delete(0, 'end')
            entry_worker.insert(0, "Worker")

        def validate(event):
            if entry_worker.get() == "Worker":
                messagebox.showwarning("Alert", "Insert Worker")
            else:
                ##################################
                repairBicycle.set_worker(entry_worker.get())
                repairOldBicycle.set_service("")
                clean()
                controller.show_frame(MaintenancePage)

        def update_label():

            if repairBicycle.get_plate() != repairOldBicycle.get_plate():
                pla.set(repairBicycle.get_plate())
                ser.set(repairBicycle.get_service())
                repairOldBicycle.set_bike(repairBicycle.get_brand(), repairBicycle.get_model(),
                                          repairBicycle.get_plate(), repairBicycle.get_tag())

            self.after(100, update_label)

        def back():
            repairBicycle.set_bike("", "", "", "")
            repairOldBicycle.set_bike("", "", "", "")
            repairBicycle.set_service("")
            repairOldBicycle.set_service("")

        label = ttk.Label(self, text="Completion Service Report:", font=LARGE_FONT, background=BACK_GROUND)
        label.grid(row=1, columnspan=10)

        label_plate = ttk.Label(self, text="Plate:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_plate.grid(row=2, column=0, columnspan=6, sticky='S')
        label_plate2 = tk.Label(self, textvariable=pla, font=SMALL_FONT, background=BACK_GROUND)
        label_plate2.grid(row=3, column=0, columnspan=6, sticky='N')

        label_service = ttk.Label(self, text="Service required:", font=MEDIUM_FONT, background=BACK_GROUND)
        label_service.grid(row=2, column=4, columnspan=5, sticky='S')
        label_service2 = tk.Label(self, textvariable=ser, font=SMALL_FONT, background=BACK_GROUND)
        label_service2.grid(row=3, column=4, columnspan=5, sticky='N')

        txt = tk.Text(self, height=5, width=36)
        txt.grid(row=4, columnspan=10, rowspan=4, sticky='N')

        label_worker = ttk.Label(self, text="Service given by: ", font=MEDIUM_FONT, background=BACK_GROUND)
        label_worker.grid(row=7, columnspan=5, sticky='NE')
        entry_worker = ttk.Entry(self, width=17)
        entry_worker.grid(row=7, column=5, columnspan=5, sticky='NW')
        entry_worker.insert(0, "Worker")
        entry_worker.bind('<FocusIn>', clear_widget)
        entry_worker.bind('<FocusOut>', repopulate_defaults)
        entry_worker.bind('<Return>', validate)

        button_send = ttk.Button(self, text="Report",
                                 command=lambda: [validate('<FocusIn>')])
        button_send.grid(row=9, column=4, sticky='N')
        button_cancel = ttk.Button(self, text="Cancel",
                                   command=lambda: [clean(), back(), controller.show_frame(MaintenancePage)])
        button_cancel.grid(row=9, column=5, sticky='N')

        self.after(100, update_label)


app = BiciCoopRentalapp()
app.geometry("800x400")
app.resizable(width=False, height=False)

app.mainloop()