from tkinter import *
import requests
root = Tk()

def Login():
    payload = {'email': 'bicicoop@email.com', 'password': 'bicicoop'}
    print('Entering...')
    # payload = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiV29ya2VyIiwid0lEIjpbMl0sImV4cCI6MTU1MzcyMjQ3M30.OnezL0RKvf15vzVBUlVqjg472ukjxzDpGVz4bUr2xx8"}
    t = requests.get('http://127.0.0.1:5000/workerLogin', json=payload)
    print(t.text)
    r = requests.get('http://localhost:5000/home', json=t.text)
    return print(r.text)

    #print("Approved!")

label_1 = Label(root, text = "Name:")
label_2 = Label(root, text = "Password:")
entry_1 = Entry(root)
entry_2 = Entry(root)

label_1.grid(row=0,sticky=E)
label_2.grid(row=1,sticky=E)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

button_1 = Button(root, text = "Login", command = Login)
button_1.grid(columnspan=2)

c=Checkbutton(root,text="Keep me logged in")
c.grid(columnspan=2)


root.mainloop()