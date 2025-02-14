import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sv_ttk
import sys
import mysql.connector
import ignore
import pandas as pd
import sqlalchemy
import phonenumbers
import hashlib
import re

PASSWORD = ignore.password

#store the special character in a regex object
regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

#establish a connection to the database
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=PASSWORD
    )
#establish a connection to the database using sqlalchemy
connection = sqlalchemy.create_engine(f'mysql+mysqlconnector://root:{PASSWORD}@localhost:3306')
#establish a cursor to interact with the database
mycursor = mydb.cursor(buffered=True)
#create the database if it doesnt exists
mycursor.execute("CREATE DATABASE IF NOT EXISTS COURSEWORK;")
mycursor.execute("USE COURSEWORK;")
mycursor.execute("CREATE TABLE IF NOT EXISTS userCredentials(username varchar(255) NOT NULL, password varchar(255) NOT NULL, PRIMARY KEY(username));")
mydb.commit()
#execute to use the database 

#declare a global variable which will store the username when the user log in
global userID
userID = ""

#declear the App class which will work as the "backend" to initiate all the objects and switch the frame
class app(tk.Tk):
  
    #init
    def __init__(self, *args, **kwargs):
      
      #initiate tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        
        #initiate a container frame  
        container = ttk.Frame(self, relief="sunken")  
        #pack to display on the screen
        container.pack(fill="both", expand = True)  
        #set up a tuple for the frames
        self.frames = {}  
        #configure the grid manager for the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #initiate a loop which will initiate all the frames
        for F in (startUpMenu, logIn, signUpMenu, importCSVPage, mainMenu, searchMenu, deleteExplanationMenu, alterationExplanation,finalAlterationRecord, alterationRecord, deletionRecord, alterationRecord, additionRecord, toolMenu):  
            
            frame = F(container, self)  

            self.frames[F] = frame  
  
            frame.grid(row=0, column=0, sticky="nsew")  
        #show the start up menu frame
        self.show_frame(startUpMenu)  
    # define the show_frame function which will raise and display whatever frame is passed in on top of the frame stack (basically what the user sees)
    def show_frame(self, cont):  
  
        frame = self.frames[cont]  
        frame.tkraise()  
        
#FUNCTIONAL REQUIREMENT 1       
#define the startUpMenu class (which will be the login / sign up page)
class startUpMenu(ttk.Frame):
    #init
    def __init__(self, parent, controller):
        #initiate the frame
        ttk.Frame.__init__(self,parent,)
        #set the theme
        sv_ttk.set_theme("dark")
        #initiate a style object 
        style = ttk.Style()
        #configure the style of the button
        style.configure("TButton", width= 20,font=(None, 20))
        #create and display a label for the user to see
        label = ttk.Label(self, text="Welcome to the CSV Navi!", font=("Helvetica", 40))
        label.pack(expand=True, pady=100)
        #create two buttons which redirects them to the relative page and display them
        button = ttk.Button(self, text="Log In", command=lambda: controller.show_frame(logIn))
        button.pack(side="left",expand=True,ipadx= 100, ipady=100)
        
        button2 = ttk.Button(self, text="Sign Up", command=lambda: controller.show_frame(signUpMenu),)
        button2.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
        #Create a quit program button and display it
        backwardButton = ttk.Button(self, text="Quit", command=lambda: sys.exit())
        backwardButton.place(relx=0.05, rely=0.05)

#FUNCTIONAL REQUIREMENT 2    
#create a class which will be the template for the login and sign up page
class frontPageTemplate(ttk.Frame):
    #init
    def __init__(self, parent, controller):
        
        #initiate the frame
        ttk.Frame.__init__(self, parent)
        #set the label relative to the function
        self.createLabel()
        #initiate the username and password variables
        self.inputtedUsername = tk.StringVar()
        self.inputtedPassword = tk.StringVar()
        #trace them to check if the user has inputted anything
        self.inputtedUsername.trace_add('write', self.statusButton)
        self.inputtedPassword.trace_add('write', self.statusButton)
        #create the labels and entry boxes for the username and password
        self.label1 = ttk.Label(self, text="Username:", font=("none, 26"))
        self.label2 = ttk.Label(self, text="Password:", font=("none, 26"))
        
        self.usernameEntry = ttk.Entry(self, textvariable=self.inputtedUsername, font=("none, 24"))
        self.passwordEntry = ttk.Entry(self, textvariable=self.inputtedPassword, font=("none, 24"), show="*")
        #pack them to display on the screen
        self.label1.pack(side="top", expand=True, pady=10)
        self.usernameEntry.pack(side="top", expand=True, pady=10)
        
        self.label2.pack(side="top", expand=True, pady=10)
        self.passwordEntry.pack(side="top", expand=True, pady=10)
        
        #the explanation text for the user (only for sign up)
        self.explanationText()
        
        #create the buttons for the user to go back and display it on the screen
        self.backwardButton = ttk.Button(self, text="Go Back", command=lambda: [self.clear_text(), controller.show_frame(startUpMenu)])
        self.backwardButton.place(relx=0.05, rely=0.05)
        
        #create the submit button and display it on the screen
        self.submitButton = ttk.Button(self, text="Submit", state='disabled', command=lambda: [self.submit(), self.clear_text()])
        self.submitButton.pack(side="top", pady= 50,expand=True, ipadx= 60, ipady=50)
        
        #create a style object and configure the button style
        self.style = ttk.Style(self)
        self.style.configure('TButton', width=15)
        
    #define the statusButton function which will check if the user has inputted anything    
    def statusButton(self,*args):
      
      if(len(self.inputtedUsername.get()) ) > 0 and len(self.inputtedPassword.get()) > 0:
        self.submitButton.configure(state='normal')
      else:
        self.submitButton.configure(state='disabled')
        
    #define the clear_text function which will clear the entry boxes    
    def clear_text(self):
      
      self.usernameEntry.delete(0, 'end')
      self.passwordEntry.delete(0,'end')
      
    #define the createLabel function which will create the label for the page, these methods will be used in the child class  
    def createLabel(self):
              
      pass
    
    #define the explanationText function which will create the explanation text for the page
    def explanationText(self):
      
      pass
    
    #define the submit function which will be used in the child class 
    def submit(self):
      
      pass
    
