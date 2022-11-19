from tkinter import *
from PIL import ImageTk, Image
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..',)
sys.path.append( mymodule_dir)
import Client
