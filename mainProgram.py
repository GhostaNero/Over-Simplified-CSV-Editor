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


loggedIn = False

class app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)  
        container = ttk.Frame(self, relief="sunken")  
        container.pack(fill="both", expand = True)  
        self.frames = {}  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (menu, logIn, signUpMenu, importCSVPage):  
  
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
      
      self.explanationLabel = ttk.Label(self, text="1. Username can only contain english\n    and numeric characters.\n2. Password must contain english characters, \n    numeric characters and special characters.", font=("none, 14"))
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
    
    
    
  def backFunction(self):
    
    loggedIn = False
    self.controller.show_frame(menu)
    
  def importCSV(self):
    
    file = filedialog.askopenfilename(title="CSV File", initialdir='/', filetypes=[("CSV Files", "*.csv")])
    

    
    
    
App = app()
App.mainloop()

#very proud