#create the sign up menu class which will inherit from the frontPageTemplate class   
class signUpMenu(frontPageTemplate):
    #init
    def __init__(self, parent, controller):
      #initiate everything in the parent class
      super().__init__(parent, controller)
      
    #override parent method  
    def createLabel(self):
      
      #create the label for the page and display it on the screen
      self.label = ttk.Label(self, text="Sign Up / Create user", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
    
    #override parent method  
    def explanationText(self):
      
      #create the explanation text for the user and display it on the screen
      self.explanationLabel = ttk.Label(self, text="1. Username can only contain english\n    and numeric characters\n    Also not case-sensitve.\n2. Password must contain english characters, \n    numeric characters and special characters.", font=("none, 14"))
      self.explanationLabel.pack(side="top", expand=True, pady=10)
    
    #override parent method  
    def submit(self):
      
      #get the values of the tkinter variables declared in the parent class
      username = self.usernameEntry.get()
      password = self.passwordEntry.get()

      #check if the username is alphanumeric
      if username.isalnum() == False:
        #if not, display an error message
        messagebox.showerror("Error", "Username can only contain english and numeric characters.")
        return
      
      #check if the username is already taken  
      sql = f"SELECT username FROM usercredentials WHERE username = '{username}'" 
      #execute the sql statement
      mycursor.execute(sql)
      #fetch the data
      data = mycursor.fetchall()
      
      #if the data is not empty, display an error message
      if data:
        
        messagebox.showerror("Error", "Username has been taken, oops :D")
        return
      
      #set up three boolean variable that needs to be true for the password to be valid
      isEnglish = False
      isNumeric = False
      isSpecial = False
      
      #loop through the characters in the password
      for i in range(len(password)):
        
        #if the password contains alphabetical character
        if password[i].isalpha() == True:
          #set the boolean to true
          isEnglish = True
          continue
        
        #if the password contains numeric character
        if password[i].isdigit() == True:
          #set the boolean to true
          isNumeric = True
          continue
        
        #if the password contains special character
        if regex.search(password[i]) != None:
          #set the boolean to true
          isSpecial = True
          continue
        
        #if the password contains any other character that is not english, numeric or special character display an error message
        else:
          #display an error message
          messagebox.showerror("Error", "What character did you input???")
          return
        
      #if no english character is present in the password  
      if isEnglish == False:
        
        #display an error message
        messagebox.showerror("Error", "Please have english characters in your password")
        return
      
      #if no numeric character is present in the password
      if isNumeric == False:
        
        #display an error message
        messagebox.showerror("Error", "Please include numbers in your password")
        return
      
      #if no special character is present in the password
      if isSpecial == False:
        
        #display an error message
        messagebox.showerror("Error", "Please include special characters in your password.")
        return
      
      #encode the password to bytes in utf-8
      byteRepPassword = password.encode(encoding="utf-8")
      #create a sha256 object
      sha256 = hashlib.sha256()
      #update the object with the byte representation of the password
      sha256.update(byteRepPassword)
      #get the hexdigest of the password
      hashedPassword = sha256.hexdigest()
      
      #create the sql statement to insert the username and password into the database
      sql = f"INSERT INTO usercredentials VALUES('{username}','{hashedPassword}');"
      
      try:
        #execute the sql statement, commit the change and display a success message
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("Success!", ":D You created an user!!")
        
      
      except:
        
        #if an error occurs, display an error message
        messagebox.showerror("Error", "Something happened while trying to create user, try again later or use different username and password.")
        return

#create the log in class which will inherit from the frontPageTemplate class
class logIn(frontPageTemplate):
  
    #init
    def __init__(self, parent, controller):
      #initiate everything in the parent class
      super().__init__(parent, controller)
      #declare the controller object
      self.controller = controller
    
    #override the parent method    
    def createLabel(self):
      
      #create and display the label for the page
      self.label = ttk.Label(self, text="Log In", font=("Helvetica", 40))
      self.label.pack(expand=True, pady=100)
    
    #override the parent method
    def submit(self):
      
      #get the values of the tkinter variables declared in the parent class
      username = self.usernameEntry.get()
      password = self.passwordEntry.get()
      
      #check if the username is alphanumeric
      if username.isalnum() == False:
        
        #if not, display an error message
        messagebox.showerror("Error", "Username can only contain english and numeric characters.")
        return
      
      #encode the password to bytes in utf-8
      byteRepPassword = password.encode(encoding="utf-8")
      #create a sha256 object
      sha256 = hashlib.sha256()
      #update the object with the byte representation of the password
      sha256.update(byteRepPassword)
      #get the hexdigest of the password
      hashedPassword = sha256.hexdigest()
      
      #create the sql statement to select the username and password from the database where the username and password matches the inputted username and password
      sql = f"SELECT * FROM usercredentials WHERE username = '{username}' AND password = '{hashedPassword}'"
      #execute the sql statement and fetch the data
      mycursor.execute(sql)
      data = mycursor.fetchall()
      
      #if the data is not empty, display a success message and redirect the user to the importCSVPage
      if data:
        
        messagebox.showinfo("Success!", "You are logged on!!")
        global userID
        userID = username.lower()
        self.controller.show_frame(importCSVPage)
      
      #if the data is empty, display an error message
      else:
        
        messagebox.showerror("Error!", "Username or password is incorrect")
        return
       
#create the class which displays the page for the user to import the CSV file   
class importCSVPage(ttk.Frame):
  
  #init
  def __init__(self, parent, controller):
    
    #initiate the frame
    ttk.Frame.__init__(self, parent)
    #set the controller object
    self.controller = controller
    #create a style object and change the style of the button
    style = ttk.Style()
    style.configure("TButton", width= 20,font=(None, 20))
    
    #create the back and import button and display them on the screen
    self.backButton = ttk.Button(self, text="Back to main menu", command=lambda: self.backFunction())
    self.backButton.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
    self.importingButton = ttk.Button(self, text="Import CSV", command=lambda: self.importCSV())
    self.importingButton.pack(side="left", pady=150,expand=True, ipadx= 100, ipady=100)
    
    #create the explanation label and display it on the screen
    self.explanationLabel = ttk.Label(self, text="The CSV file's first row must contain the words below in\nthe exact character(case sensitive):\n- firstName\n- secondName\n- phoneNumber\n- gender\n- email", font=("none, 14"))
    self.explanationLabel.place(relx=0.35, rely=0.75)
    
  #define the backFunction which will redirect the user to the login/signup menu
  def backFunction(self):
    
    self.controller.show_frame(startUpMenu)
  
  #define the importCSV function which will import the CSV file into the database
  def importCSV(self):
    
    #create a list of the required columns
    requirementColumn = ['firstName', 'secondName', 'phoneNumber', 'gender', 'email']
    
    #create a sub interface for the user to select the CSV file
    file = filedialog.askopenfilename(title="CSV File", initialdir='/', filetypes=[("CSV Files", "*.csv")])
     
    #global the columnName variable
    global columnName
    #read the first row of the CSV file and store it in columnName
    columnName = pd.read_csv(file, nrows=1).columns.to_list()    

    #check if the first row of the CSV file contains the required columns
    if len(columnName) == 5:
      
      #While there is still columns in the requirementColumn list
      while len(requirementColumn) > 0:
        
        #loop through the columnName list
        for i in range(len(columnName)):
          
          #if the column name is in the requirementColumn list
          if columnName[i] in requirementColumn:
            
            #remove the column name from the requirementColumn list
            requirementColumn.remove(columnName[i])
            continue
          
          #if the column name is not in the requirementColumn list
          else:
            
            #display an error message
            messagebox.showerror("Error", "The CSV file is in the wrong format.")
            return
    
    #if the first row of the CSV file does not contain the required columns amount
    else:
      messagebox.showerror("Error", "The CSV file is in the wrong format.")
      return 
    
    #initiate a dataframe which reads all the CSV data
    df = pd.read_csv(file, header=0, dtype={0:'string', 1:'string', 2:'string', 3:'string', 4:'string', 5:'string'})
    #delete the user specific table if it exists
    deleteSQL = f"DROP TABLE IF EXISTS `{userID}`;"
    mycursor.execute(deleteSQL)
    mydb.commit()
    #recreate the user specific table
    createTableSQL = f"CREATE TABLE IF NOT EXISTS `{userID}` ({columnName[0]} varchar(255), {columnName[1]} varchar(255), {columnName[2]} varchar(255), {columnName[3]} varchar(255), {columnName[4]} varchar(255) );"
    mycursor.execute(createTableSQL)
    mydb.commit()
    #drop the first row (which should contain the header)
    df.drop(index=0)
    #print a log
    print("System log: table created for", userID)
    #load the dataframe to the SQA
    df.to_sql(userID, schema="COURSEWORK", con=connection, if_exists='append', index=False, chunksize=10000)
    #display success message
    messagebox.showinfo("Success!!!", "You have successfully imported a CSV file :D")
    #show the main menu
    self.controller.show_frame(mainMenu)
    
    
#create the main menu class which will inherit from the importCSVPage class
class mainMenu(importCSVPage):
  
  #init  
  def __init__(self, parent, controller):
    
    #initiate the frame
    ttk.Frame.__init__(self, parent)
    #set the controller object
    self.controller = controller
    #create a style object and configure the button style
    style = ttk.Style()
    style.configure("TButton", width= 15,font=(None, 20))

    #create the welcome label and display it on the screen
    self.welcomeLabel = ttk.Label(self, text=f"Welcome", font=("Helvetica", 40))
    self.welcomeLabel.place(relx=0.435, rely=0.1)
    
    #create the log out button and display it on the screen    
    self.backwardButton = ttk.Button(self, text="Log Out", command=lambda: [self.clearTreeData(self.tree), controller.show_frame(startUpMenu)])
    self.backwardButton.place(relx=0.05, rely=0.05)
    
    #create the treeview object and display it on the screen
    self.tree = ttk.Treeview(self, column=("First name", "Surname", "Gender", "Email", "Phone Number"), show='headings')
    #configure the tree's columns and headings
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
    
    #create the refresh data, import new data, tools and export button and display them on the screen
    self.refreshDataButton = ttk.Button(self, text="Refresh Data", command=lambda: self.refreshData(self.tree))
    self.loadNewData = ttk.Button(self, text="Import New Data", command=lambda: [importCSVPage.importCSV(self),self.refreshData(self.tree)])
    self.toolButton = ttk.Button(self, text="Tools", command=lambda: controller.show_frame(toolMenu))
    self.exportButton = ttk.Button(self, text="Export CSV", command=lambda: self.exportCSV())
    
    self.refreshDataButton.place(relx=0.4257, rely=0.79)
    self.loadNewData.place(relx=0.4257, rely= 0.86)
    self.toolButton.place(relx=0.4257, rely= 0.93)
    self.exportButton.place(relx=0.4257, rely= 0.72)

  #define the exportCSV function which will export the data in the table to a CSV file  
  def exportCSV(self):
    
    #create a file dialog for the user to select the location of the CSV file
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    #create a sql statement to get the column name of the table
    columnSQL = f"Show columns from {userID};"
    mycursor.execute(columnSQL)
    columns = mycursor.fetchall()
    #store the column names in a list
    columns = [column[0] for column in columns]
    #create a sql statement to fetch all of the data from the table
    sql = f"SELECT * FROM {userID}"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    #create a dataframe with the data and column names
    df = pd.DataFrame(rows, columns=columns)
    #export the dataframe to a CSV file and display a success message
    df.to_csv(file, index=False)
    messagebox.showinfo("Success", "You have exported the CSV file")
    
    
  #define the clearTreeData function which will clear the data in the treeview object 
  def clearTreeData(self, tree):
    for item in tree.get_children():
      tree.delete(item)
  
  #define the refreshData function which will refresh the data in the treeview object    
  def refreshData(self, tree):
    
    #clear the data in the treeview object
    self.clearTreeData(tree)
    #create a sql statement to fetch all of the data from the table
    sql = f"SELECT firstName, secondName, gender, email, phoneNumber FROM `{userID}` LIMIT 100;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    #sort the datas in the rows into alphabetical order using bubble sort
    rows = self.bubble_sort(rows)
    #insert the data into the treeview object
    for row in rows:
      tree.insert("", tk.END, values=row)
      
      
  #define the bubble_sort function which will sort the data in the rows into alphabetical order
  def bubble_sort(self, rows):
    
    #get the length of the rows
    length = len(rows)
    #loop through the rows
    for i in range(length):
      #set swapped to false
      swapped = False
      #loop through the rows again
      for j in range(0, length-i-1):
        #if the first character of the first name is greater than the first character of the second name
        if ord(rows[j][0][0]) > ord(rows[j+1][0][0]):
          #swap the rows
          rows[j], rows[j+1] = rows[j+1], rows[j]
          swapped = True
      #if swapped is false, break the loop  
      if not swapped:
        
        break
    #return the sorted rows  
    return rows

#create the class which will display a menu with all the tools to manipulatte the CSV file. This class will inherit from the mainMenu class
class toolMenu(mainMenu):
  
  #init
  def __init__(self, parent, controller):
    
    #initiate the frame
    ttk.Frame.__init__(self, parent)
    #set the controller object
    self.controller = controller
    
    #create the buttons for the user to go back, delete record, alter record, add new record and search records
    self.backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(mainMenu))
    self.deleteButton = ttk.Button(self, text="Delete Record", command=lambda: controller.show_frame(deleteExplanationMenu))
    self.alterButton = ttk.Button(self, text="Alter Record", command=lambda: controller.show_frame(alterationExplanation))
    self.addNewButton = ttk.Button(self, text="Add New Record", command=lambda: controller.show_frame(additionRecord))
    self.searchMenuButton = ttk.Button(self, text="Search", command=lambda: controller.show_frame(searchMenu))
    
    #display all the buttons created above on the screen
    self.backButton.place(relx=0.05, rely=0.05)
    self.deleteButton.place(relx=0.235, rely=0.3, height = 250, width= 400)
    self.alterButton.place(relx=0.235, rely= 0.6, height = 250, width= 400)
    self.addNewButton.place(relx=0.535, rely= 0.3, height = 250, width= 400)
    self.searchMenuButton.place(relx=0.535, rely=0.6, height = 250, width= 400)
    
