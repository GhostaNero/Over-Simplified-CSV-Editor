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
