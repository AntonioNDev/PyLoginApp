import logging
import datetime
import os
from tkinter import messagebox as mb
import database as db


currentPath = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=f'{currentPath}/appLogs.log', level=logging.INFO, format='%(levelname)s-%(message)s')
date = datetime.datetime.now().strftime('[%d/%m/%Y|%H:%M:%S]')


class App:
    def __init__(self, username, passowrd):
        self.username = username
        self.password = passowrd
    
    def login(self):
        x = db.checkData(self.username, self.password)
        if x == True:
            logging.info(f'{date}-User {self.username} logged in')
            mb.showinfo('Info', 'User logged in')   
        else:
            logging.warning(f'{date}-User tried logging in but something went wrong. Error: [{x}]')
            popUp = mb.askyesnocancel('Info', f'Wrong password/username OR the account doesn\'t exist. Do you want to create an account with this info?') 
            if popUp == True:
                db.writeData(self.username, self.password)
                logging.info(f'{date}-Account created [Username:{self.username}|Password:{self.password}].')
                popUp = mb.showinfo('Info', 'Account created.') 

    def signup(self):
        x = db.writeData(self.username, self.password)
        if x == True:
            logging.info(f'{date}-Account created [Username:{self.username}|Password:{self.password}].')
            mb.showinfo('Info', 'Account created.') 
        else:
            logging.warning(f'{date}-User failed when creating an account. Error: [{x}].')
            mb.showwarning('Info', 'Something went wrong [Account already exist].') 

        
def deleteAccount(usrId, user, pas):
    db.deleteRecord(usrId)
    logging.info(f'{date}-Account deleted [Username:{user}|Password:{pas}].')


def updateInfo(usrId, username, password):
    db.updateData(usrId, username, password)
    logging.info(f'{date}-Account was updated [Username:{username}|Password:{password}].')