#create the class for which contains the methods, general displays for all the tools (Alteration, Deletion, Addition, Search)    
class bluePrint(mainMenu):
  
  #init
  def __init__(self, parent, controller):
    
    #initiate the frame
    ttk.Frame.__init__(self, parent)
    #set the controller object
    self.controller = controller
    #create the variables for the user inputs
    self.firstName = tk.StringVar()
    self.secondName = tk.StringVar()
    self.phoneNum = tk.StringVar()
    self.gender = tk.StringVar()
    self.email = tk.StringVar()
    #trace the variables to check if the user has inputted anything
    self.firstName.trace_add("write", self.statusButton)
    self.secondName.trace_add("write", self.statusButton)
    self.phoneNum.trace_add("write", self.statusButton)
    self.gender.trace_add("write", self.statusButton)
    self.email.trace_add("write", self.statusButton)
    
  #define the function for the user inputs  
  def userInputs(self, controller):
    
    #create the labels and entry boxes for the user inputs
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
    #create the submit button
    self.actionButton = ttk.Button(self, text="Submit", state='disabled', command=lambda: [self.action()])
    #create the go back button and display it
    self.backwardButton = ttk.Button(self, text="Go Back", command=lambda: self.backButtonFunction())
    self.backwardButton.place(relx=0.05, rely=0.05)
    
    #note: in this function none of the widgets are packed, they will be packed in the child class. The only exception is the backwards button.
  
  #create a function for the result menu, which is the general display menu for the aftermaths of the usages of the tools
  def resultMenu(self, controller):
    
    #create the result label and display it on the screen
    self.resultLable()
    
    #create the treeview object and display it on the screen
    self.tree = ttk.Treeview(self, column=("First name", "Surname", "Gender", "Email", "Phone Number"), show='headings')
    #configure the tree's columns and headings
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
  
  #create the function to show the result menu
  def showResultMenu(self):
    
    self.tree.pack(expand=True)

  #create the action function which will be overrided in the child class to tailor to the specific need of the class
  def action(self):
    
    pass

  #create the function to monitor the entry boxes and check if anything has been inputted.
  def statusButton(self, *args):
    
    if(len(self.firstName.get()) ) > 0 or len(self.secondName.get()) > 0 or len(self.phoneNum.get()) > 0 or len(self.email.get()) > 0 or len(self.gender.get()) > 0:
      
      self.actionButton.configure(state='normal')
      
    else:
      self.actionButton.configure(state='disabled')
      
  #create the function to clear all the texts on the entry box
  def clear_text(self):
    
    self.fNameEntryBox.delete(0, 'end')
    self.sNameEntryBox.delete(0,'end')
    self.phoneEntryBox.delete(0,'end')
    self.genderEntryBox.delete(0,'end')
    self.emailEntryBox.delete(0,'end')

  #create the function to show the user inputs
  def showSearchMenu(self):
    
    #display all the label and entry box onto the screen
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
    #create a style objects that styles the button
    self.style = ttk.Style(self)
    self.style.configure('TButton', width=15)


  #create the function to hide the user input boxes
  def hideSearchMenu(self):
    
    #hide all the label, entry box and button by using pack_forget
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

  #Function for creating the conditions for SQL statements
  def dynamicSQL(self, firstName, secondName, phoneNumber, gender, email, sql):
      
      #create a list of conditions and parameters
      conditions = []
      parms = []
      
      '''
      This is done through a series of if statements
      if the user has inputted anything into the entry box, 
      the condition will be added to the conditions list and the parameter will be added to the parms list.
      
      There are some with additional checks, such as the phone numbers and email.
      '''
      
      if firstName:
        
        conditions.append("firstname = %s")
        parms.append(firstName)
      
      if secondName:
        
        conditions.append("secondName = %s")
        parms.append(secondName)
    
      if phoneNumber:
        
        try:
          
          #parse the phone number
          num = phonenumbers.parse(phoneNumber)
          #check if the numbers is a possible phone number
          if phonenumbers.is_possible_number(num) == True:
            #if its true then append the condition and parameter to the lists
            conditions.append("phoneNumber = %s")
            parms.append(phoneNumber)
          #Send error message if the number is not possible
          else:
            messagebox.showerror("Error", "This doesn't seem like a correct phone number, please remember to add the country code.")
            return 1
        #if there was a few things wrong with adding the phone number, send an error message
        except:
          messagebox.showerror("Error", "There seems to be something wrong while adding the phone number")
          return 1
          
      
      if gender:
        #if the gender is not in the list of the requirements, send an error message
        if gender not in ["Non-binary" ,"Male", "Female"]:
          
          messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
          return 1
        
        else:
          #append the conditions and parms into the relative list
          conditions.append("gender = %s")
          parms.append(gender)
          
      if email:
        #if the email is in the correct format, append the conditions and parms into the relative list
        if ".com" in email and "@" in email:
          
          conditions.append("email = %s")
          parms.append(email)
        #if the email is not in the correct format, send an error message
        else:
          
          messagebox.showerror("Error", "This doesn't seem like a correct email")
          
      #Join the conditions list with "AND" and add it to the sql statement
      sql += " WHERE " + " AND ".join(conditions)

      #return the statement and the parameters
      return sql, parms
  
