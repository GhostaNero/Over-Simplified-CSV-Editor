import tkinter as tk
from tkinter import ttk
import sv_ttk
import os
import sys
import mysql.connector
import ignore
import pandas as pd
import sqlalchemy
import phonenumbers
import hashlib
PASSWORD = ignore.password


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
mydb.commit()
#execute to use the database 
mycursor.execute("USE COURSEWORK;")
mydb.commit()

loggedIn = False

class app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)  
        container = ttk.Frame(self, relief="sunken")  
        container.pack(fill="both", expand = True)  
        self.frames = {}  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for F in (menu, logIn, signUpMenu):  
  
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
        
        
class frontPageTemplate(ttk.Frame):
    
    def __init__(self, parent, controller):
        
        ttk.Frame.__init__(self,parent)
        
        self.createLabel()
        
        self.inputtedUsername = tk.StringVar()
        self.inputtedPassword = tk.StringVar()
        
        self.inputtedUsername.trace_add('write', self.statusButton)
        self.inputtedPassword.trace_add('write', self.statusButton)
        
        self.label1 = ttk.Label(self, text="Username:")
        self.label2 = ttk.Label(self, text="Password:")
        
        self.usernameEntry = ttk.Entry(self, textvariable=self.inputtedUsername)
        self.passwordEntry = ttk.Entry(self, textvariable=self.inputtedPassword)
        
        self.label1.pack(side="top", expand=True)
        self.usernameEntry.pack(side="top", expand=True)
        
        self.label2.pack(side="top", expand=True)
        self.passwordEntry.pack(side="top", expand=True)
                
        self.backwardButton = ttk.Button(self, text="Go Back", command=lambda: [self.clear_text(), controller.show_frame(menu)])
        self.backwardButton.pack(side="top",expand=True, ipady=50)
        
        self.submitButton = ttk.Button(self, text="Submit", state='disabled')
        self.submitButton.pack(side="left", pady=150,expand=True, ipadx= 60, ipady=50 )
        
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
              
      self.label = ttk.Label(self, text="Sign Up / Create user", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
      
class signUpMenu(frontPageTemplate):
    
    def __init__(self, parent, controller):
      super().__init__(parent, controller)
      
    def createLabel(self):
      
      self.label = ttk.Label(self, text="Sign Up / Create user", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)


class logIn(frontPageTemplate):
    
    def __init__(self, parent, controller):
      frontPageTemplate.__init__(self, parent, controller)
      
    def createLabel(self):
      
      self.label = ttk.Label(self, text="Log In", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
      
App = app()
App.mainloop()