from tkinter import *
from tkinter import ttk
from appBackEnd import *
from database import checkData, deleteRecord, displayData

root = Tk()
root.title('SimpleApp')

#width and height of the window
def GUIGeometrics():
   app_width = 400
   app_height = 200

   screen_w = root.winfo_screenwidth()
   screen_h = root.winfo_screenheight()

   x = (screen_w / 2) - (app_width) + 200
   y = (screen_h / 2) - (app_height) + 150

   root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
GUIGeometrics()

#Labels and inputs main window
pwLabel = Label(root,text="Username", font=('Arial', 13))
pwLabel.pack()

username = Entry(root, width=35, borderwidth=1, relief="ridge", font=('Arial', 10), highlightthickness=2)
username.config(highlightbackground='grey', highlightcolor='grey')
username.pack()

usrLabel = Label(root,text="Password", font=('Arial', 13))
usrLabel.pack()

password = Entry(root, width=35, borderwidth=1, relief="ridge", font=('Arial', 10), highlightthickness=2, show='*')
password.config(highlightbackground='grey', highlightcolor='grey')
password.pack()

def login():
   #Check if inputs are empty return error
   if len(username.get()) != 0 and len(password.get()) != 0:
      user = App(username.get(), password.get())
      user.login()
      username.delete(0, 'end')
      password.delete(0, 'end')
   else:
      from tkinter import messagebox as mb
      mb.showerror('Error', 'Invalid input!.')  

def signup():
   if len(username.get()) != 0 and len(password.get()) != 0:
      user = App(username.get(), password.get())
      user.signup()
      username.delete(0, 'end')
      password.delete(0, 'end')
   else:
      from tkinter import messagebox as mb
      mb.showerror('Error', 'Invalid input!.')


def deleteAccHolder():

   usrId = idInput.get()
   username = nameInput.get()
   passw = passInput.get()
   
   if len(usrId) != 0 and len(username) != 0 and len(passw) != 0:
      x = my_tree.selection()[0]
      my_tree.delete(x)

      deleteAccount(usrId, username, passw)
   else:
      mb.showerror('Error', 'You can\'t delete an empty inputs. Please select something!.')

   idInput.delete(0, END)
   nameInput.delete(0, END)
   passInput.delete(0, END)

def updateDataHolder():
   usrId = idInput.get()
   username = nameInput.get()
   passw = passInput.get()
   
   if len(usrId) != 0 and len(username) != 0 and len(passw) != 0:
      selected = my_tree.focus()
      my_tree.item(selected, text='', values=(idInput.get(), nameInput.get(), passInput.get()))

      updateInfo(usrId, username, passw)
   else:
      mb.showerror('Error', 'You can\'t update an empty inputs. Please select something!.')

   idInput.delete(0, END)
   nameInput.delete(0, END)
   passInput.delete(0, END)

def select_record():
   idInput.delete(0, END)
   nameInput.delete(0, END)
   passInput.delete(0, END)

   selected = my_tree.focus()

   values = my_tree.item(selected, 'values')

   try:
      idInput.insert(0, values[0])
      nameInput.insert(0, values[1])
      passInput.insert(0, values[2])
   except IndexError:
      pass

def clicker(e):
   select_record()


def showAllRecords():
   global idInput, nameInput, passInput, my_tree

   newWindow = Toplevel(root)
   newWindow.title('All records')
   newWindow.geometry('500x500')
   fetchedData = displayData()

   treeFrame = Frame(newWindow)
   treeFrame.pack(pady=10,padx=10, fill=BOTH)

   tree_scroll = Scrollbar(treeFrame)
   tree_scroll.pack(side=RIGHT, fill=Y)

   style = ttk.Style()
   style.theme_use("clam")  
   style.configure("Treeview",
      background="white",
      foreground="black",
      rowheight=25,
      fieldbackground="white"
      )


   my_tree = ttk.Treeview(treeFrame, yscrollcommand=tree_scroll.set)
   my_tree.pack(pady=20, fill=BOTH)

   tree_scroll.config(command=my_tree.yview)

   my_tree['columns'] = ("ID", "Name", "Password")

   my_tree.column("#0", width=0, stretch=NO)
   my_tree.column("ID", anchor=CENTER, width=100)
   my_tree.column("Name", anchor=CENTER, width=120)
   my_tree.column("Password", anchor=CENTER, width=120)

   my_tree.heading("#0", text='', anchor=W)
   my_tree.heading("ID", text="ID", anchor=CENTER)
   my_tree.heading("Name", text="Name", anchor=CENTER)
   my_tree.heading("Password", text="Password", anchor=CENTER)


   for x,y,z in fetchedData:
      my_tree.insert(parent='', index='end', text='', values=(x,y,z))


   inputsFrame = Frame(newWindow)
   inputsFrame.pack(anchor=CENTER)

   idLabel = Label(inputsFrame, text='ID')
   idInput = Entry(inputsFrame, width=15, borderwidth=1, relief="ridge", font=('Arial', 10), highlightthickness=2)
   
   nameLabel = Label(inputsFrame, text='Username')
   nameInput = Entry(inputsFrame, width=15, borderwidth=1, relief="ridge", font=('Arial', 10), highlightthickness=2)

   passLabel = Label(inputsFrame, text='Password')
   passInput = Entry(inputsFrame, width=15, borderwidth=1, relief="ridge", font=('Arial', 10), highlightthickness=2)

   idLabel.grid(row=0, column=1)
   idInput.grid(row=1, column=1)
   nameLabel.grid(row=0, column=2, padx=10)
   nameInput.grid(row=1, column=2, padx=10)
   passLabel.grid(row=0, column=3)
   passInput.grid(row=1, column=3)
   
   idInput.config(highlightbackground='grey', highlightcolor='grey')
   nameInput.config(highlightbackground='grey', highlightcolor='grey')
   passInput.config(highlightbackground='grey', highlightcolor='grey')


   deleteButton = Button(newWindow, text='Delete', borderwidth=3, command=deleteAccHolder, background='grey', font=('Arial', 11), relief='ridge', fg='white', width=13)
   deleteButton.pack(pady=15)

   updateButton = Button(newWindow, text='Update username', borderwidth=3, command=updateDataHolder, background='grey', font=('Arial', 11), relief='ridge', fg='white', width=13)
   updateButton.pack(pady=3)

   my_tree.bind("<Double-1>", clicker)
   #newWindow.resizable(False, False)



menubar = Menu(root)
more = Menu(menubar, tearoff=0)
more.add_command(label='Show all records', command=showAllRecords)
menubar.add_cascade(label="More", menu=more)

frame = Frame(root)
frame.pack(pady=10)  

login1 = Button(frame, text="Login", padx=15, pady=1, borderwidth=3, command=login, background='grey', font=('Arial', 11), relief='ridge', fg='white')
login1.pack(side=LEFT, padx=3)
signup1 = Button(frame, text="Signup", padx=14, pady=1, borderwidth=3, command=signup, background='grey', font=('Arial', 11), relief='ridge', fg='white')
signup1.pack(side=LEFT, padx=3)

root.config(menu=menubar)
root.resizable(False, False) 
root.mainloop()