#creates the class to display the search menu for a record
class searchMenu(bluePrint):
  
  def __init__(self, parent, controller):
    #initiate everything in the parent class
    super().__init__(parent, controller)
    #create the input boxes
    bluePrint.userInputs(self, controller)
    #show the input boxes
    bluePrint.showSearchMenu(self)
    #create the result menu note: the result menu isn't shown 
    bluePrint.resultMenu(self, controller)
    
  #define the result lable function
  def resultLable(self):
    
    self.result = ttk.Label(self, text="Result record", font=(None, 30))
    self.result.place(relx=0.435, rely = 0.1)

  #define the action function
  def action(self):
     
    #get the values of the user inputs 
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    #clear the text in the entry boxes
    bluePrint.clear_text(self)
    #run the search function which returns a list of rows of data
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    #If there is data in the rows
    if rows:
      
      mainMenu.bubble_sort(self, rows)
      
      #for every data in the treeview object, delete it
      for item in self.tree.get_children():
        self.tree.delete(item)
      
      #hide the search menu
      bluePrint.hideSearchMenu(self)
      #show the result menu and label
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      
      #print the rows for logs
      print(rows)
      #for every row in the list, insert them into the treeview.
      for row in rows:
        self.tree.insert("", tk.END, values=row)
        
    #If there is no data in the rows
    else:
      #send an error message
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
    
  #define the result label function  
  def resultLable(self):
    
    #create a result label for the user to see, this is not displayed yet.
    self.resultLable = ttk.Label(self, text="Result record", font=(None, 30))

  #define the search function    
  def searchFunction(self, firstName, secondName, phoneNumber, gender, email):
    
    '''
    This code works as the following:
    1. First create a statement to select all the data from the user specific table,
    2. Then use the dynamic SQL statement to get the conditions added onto the current SQL statement and the relative parameters
    3. Finally executes it and fetches the data.
    '''
    #1.
    sql = f"SELECT * FROM {userID}"
    #2.
    sql, parms = bluePrint.dynamicSQL(self,firstName, secondName, phoneNumber, gender, email, sql)
    #this was for log purposes
    print(sql, parms)
    #3.
    mycursor.execute(sql, parms)
    rows = mycursor.fetchall()
    #returns the data
    return rows
  
  #define the back button function
  def backButtonFunction(self):
    
    '''
    Note: As said before, each frame was already loaded in and just stacked on top of each other.
          So this means that I had to hide the result menu and load up the search menu again.
          Then put raise the menu to the top of the stack. 
          A bit like a theater, preparing the scene the user would see when they clicked into the search screen again.
    '''
    #clear the text in the entry boxes
    bluePrint.clear_text(self)
    #hide the treeview
    self.tree.pack_forget()
    #hide the result label
    self.resultLable.place_forget()
    #show the search menu
    bluePrint.showSearchMenu(self)
    #show the main menu
    self.controller.show_frame(toolMenu)


