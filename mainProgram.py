import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sv_ttk
import os
import sys
import mysql.connector
import ignore
import pandas as pd
import sqlalchemy
import phonenumbers
import hashlib
import re

PASSWORD = ignore.password

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=PASSWORD
    )
connection = sqlalchemy.create_engine(f'mysql+mysqlconnector://root:{PASSWORD}@localhost:3306')
#establish a cursor to interact with the database
mycursor = mydb.cursor(buffered=True)
#create the database if it doesnt exists
mycursor.execute("CREATE DATABASE IF NOT EXISTS COURSEWORK;")
mycursor.execute("USE COURSEWORK;")
mycursor.execute("CREATE TABLE IF NOT EXISTS userCredentials(username varchar(255) NOT NULL, password varchar(255) NOT NULL, PRIMARY KEY(username));")
mydb.commit()
#execute to use the database 
global userID
userID = ""
loggedIn = False

class app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)  
        container = ttk.Frame(self, relief="sunken")  
        container.pack(fill="both", expand = True)  
        self.frames = {}  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (menu, logIn, signUpMenu, importCSVPage, mainMenu, searchMenu, deleteExplanationMenu, alterationExplanation,finalAlterationRecord, alterationRecord, deletionRecord, alterationRecord, additionRecord, toolMenu):  
  
            frame = F(container, self)  
  
            self.frames[F] = frame  
  
            frame.grid(row=0, column=0, sticky="nsew")  
  
        self.show_frame(menu)  
  
    def show_frame(self, cont):  
  
        frame = self.frames[cont]  
        frame.tkraise()  
        

class menu(ttk.Frame):
    
    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self,parent,)
        sv_ttk.set_theme("dark")
        style = ttk.Style()
        style.configure("TButton", width= 20,font=(None, 20))
        label = ttk.Label(self, text="Welcome to the CSV Navi!", font=("Helvetica", 40))
        label.pack(expand=True, pady=100)
        
        button = ttk.Button(self, text="Log In", command=lambda: controller.show_frame(logIn))
        button.pack(side="left",expand=True,ipadx= 100, ipady=100)
        
        button2 = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(signUpMenu),)
        button2.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
        
        backwardButton = ttk.Button(self, text="Quit", command=lambda: sys.exit())
        backwardButton.place(relx=0.05, rely=0.05)
        
        
class frontPageTemplate(ttk.Frame):
    
    def __init__(self, parent, controller):
        
        
        ttk.Frame.__init__(self, parent)
        
        self.createLabel()
        
        self.inputtedUsername = tk.StringVar()
        self.inputtedPassword = tk.StringVar()
        
        self.inputtedUsername.trace_add('write', self.statusButton)
        self.inputtedPassword.trace_add('write', self.statusButton)
        
        self.label1 = ttk.Label(self, text="Username:", font=("none, 26"))
        self.label2 = ttk.Label(self, text="Password:", font=("none, 26"))
        
        self.usernameEntry = ttk.Entry(self, textvariable=self.inputtedUsername, font=("none, 24"))
        self.passwordEntry = ttk.Entry(self, textvariable=self.inputtedPassword, font=("none, 24"), show="*")
        
        self.label1.pack(side="top", expand=True, pady=10)
        self.usernameEntry.pack(side="top", expand=True, pady=10)
        
        self.label2.pack(side="top", expand=True, pady=10)
        self.passwordEntry.pack(side="top", expand=True, pady=10)
        self.explanationText()
        self.backwardButton = ttk.Button(self, text="Go Back", command=lambda: [self.clear_text(), controller.show_frame(menu)])
        self.backwardButton.place(relx=0.05, rely=0.05)
        
        self.submitButton = ttk.Button(self, text="Submit", state='disabled', command=lambda: [self.submit(), self.clear_text()])
        self.submitButton.pack(side="top", pady= 50,expand=True, ipadx= 60, ipady=50)
        self.style = ttk.Style(self)
        self.style.configure('TButton', width=15)
        
    def statusButton(self,*args):
    
      if(len(self.inputtedUsername.get()) ) > 0 and len(self.inputtedPassword.get()) > 0:
        self.submitButton.configure(state='normal')
      else:
        self.submitButton.configure(state='disabled')
        
    def clear_text(self):
      
      self.usernameEntry.delete(0, 'end')
      self.passwordEntry.delete(0,'end')
      
      
    def createLabel(self):
              
      pass
    
    def explanationText(self):
      
      pass
    
    def submit(self):
      
      pass
    
    
