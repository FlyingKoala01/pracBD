import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import interface
# import input_manager
import database

def main(*args):
    database.check_db()
    interface.start_up()

if __name__ == '__main__':
    main()