class deletionRecord(searchMenu):
  
  #Init
  def __init__(self, parent, controller):
    
    #Initiate everything in the parent class
    super().__init__(parent, controller)
    
  #define the back button function  
  def backButtonFunction(self):
    
    '''
    Note: As said before, each frame was already loaded in and just stacked on top of each other.
          So this means that I had to hide the result menu and load up the search menu again.
          Then put raise the menu to the top of the stack. 
          A bit like a theater, preparing the scene the user would see when they clicked into the search screen again.
    '''
    #clear the text in the entry boxes
    bluePrint.clear_text(self)
    #hide the treeview
    self.tree.pack_forget()
    #hide the result label
    self.resultLable.place_forget()
    #show the search menu
    bluePrint.showSearchMenu(self)
    #show the explanation menu for deleting
    self.controller.show_frame(deleteExplanationMenu)
    
  #create the action function, this overrides the parent method 
  def action(self):
     
    #get the values of the user inputs
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    #clear the text in the entry boxes
    bluePrint.clear_text(self)
    #run the search function which returns a list of rows of data
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    #If there is data in the rows
    if rows:
      
      #for every data in the treeview object, delete it
      for item in self.tree.get_children():
        self.tree.delete(item)
      
      #hide the search menu
      bluePrint.hideSearchMenu(self)
      #show the result menu and label
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      '''
      Create and place the delete button onto the screen
      Note:
      When this button is clicked, it will delete the records using the delete function,
      then it will hide the result menu / deletion menu and show the previous frame
      finally removing the deleteButton from the screen and show the main menu.
      '''
      self.deleteButton = ttk.Button(self, text="Delete", command=lambda: [self.delete(firstName, secondName, phoneNumber, gender, email), searchMenu.backButtonFunction(self), self.deleteButton.place_forget(), self.controller.show_frame(mainMenu)])
      self.deleteButton.place(relx=0.435, rely=0.75)
      #print the rows for log purpose
      print(rows)
      #insert the data in the rows into the tree
      for row in rows:
        self.tree.insert("", tk.END, values=row)
        
    #if there is nothing, then display the message to the user    
    else:
      
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
  
  #define the delete function  
  def delete(self, firstName, secondName, phoneNumber, gender, email):
    
    #ask the user through a messagebox if they are sure about deleting the data
    choice = messagebox.askokcancel(title="Delete", message="Are you sure you want to delete the record?", icon="warning")
    
    #If true
    if choice == True:
      #Create the SQL statement with out the condition
      sql = f"DELETE FROM {userID}"
      #Get the complete SQL statement with the conditions attached and the parameter for the condition
      sql, parms= bluePrint.dynamicSQL(self, firstName, secondName, phoneNumber, gender, email, sql)
      #execute and commit
      mycursor.execute(sql, parms)
      mydb.commit()
      #display success message
      messagebox.showinfo("Success", "You have deleted the record!")
    
