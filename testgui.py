# from Network import Network
# from Broker import Broker
# from Task import Task
# from TaskGenerator import TaskGenerator

# network=Network()
# network.createAndLayerSpecs()
# #NO of task generated is 30
# broker=Broker(network)
# broker.dynamicSimulation()

import tkinter as tk
import os
import sys
import subprocess
from Network import Network
# --- functions ---

def test():
    print("Hello World")
    p = subprocess.run("ping -c 4 stackoverflow.com", shell=True, stdout=subprocess.PIPE)
    print(p.stdout.decode())
    
# --- classes ---

class Redirect():
    
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        #self.widget.see('end') # autoscroll

    #def flush(self):
    #    pass
    
# --- main ---    
   
root = tk.Tk()
network=Network()

text = tk.Text(root)
text.pack()

button = tk.Button(root, text='TEST', command=network.createAndLayerSpecs)
button.pack()

old_stdout = sys.stdout    
sys.stdout = Redirect(text)

root.mainloop()

sys.stdout = old_stdout