class signUpMenu(frontPageTemplate):
    
    def __init__(self, parent, controller):
      super().__init__(parent, controller)
      
      
    def createLabel(self):
      
      self.label = ttk.Label(self, text="Sign Up / Create user", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
      
    def explanationText(self):
      
      self.explanationLabel = ttk.Label(self, text="1. Username can only contain english\n    and numeric characters\n    Also not case-sensitve.\n2. Password must contain english characters, \n    numeric characters and special characters.", font=("none, 14"))
      self.explanationLabel.pack(side="top", expand=True, pady=10)
      
    def submit(self):
      
      username = self.usernameEntry.get()
      password = self.passwordEntry.get()

      if username.isalnum() == False:
        messagebox.showerror("Error", "Username can only contain english and numeric characters.")
        return
        
      sql = f"SELECT username FROM usercredentials WHERE username = '{username}'" 
      mycursor.execute(sql)
      data = mycursor.fetchall()
      
      if data:
        messagebox.showerror("Error", "Username has been taken, oops :D")
        return
      else:
        pass
      
      isEnglish = False
      isNumeric = False
      isSpecial = False
      
      for i in range(len(password)):
        
        if password[i].isalpha() == True:
          isEnglish = True
          continue
        
        if password[i].isdigit() == True:
          isNumeric = True
          continue
        
        if regex.search(password[i]) != None:
          isSpecial = True
          continue
        
        else:
          messagebox.showerror("Error", "What character did you input???")
          return
        
      if isEnglish == False:
        messagebox.showerror("Error", "Please have english characters in your password")
        return
      
      if isNumeric == False:
        messagebox.showerror("Error", "Please include numbers in your password")
        return
      
      if isSpecial == False:
        messagebox.showerror("Error", "Please include special characters in your password.")
        return
      
      byteRepPassword = password.encode(encoding="utf-8")
      sha256 = hashlib.sha256()
      sha256.update(byteRepPassword)
      hashedPassword = sha256.hexdigest()
      
      sql = f"INSERT INTO usercredentials VALUES('{username}','{hashedPassword}');"
      
      try:
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("Success!", ":D You created an user!!")
        return
      except:
        messagebox.showerror("Error", "Something happened while trying to create user, try again later or use different username and password.")
        return


class logIn(frontPageTemplate):
  
    
    def __init__(self, parent, controller):
      super().__init__(parent, controller)
      self.controller = controller
    
    def createLabel(self):
      
      self.label = ttk.Label(self, text="Log In", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
    
    def submit(self):
      username = self.usernameEntry.get()
      password = self.passwordEntry.get()

      if username.isalnum() == False:
        messagebox.showerror("Error", "Username can only contain english and numeric characters.")
        return
      
      byteRepPassword = password.encode(encoding="utf-8")
      sha256 = hashlib.sha256()
      sha256.update(byteRepPassword)
      hashedPassword = sha256.hexdigest()
      
      sql = f"SELECT * FROM usercredentials WHERE username = '{username}' AND password = '{hashedPassword}'"
      mycursor.execute(sql)
      data = mycursor.fetchall()
      
      if data:
        
        messagebox.showinfo("Success!", "You are logged on!!")
        global userID
        userID = username.lower()
        loggedIn = True
        self.controller.show_frame(importCSVPage)
        
      else:
        messagebox.showerror("Error!", "Username or password is incorrect")
      
      return
    
    
    
    
class importCSVPage(ttk.Frame):
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    style = ttk.Style()
    style.configure("TButton", width= 20,font=(None, 20))
    
    self.backButton = ttk.Button(self, text="Back to main menu", command=lambda: self.backFunction())
    self.backButton.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
    self.importingButton = ttk.Button(self, text="Import CSV", command=lambda: self.importCSV())
    self.importingButton.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
    self.explanationLabel = ttk.Label(self, text="The CSV file's first row must contain the words below in\nthe exact character(case sensitive):\n- firstName\n- secondName\n- phoneNumber\n- gender\n- email", font=("none, 14"))
    self.explanationLabel.place(relx=0.35, rely=0.75)
    
    
  def backFunction(self):
    
    loggedIn = False
    self.controller.show_frame(menu)
    
  def importCSV(self):
    
    
    requirementColumn = ['firstName', 'secondName', 'phoneNumber', 'gender', 'email']
    
    file = filedialog.askopenfilename(title="CSV File", initialdir='/', filetypes=[("CSV Files", "*.csv")])
    global columnName
    columnName = pd.read_csv(file, nrows=1).columns.to_list()    

    if len(columnName) == 5:
      
      for i in range(5):
        
        for j in range(5):
          
          if requirementColumn[i] == columnName[j]:
            break
          elif j < 4:
            continue
          else:
            messagebox.showerror("Error", "The CSV file is in the wrong format.")
            return
    else:
      messagebox.showerror("Error", "The CSV file is in the wrong format.")
      return 
    
    df = pd.read_csv(file, header=0, dtype={0:'string', 1:'string', 2:'string', 3:'string', 4:'string', 5:'string'})
    deleteSQL = f"DROP TABLE IF EXISTS `{userID}`;"
    mycursor.execute(deleteSQL)
    mydb.commit()
    createTableSQL = f"CREATE TABLE IF NOT EXISTS `{userID}` ({columnName[0]} varchar(255), {columnName[1]} varchar(255), {columnName[2]} varchar(255), {columnName[3]} varchar(255), {columnName[4]} varchar(255) );"
    mycursor.execute(createTableSQL)
    mydb.commit()
    df.drop(index=0)
    print("System log: table created for", userID)
    df.to_sql(userID, schema="COURSEWORK", con=connection, if_exists='append', index=False, chunksize=10000)
    
    messagebox.showinfo("Success!!!", "You have successfully imported a CSV file :D")
    self.controller.show_frame(mainMenu)
    
    
    
class mainMenu(importCSVPage):
  
    
  def __init__(self, parent, controller):
    
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    style = ttk.Style()
    style.configure("TButton", width= 15,font=(None, 20))

    self.welcomeLabel = ttk.Label(self, text=f"Welcome", font=("Helvetica", 40))
    self.welcomeLabel.place(relx=0.435, rely=0.1)
        
    self.backwardButton = ttk.Button(self, text="Log Out", command=lambda: [self.clearTreeData(self.tree), controller.show_frame(menu)])
    self.backwardButton.place(relx=0.05, rely=0.05)
    
    self.tree = ttk.Treeview(self, column=("First name", "Surname", "Gender", "Email", "Phone Number"), show='headings')
    self.tree.column("#1", anchor="w")
    self.tree.heading('#1', text="First Name") 
    
    self.tree.column("#2", anchor="w")
    self.tree.heading('#2', text="Surname")
     
    self.tree.column("#3", anchor="w")
    self.tree.heading('#3', text="Gender")
    
    self.tree.column("#4", anchor="w")
    self.tree.heading('#4', text="Email")
                      
    self.tree.column("#5", anchor="w")
    self.tree.heading('#5', text="Phone Number") 
    
    self.tree.pack(expand=True)
    
    self.refreshDataButton = ttk.Button(self, text="Refresh Data", command=lambda: self.refreshData(self.tree))
    self.loadNewData = ttk.Button(self, text="Import New Data", command=lambda: [importCSVPage.importCSV(self),self.refreshData(self.tree)])
    self.toolButton = ttk.Button(self, text="Tools", command=lambda: controller.show_frame(toolMenu))
    
    self.refreshDataButton.place(relx=0.4257, rely=0.79)
    self.loadNewData.place(relx=0.4257, rely= 0.86)
    self.toolButton.place(relx=0.4257, rely= 0.93)

    

    
  def clearTreeData(self, tree):
    for item in tree.get_children():
      tree.delete(item)
      
  def refreshData(self, tree):
    
    self.clearTreeData(tree)
    sql = f"SELECT firstName, secondName, gender, email, phoneNumber FROM `{userID}` LIMIT 100;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    rows = self.binary_sort(rows)
    for row in rows:
      tree.insert("", tk.END, values=row)
      
      
  # Function to perform binary sort using ord and chr
  def bubble_sort(self, rows):
    
    length = len(rows)
    
    for i in range(length):
      
      swapped = False
      
      for j in range(0, length-i-1):
        
        if ord(rows[j][0][0]) > ord(rows[j+1][0][0]):
          
          rows[j], rows[j+1] = rows[j+1], rows[j]
          swapped = True
        
      if not swapped:
        break
    return rows


class toolMenu(mainMenu):
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    
    self.backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(mainMenu))
    self.deleteButton = ttk.Button(self, text="Delete Record", command=lambda: controller.show_frame(deleteExplanationMenu))
    self.alterButton = ttk.Button(self, text="Alter Record", command=lambda: controller.show_frame(alterationExplanation))
    self.addNewButton = ttk.Button(self, text="Add New Record", command=lambda: controller.show_frame(additionRecord))
    self.searchMenuButton = ttk.Button(self, text="Search", command=lambda: controller.show_frame(searchMenu))
    
    self.backButton.place(relx=0.05, rely=0.05)
    self.deleteButton.place(relx=0.235, rely=0.3, height = 250, width= 400)
    self.alterButton.place(relx=0.235, rely= 0.6, height = 250, width= 400)
    self.addNewButton.place(relx=0.535, rely= 0.3, height = 250, width= 400)
    self.searchMenuButton.place(relx=0.535, rely=0.6, height = 250, width= 400)
    
    
class bluePrint(mainMenu):
  
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    
    self.controller = controller
    
    self.firstName = tk.StringVar()
    self.secondName = tk.StringVar()
    self.phoneNum = tk.StringVar()
    self.gender = tk.StringVar()
    self.email = tk.StringVar()
    
    self.firstName.trace_add("write", self.statusButton)
    self.secondName.trace_add("write", self.statusButton)
    self.phoneNum.trace_add("write", self.statusButton)
    self.gender.trace_add("write", self.statusButton)
    self.email.trace_add("write", self.statusButton)
    
    
  def userInputs(self, controller):
    
    self.fNameLabel = ttk.Label(self, text="First Name:", font=("none, 26"))
    self.sNameLabel = ttk.Label(self, text="Second Name:", font=("none, 26"))
    self.phoneLabel = ttk.Label(self, text="Phone Number:", font=("none, 26"))
    self.phoneExplanationLabel = ttk.Label(self, text="note: please add your country code\nto the number\nExample: +44741234567", font=("none, 15"))
    self.genderLabel = ttk.Label(self, text="Gender:", font=("none, 26"))
    self.emailLabel = ttk.Label(self, text="Email:", font=("none, 26"))
    
    
    self.fNameEntryBox = ttk.Entry(self, textvariable=self.firstName, font=("none, 24"))
    self.sNameEntryBox = ttk.Entry(self, textvariable=self.secondName, font=("none, 24"))
    self.phoneEntryBox = ttk.Entry(self, textvariable=self.phoneNum, font=("none, 24"))
    self.genderEntryBox = ttk.Entry(self, textvariable=self.gender, font=("none, 24"))
    self.emailEntryBox = ttk.Entry(self, textvariable=self.email, font=("none, 24"))

    self.actionButton = ttk.Button(self, text="Submit", state='disabled', command=lambda: [self.action()])
    
    self.backwardButton = ttk.Button(self, text="Go Back", command=lambda: self.backButtonFunction())
    self.backwardButton.place(relx=0.05, rely=0.05)
    
    
    
  def resultMenu(self, controller):
    
    self.resultLable()
    
    self.tree = ttk.Treeview(self, column=("First name", "Surname", "Gender", "Email", "Phone Number"), show='headings')
    self.tree.column("#1", anchor="w")
    self.tree.heading('#1', text="First Name") 
    
    self.tree.column("#2", anchor="w")
    self.tree.heading('#2', text="Surname")
    
    self.tree.column("#3", anchor="w")
    self.tree.heading('#3', text="Gender")
    
    self.tree.column("#4", anchor="w")
    self.tree.heading('#4', text="Email")
                      
    self.tree.column("#5", anchor="w")
    self.tree.heading('#5', text="Phone Number") 
    
    self.button(controller)  
  
  def showResultMenu(self):
    
    self.tree.pack(expand=True)

    
    
  def button(self, controller):
    
    pass
    
    
  def action(self):
    
    pass


  def statusButton(self, *args):
    
    if(len(self.firstName.get()) ) > 0 or len(self.secondName.get()) > 0 or len(self.phoneNum.get()) > 0 or len(self.email.get()) > 0 or len(self.gender.get()) > 0:
      
      self.actionButton.configure(state='normal')
      
    else:
      self.actionButton.configure(state='disabled')
      
      
  def clear_text(self):
    
    self.fNameEntryBox.delete(0, 'end')
    self.sNameEntryBox.delete(0,'end')
    self.phoneEntryBox.delete(0,'end')
    self.genderEntryBox.delete(0,'end')
    self.emailEntryBox.delete(0,'end')


  def showSearchMenu(self):
    
    self.fNameLabel.pack(side= "top", expand=True, pady=(25, 10))
    self.fNameEntryBox.pack(side= "top", expand=True)
    
    self.sNameLabel.pack(side= "top", expand=True, pady=(25, 10))
    self.sNameEntryBox.pack(side= "top", expand=True,)
    
    self.phoneLabel.pack(side= "top", expand=True,  pady=(25,0))
    self.phoneExplanationLabel.pack(side= "top", expand=True,  pady=(10, 10))
    self.phoneEntryBox.pack(side= "top", expand=True)
    
    self.genderLabel.pack(side= "top", expand=True, pady=(25, 10))
    self.genderEntryBox.pack(side= "top", expand=True)
    
    self.emailLabel.pack(side= "top", expand=True, pady=(25, 10))
    self.emailEntryBox.pack(side= "top", expand=True)
    
    self.actionButton.pack(side="top", pady= 50,expand=True, ipadx= 60, ipady=50)
    
    self.style = ttk.Style(self)
    self.style.configure('TButton', width=15)



  def hideSearchMenu(self):
    
    self.fNameLabel.pack_forget()
    self.sNameLabel.pack_forget()
    self.phoneLabel.pack_forget()
    self.phoneExplanationLabel.pack_forget()
    self.genderLabel.pack_forget()
    self.emailLabel.pack_forget()
    
    self.fNameEntryBox.pack_forget()
    self.sNameEntryBox.pack_forget()
    self.phoneEntryBox.pack_forget()
    self.genderEntryBox.pack_forget()
    self.phoneEntryBox.pack_forget()
    self.emailEntryBox.pack_forget()
    
    self.actionButton.pack_forget()


  def dynamicSQL(self, firstName, secondName, phoneNumber, gender, email, sql):
      
      conditions = []
      parms = []
      
      if firstName:
        conditions.append("firstname = %s")
        parms.append(firstName)
      
      
      if secondName:
        
        conditions.append("secondName = %s")
        parms.append(secondName)
      
      
      if phoneNumber:
        
        try:
          
          num = phonenumbers.parse(phoneNumber)
          if phonenumbers.is_possible_number(num) == True:
            
            conditions.append("phoneNumber = %s")
            parms.append(phoneNumber)
        
          else:
            messagebox.showerror("Error", "This doesn't seem like a correct phone number")
            return 1
          
        except:
          messagebox.showerror("Error", "This doesn't seem like a correct phone number, please remember to type the country code.")
          return 1
          
      
      if gender:
        
        if gender not in ["Non-binary" ,"Male", "Female"]:
          
          messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
          return 1
        
        else:
          
          conditions.append("gender = %s")
          parms.append(gender)
          
      if email:
        
        if ".com" in email and "@" in email:
          
          conditions.append("email = %s")
          parms.append(email)

        else:
          
          messagebox.showerror("Error", "This doesn't seem like a correct email")
          
      
      sql += " WHERE " + " AND ".join(conditions)

      return sql, parms
  

class searchMenu(bluePrint):
  
  def __init__(self, parent, controller):
    
    super().__init__(parent, controller)
    
    
    bluePrint.userInputs(self, controller)
    
    bluePrint.showSearchMenu(self)
    
    bluePrint.resultMenu(self, controller)
    
  
  def resultLable(self):
    
    self.result = ttk.Label(self, text="Result record", font=(None, 30))
    self.result.place(relx=0.435, rely = 0.1)

    
  def action(self):
      
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    bluePrint.clear_text(self)
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    if rows:
      
      
      for item in self.tree.get_children():
        self.tree.delete(item)
      
      bluePrint.hideSearchMenu(self)
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      
      print(rows)
      for row in rows:
        self.tree.insert("", tk.END, values=row)
        
        
    else:
      
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
    
    
    
    
  def resultLable(self):
    
    self.resultLable = ttk.Label(self, text="Result record", font=(None, 30))

    
  def searchFunction(self, firstName, secondName, phoneNumber, gender, email):
    
    sql = f"SELECT * FROM {userID}"
    sql, parms = bluePrint.dynamicSQL(self,firstName, secondName, phoneNumber, gender, email, sql)
    print(sql, parms)
    mycursor.execute(sql, parms)
    rows = mycursor.fetchall()
    
    return rows
  
  
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(mainMenu)


class deletionRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    super().__init__(parent, controller)
    
    
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(deleteExplanationMenu)
  
  
  def action(self):
      
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    bluePrint.clear_text(self)
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    if rows:
      
      
      for item in self.tree.get_children():
        self.tree.delete(item)
      
      bluePrint.hideSearchMenu(self)
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      
      self.deleteButton = ttk.Button(self, text="Delete", command=lambda: [self.delete(firstName, secondName, phoneNumber, gender, email), self.hideResultMenu(), self.showSearchMenu(), self.controller.show_frame(mainMenu)])
      self.deleteButton.place(relx=0.435, rely=0.75)
      
      print(rows)
      for row in rows:
        self.tree.insert("", tk.END, values=row)
        
        
    else:
      
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
    
  def delete(self, firstName, secondName, phoneNumber, gender, email):
    
    choice = messagebox.askokcancel(title="Delete", message="Are you sure you want to delete the record?", icon="warning")
    
    if choice == True:
      
      sql = f"DELETE FROM {userID}"
      sql, parms= bluePrint.dynamicSQL(self, firstName, secondName, phoneNumber, gender, email, sql)
      mycursor.execute(sql, parms)
      mydb.commit()
      messagebox.showinfo("Success", "You have deleted the record!")
      return 0
    
    

class deleteExplanationMenu(bluePrint):
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    
    self.explanationLabel = ttk.Label(
        self, 
        text="When you proceed to the next menu you are required to enter credentials first.\nIf there is record present then you are allowed to delete it. \nTo delete the whole CSV file, you can do so by clicking the 'Delete CSV' button.",
        font=("none, 20")
        )
    
    
    self.explanationLabel.place(relx=0.20, rely=0.35)
    style = ttk.Style()
    style.configure("TButton", width=20,font=(None, 20))
    
    self.backwardButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(mainMenu))
    self.buttonDeLuxDelete = ttk.Button(self, text="Proceed", command=lambda: controller.show_frame(deletionRecord))
    self.deleteCSVButton = ttk.Button(self, text="Delete CSV", command=lambda: self.deleteCSV(controller))
    
    self.backwardButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.buttonDeLuxDelete.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.deleteCSVButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    
    
  def deleteCSV(self, controller):
    
    choice = messagebox.askokcancel(title="Delete CSV", message="Are you sure you want to delete the CSV file?", icon="warning")
    
    if choice == True:
      
      secondChoice = messagebox.askokcancel(title="Delete CSV", message="Are you very sure?", icon="warning")
      
      if secondChoice == True:
        
        deleteSQL = f"DELETE FROM {userID};"
        mycursor.execute(deleteSQL)
        mydb.commit()
        messagebox.showinfo("Success", "You have deleted the CSV file")
        controller.show_frame(toolMenu)
        return 0 

      else:
        
        pass
      
      
    messagebox.showinfo("Info", "Returning you to the main menu.")
    controller.show_frame(mainMenu)
    return 0