#Create the explanation menu for how the process is going to work for deleting data
class deleteExplanationMenu(bluePrint):

  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    
    #Create the explanation text and display it onto the screen
    self.explanationLabel = ttk.Label(
        self, 
        text="When you proceed to the next menu you are required to enter credentials first.\nIf there is record present then you are allowed to delete it. \nTo delete the whole CSV file, you can do so by clicking the 'Delete CSV' button.",
        font=("none, 20")
        )
    self.explanationLabel.place(relx=0.20, rely=0.35)
    
    #Configure the style of button through the initiated style object
    style = ttk.Style()
    style.configure("TButton", width=20,font=(None, 20))
    
    #Create the button for going back, deleting specific record and clearing the whole CSV file and displaying them onto the screen.
    self.backwardButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(mainMenu))
    self.buttonDeLuxDelete = ttk.Button(self, text="Proceed", command=lambda: controller.show_frame(deletionRecord))
    self.deleteCSVButton = ttk.Button(self, text="Delete CSV", command=lambda: self.deleteCSV(controller))
    
    self.backwardButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.buttonDeLuxDelete.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.deleteCSVButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    
  #define the function to delete the whole CSV file  
  def deleteCSV(self, controller):
    
    #Double check with the user if they want to delete the whole CSV File
    choice = messagebox.askokcancel(title="Delete CSV", message="Are you sure you want to delete the CSV file?", icon="warning")
    
    #If the choice is True
    if choice == True:
      #Ask again for a final confirmation
      secondChoice = messagebox.askokcancel(title="Delete CSV", message="Are you very sure?", icon="warning")
      #If that is also true
      if secondChoice == True:
        #Create the SQL statement with no condition, execute it and commit it.
        deleteSQL = f"DELETE FROM {userID};"
        mycursor.execute(deleteSQL)
        mydb.commit()
        #display success message and show the main menu
        messagebox.showinfo("Success", "You have deleted the CSV file")
        controller.show_frame(mainMenu)
        return 0 
    #if the choice wasn't true then just return them to the main menu.
    messagebox.showinfo("Info", "Returning you to the main menu.")
    controller.show_frame(mainMenu)
    return 0
  
