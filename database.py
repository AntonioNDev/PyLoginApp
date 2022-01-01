import sqlite3
import os

databasePath = 'C:/Users/Antonio/Documents/PyLoginApp'
conn = sqlite3.connect(f'{databasePath}/database.db')
cur = conn.cursor()


#Create table 
def createTable():
   cur.execute("""CREATE TABLE IF NOT EXISTS users (
         username TEXT NOT NULL,
         password TEXT NOT NULL 
      );""")
   print('table created')

#Write data
def writeData(x1,x2):
   sendData = checkData(x1, x2)
   
   #Check if the account already exist.
   if sendData == True:
      return 'Account already exist'
   else:
      cur.execute("INSERT INTO users VALUES(?,?)", (x1,x2))
      conn.commit()
      return True

#check if the account exist
def checkData(x, y):
   cur.execute(f"SELECT * FROM users WHERE username='{x}' AND password='{y}'")
   m = cur.fetchall()
   
   #if length of the list is 1 then account already exist.
   if len(list(m)) == 1:
      return True
   return 'Wrong Password/Username OR account doesnt exist.'
   
#delete record
def deleteRecord(userId):
   cur.execute(f"DELETE FROM users WHERE rowid='{userId}'")
   conn.commit()

#display all data
def displayData():
   cur.execute('SELECT rowid, * FROM users')
   data = cur.fetchall()
   return data

#Update record
def updateData(userId, usr, pw):
   cur.execute(f"UPDATE users SET username='{usr}' WHERE rowid='{userId}'")
   conn.commit()