class alterationExplanation(bluePrint):
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    
    self.explanationLabel = ttk.Label(
        self, 
        text="When you proceed to the next menu you are required to enter credentials first.\nIf there is record present then you are allowed to alter it.\nOtherwise, you can't alter the record.",
        font=("none, 20")
        )
    
    
    self.explanationLabel.place(relx=0.20, rely=0.35)
    style = ttk.Style()
    style.configure("TButton", width=20,font=(None, 20))
    
    self.backwardButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(toolMenu))
    self.buttonDeLuxAlter = ttk.Button(self, text="Proceed", command=lambda: controller.show_frame(alterationRecord))
    
    
    self.backwardButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.buttonDeLuxAlter.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)



class alterationRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    super().__init__(parent, controller)
    
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(alterationExplanation)
    
  def action(self):
    
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.email.get()
    
    bluePrint.clear_text(self)
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    if rows:
      
      
      for item in self.tree.get_children():
        self.tree.delete(item)
      
      
      bluePrint.hideSearchMenu(self)
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      
      print(rows)
      for row in rows:
        self.tree.insert("", tk.END, values=row)
        
      messagebox.showinfo("Info", "Please double check if the record(s) are correct.")
      
      self.alterButton = ttk.Button(self, text="Alter", command=lambda: [self.sqlFunc(firstName, secondName, phoneNumber, email, gender), self.controller.show_frame(finalAlterationRecord)])
      self.alterButton.place(relx=0.435, rely=0.75)
      
    else:
      
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
    
  def sqlFunc(self, firstName, secondName, phoneNumber, email, gender):
    
    
    global updateSQL
    global updateParms
    updateSQL = ""
    updateSQL, updateParms = bluePrint.dynamicSQL(self, firstName, secondName, phoneNumber, email, gender, updateSQL)
    

    
    
  def resultLable(self):
    
    self.resultLable = ttk.Label(self, text="Result record(s)", font=(None, 30))
    
    
class finalAlterationRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    super().__init__(parent, controller)
    
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(toolMenu)
    
  def action(self):
    
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.email.get()
    
    
    if phoneNumber:
        
      try:
        
        num = phonenumbers.parse(phoneNumber)
        if phonenumbers.is_possible_number(num) == False:
          
          messagebox.showerror("Error", "This doesn't seem like a correct phone number")
          bluePrint.clear_text(self)
          return 1
        
      except:
        
        messagebox.showerror("Error", "This doesn't seem like a correct phone number, please remember to type the country code.")
        bluePrint.clear_text(self)
        return 1
      
      
    if gender:
        
      if gender not in ["Non-binary" ,"Male", "Female"]:
          
        messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
        bluePrint.clear_text(self)
        return 1
    
    
    if email:
        
      if ".com" in email and "@" in email:
        
        pass

      else:
        
        messagebox.showerror("Error", "This doesn't seem like a correct email")
        bluePrint.clear_text(self)
        return 1
      
      
    choice = messagebox.askokcancel(title="Hmmm", message="Confirmation for altering the record", icon="warning")
    
    if choice == True:  
        
        finalUpdateSQL, parms = self.updateSQL(updateSQL, updateParms, firstName, secondName, phoneNumber, email, gender)
        print(finalUpdateSQL, parms)
        mycursor.execute(finalUpdateSQL, parms)
        mydb.commit()
        messagebox.showinfo("Success", "You have altered the record!")
        self.controller.show_frame(toolMenu)
        bluePrint.clear_text(self)
        return 0
        
        
  def updateSQL(self, sql, parms2, firstName, secondName, phoneNumber, email, gender):
    
    sql = f"UPDATE {userID}"
    conditions = []
    parms = []
    if firstName:
      
        conditions.append("firstname = %s")
        parms.append(firstName)
      
      
    if secondName:
      
      conditions.append("secondName = %s")
      parms.append(secondName)
    
    
    if phoneNumber:
          
      conditions.append("phoneNumber = %s")
      parms.append(phoneNumber)
      
    
    if gender:
      
      conditions.append("gender = %s")
      parms.append(gender)
        
    if email:
        
        conditions.append("email = %s")
        parms.append(email)
        
    sql += " SET " + ", ".join(conditions) + updateSQL
    parms = parms + parms2
    return sql, parms
    
class additionRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    super().__init__(parent, controller)
    
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(toolMenu)
    
  def action(self):
    
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    
    if phoneNumber:
        
      try:
        
        num = phonenumbers.parse(phoneNumber)
        if phonenumbers.is_possible_number(num) == False:
          
          messagebox.showerror("Error", "This doesn't seem like a correct phone number")
          bluePrint.clear_text(self)
          return 1
        
      except:
        
        messagebox.showerror("Error", "This doesn't seem like a correct phone number, please remember to type the country code.")
        bluePrint.clear_text(self)
        return 1
      
      
    if gender:
        
      if gender not in ["Non-binary" ,"Male", "Female"]:
          
        messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
        bluePrint.clear_text(self)
        return 1
    
    
    if email:
        
      if ".com" in email and "@" in email:
        
        pass

      else:
        
        messagebox.showerror("Error", "This doesn't seem like a correct email")
        bluePrint.clear_text(self)
        return 1
    
    
    choice = messagebox.askokcancel(title="Hmmm", message="Confirmation for adding the record", icon="warning")
    bluePrint.clear_text(self)
    
    if choice == True:
      
      try:
        
        sql = f"INSERT INTO `{userID}` (firstName, secondName, phoneNumber, email, gender) VALUES(%s, %s, %s, %s, %s);"
        parameter =  [firstName, secondName, phoneNumber, email, gender]
        mycursor.execute(sql, parameter)
        mydb.commit()
        messagebox.showinfo("Success", "You have added a new record!")
        
        self.controller.show_frame(toolMenu)
        return 0
      
      except:
        
        messagebox.showerror("Error", "Something happened while trying to add a new record, try again later.")
        return 1

    
App = app()
App.mainloop()