#define the class for the alter tool  
class alterationExplanation(bluePrint):
  
  def __init__(self, parent, controller):
    
    ttk.Frame.__init__(self, parent)
    self.controller = controller
    
    #Create and display the explanation text for how the tool is going to work.
    self.explanationLabel = ttk.Label(
        self, 
        text="When you proceed to the next menu you are required to enter credentials first.\nIf there is record present then you are allowed to alter it.\nOtherwise, you can't alter the record.",
        font=("none, 20")
        )
    self.explanationLabel.place(relx=0.20, rely=0.35)
    #create the style object to configure the style of the buttons
    style = ttk.Style()
    style.configure("TButton", width=20,font=(None, 20))
    
    #Create the button for going back to the tool menu and proceed. Then display them onto the screen
    self.backwardButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(toolMenu))
    self.buttonDeLuxAlter = ttk.Button(self, text="Proceed", command=lambda: controller.show_frame(alterationRecord))
    
    self.backwardButton.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)
    self.buttonDeLuxAlter.pack(side="left", anchor="s",expand=True, ipadx= 100, ipady=100, pady=100)

#Create the class for the frame where the user inputs the search criteria
class alterationRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    #Initiate everything in the parent class, which is the search menu. This quite literally mean we are searching a record first
    super().__init__(parent, controller)
  
  #Overrides the backButtonFunction which now does everything the same except goes back to the explanation page  
  def backButtonFunction(self):
    
    bluePrint.clear_text(self)
    self.tree.pack_forget()
    self.resultLable.place_forget()
    self.alterButton.place_forget()
    bluePrint.showSearchMenu(self)
    self.controller.show_frame(alterationExplanation)
  
  #Overrides the action button in the parent class  
  def action(self):
    
    #Gets the values of the user input
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.email.get()
    
    #Clear the entry box texts
    bluePrint.clear_text(self)
    #search for the data and return it
    rows = self.searchFunction(firstName, secondName, phoneNumber, gender, email)
    
    #If there is data
    if rows:
      
      #Delete every item in the treeview
      for item in self.tree.get_children():
        self.tree.delete(item)
      #Hide the search menu, create and place the result label and result menu
      bluePrint.hideSearchMenu(self)
      self.resultLable.place(relx=0.435, rely = 0.1)
      bluePrint.showResultMenu(self)
      #log purposes
      print(rows)
      #For every row in the dataset, insert it into the treeview
      for row in rows:
        self.tree.insert("", tk.END, values=row)
      
      #Asks the user to double check the records are correct  
      messagebox.showinfo("Info", "Please double check if the record(s) are correct.")
      
      #Create the alteration button, when pressed will call the SQL function and show the final frame for the alteration
      self.alterButton = ttk.Button(self, text="Alter", command=lambda: [self.sqlFunc(firstName, secondName, phoneNumber, email, gender), self.controller.show_frame(finalAlterationRecord)])
      self.alterButton.place(relx=0.435, rely=0.75)
      
    #If there is no data, tell the user about it and return.
    else:
      
      messagebox.showinfo("Hmm", "It seems that there is nothing...")
      return 1
  
  #Define the SQL function   
  def sqlFunc(self, firstName, secondName, phoneNumber, email, gender):
    
    #set two global parameter which will be used in the finalAlterationClass
    global updateSQL
    global updateParms
    '''
    Note: In the update SQL function, the SQL statement has a WHERE clause,
          Therefore I have to create a global variable to store the WHERE clause and the parameters for the WHERE clause.
          So when the user clicks the alter button, the finalAlterationRecord class can use the WHERE clause and the parameters to update the record.
          To do this I will concatenate the WHERE clause and the parameters to the SQL statement in the finalAlterationRecord class.
    '''
    updateSQL = ""
    updateSQL, updateParms = bluePrint.dynamicSQL(self, firstName, secondName, phoneNumber, email, gender, updateSQL)
    
  #define result lable  
  def resultLable(self):
    
    self.resultLable = ttk.Label(self, text="Result record(s)", font=(None, 30))
    
#Create the class for the final frame for altering records
class finalAlterationRecord(searchMenu):
  
  def __init__(self, parent, controller):
    #initiate everything in the parent class as usual
    super().__init__(parent, controller)

  #define the action button which overrides the parent method  
  def action(self):
    #get all the values of the user inputs
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    #If phone number is inputted
    if phoneNumber:
      
      #parse the phone number and check if the number is a possible phone number
      num = phonenumbers.parse(phoneNumber)
      if phonenumbers.is_possible_number(num) == False:
        #if its not possible, send an error message
        messagebox.showerror("Error", "This doesn't seem like a correct phone number")

        return 1
      
    #If gender is inputted  
    if gender:
        
      #check if the gender is in one of the choices  
      if gender not in ["Non-binary", "Male", "Female"]:
        #if its not then display an error message  
        messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
  
        return 1
    
    #if the user has inputted email
    if email:
      
      #check if the email is in the correct format  
      if ".com" not in email and "@" not in email:
        #if its not in the correct format then display the error message
        messagebox.showerror("Error", "This doesn't seem like a correct email")
        bluePrint.clear_text(self)
        return 1
      
    #Ask the user for confirmation
    choice = messagebox.askokcancel(title="Hmmm", message="Confirmation for altering the record", icon="warning")
    
    #if the choice is true
    if choice == True:  
        
        #get the final SQL statement and parameter returned from the updateSQL function
        finalUpdateSQL, parms = self.updateSQL(updateSQL, updateParms, firstName, secondName, phoneNumber, email, gender)
        #log purposes
        print(finalUpdateSQL, parms)
        #Execute and commit the change
        mycursor.execute(finalUpdateSQL, parms)
        mydb.commit()
        #show the success message
        messagebox.showinfo("Success", "You have altered the record!")
        #show the tool menu
        self.controller.show_frame(toolMenu)
        bluePrint.clear_text(self)
        return 0
        
  #create the updateSQL function      
  def updateSQL(self, sql, parms2, firstName, secondName, phoneNumber, email, gender):
    
    #Create the first part of the SQL statement
    sql = f"UPDATE {userID}"
    #create the arrays to store conditions and parameters
    conditions = []
    parms = []
    '''
    The nexts section of if statements basically check if there is an input for the variables, 
    and if there is append the condition and parameter.
    '''
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
        
    #create the complete SQL statement and parameter
    sql += " SET " + ", ".join(conditions) + updateSQL
    parms = parms + parms2
    #return the parameter and SQL statement
    return sql, parms
 
#Define the class for adding records    
class additionRecord(searchMenu):
  
  def __init__(self, parent, controller):
    
    #Initiate everything in search menu
    super().__init__(parent, controller)
  
  #overrides the action button  
  def action(self):
    
    #gets all the values the user inputted
    firstName = self.firstName.get()
    secondName = self.secondName.get()
    phoneNumber = self.phoneNum.get()
    email = self.email.get()
    gender = self.gender.get()
    
    #if phone number was entered
    if phoneNumber:
      
      #parse the number  
      num = phonenumbers.parse(phoneNumber)
      #check if the number is a possible phone number
      if phonenumbers.is_possible_number(num) == False:
        #show error message if its not
        messagebox.showerror("Error", "This doesn't seem like a correct phone number")
        return 1
      
    #if gender was entered  
    if gender:
      #if gender is not one of the three choices  
      if gender not in ["Non-binary" ,"Male", "Female"]:
        #show an error message  
        messagebox.showerror("Error", "This doesn't seem like a correct gender, its only Non-binary, Male or Female")
        return 1
    
    #if email was entered
    if email:
      #if email is not in the correct format  
      if ".com" not in email and "@" not in email:
        #show an error message
        messagebox.showerror("Error", "This doesn't seem like a correct email")
        return 1
    
    #ask the user for confirmation
    choice = messagebox.askokcancel(title="Hmmm", message="Confirmation for adding the record", icon="warning")
    
    if choice == True:
      
      bluePrint.clear_text(self)
      
      try:
        #create the SQL statement
        sql = f"INSERT INTO `{userID}` (firstName, secondName, phoneNumber, email, gender) VALUES(%s, %s, %s, %s, %s);"
        #set the parameters
        parameter =  [firstName, secondName, phoneNumber, email, gender]
        #execute and commit the sql statement
        mycursor.execute(sql, parameter)
        mydb.commit()
        #show the success message
        messagebox.showinfo("Success", "You have added a new record!")
        #show the tool menu frame
        self.controller.show_frame(toolMenu)
        return 0
      
      #except if there was an error in inserting the new record
      except:
        #show the error message
        messagebox.showerror("Error", "Something happened while trying to add a new record, try again later.")
        return 1

#create an instance of the app object   
App = app()
#initialise the TK mainframe loop.
App.mainloop()

