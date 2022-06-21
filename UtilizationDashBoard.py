
import tkinter.ttk
import tkinter as tk
import time
import sys

from numpy import pad

from Network import Network,Layer
from Broker import Broker,Algorithm
from Task import Task
from Graph import Graph
from TaskGenerator import TaskGenerator
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


class DisplayLabel():
    def __init__(self,widget) -> None:
        self.widget=widget

    def write(self,text):
        self.widget.insert('end',text)
    def flush(self):
        pass


def createProgressBar(window):
    bar=tkinter.ttk.Progressbar(window,orient='horizontal')
    return bar
def createLabel(window,textis):
    label=tk.Label(window,text=textis,background=__background_color,foreground=__button_text_color)
    return label
def addtoUtilization(cluster,progress,devices,rowis):
    if rowis==0:
        cluster.grid(row=rowis+1,column=0,pady=(20,20),padx=(0,10))
        progress.grid(row=rowis+1,column=1,pady=(20,20),padx=(0,10))
        devices.grid(row=rowis+1,column=2,pady=(20,20))
        return
    cluster.grid(row=rowis+1,column=0,pady=(0,20),padx=(0,10))
    progress.grid(row=rowis+1,column=1,pady=(0,20),padx=(0,10))
    devices.grid(row=rowis+1,column=2,pady=(0,20))
    
def createNetwork():
    network.dummyNetwork()
    print("[SUCCESS] Created Network ")
 
 
def quitSimulation():
    global root
    root.quit()


def showNetwork():
    pass

def showUtilization():
    if not(network.getNetworkLayers()):
        return
    layer0=network.getNetworkLayers()[0]
    assert isinstance(layer0,Layer)
    clusters=layer0.getClusters()
    for cluster in clusters:
        cluster_label=createLabel(utilzation_progress_frame,"Cluster "+str(cluster.getId()))
        pb=createProgressBar(utilzation_progress_frame)
        activedevice=cluster.getActiveDeviceNo()
        totaldevice=cluster.getNoOfDevice()
        active_text=str(activedevice)+"/"+str(totaldevice)
        activity_label=createLabel(utilzation_progress_frame,active_text)
        clusterProgress.append(pb)
        clusterLabelActive.append(activity_label)
        addtoUtilization(cluster_label,pb,activity_label,cluster.getId())

def updateUtilzationBar():
    while  True:
        layer0=network.getNetworkLayers()[0]
        assert isinstance(layer0,Layer)
        clusters=layer0.getClusters()
        for cluster in clusters:
            activedevice=cluster.getActiveDeviceNo()
            totaldevice=cluster.getNoOfDevice()
            active_text=str(activedevice)+"/"+str(totaldevice)
            clusterLabelActive[cluster.getId()].configure(text=active_text)
            pb=clusterProgress[cluster.getId()]
            assert isinstance(pb,tkinter.ttk.Progressbar)
            # print(int(activedevice/totaldevice*100))
            pb['value']=activedevice/totaldevice*100
            # print(active_text)
        root.update_idletasks()
        time.sleep(1)

def startSimulation():
    #Here
    broker=Broker(network)
    tasks=TaskGenerator.randomTasksgenerator(10)
    broker.setResourceList(tasks)
    broker.resourceAllocationAlgorithmStatic(Algorithm._RandomAllocation)
    # broker.startDynamicSimuation()
    showUtilization()
    t1=Thread(target=broker.startSimulation,args=(result,))
    t2=Thread(target=updateUtilzationBar)
    t2.start()
    t1.start()
    #till
    # taskgiven=TaskGenerator.generatenoTask(30)
    # broker.setResourceList(taskgiven)
    # print("Starting Simualation")
    # t1=Thread(target=broker.resourceAllocationAlgorithmStatic,args=(Algorithm._WeightedRoundRobin,))
    # t2=Thread(target=updateUtilzationBar)
    # t1.start()
    # t2.start()


def showBarGraph():
    fig=Figure(figsize = (5.2, 4.7), dpi = 100)
    if not(result):
        print("[Error] result  has no value")
        return
    title="Time taken for different Algorithms"
    xlabel="Algorithms"
    ylabel="Time Taken"
    plot1=fig.add_subplot(111)
    plot1.bar(alogNames,result,color='blue',width=0.1)
    plot1.set_xlabel(xlabel)
    plot1.set_ylabel(ylabel)
    plot1.title.set_text(title)
    plt.show()
  
    canvas=FigureCanvasTkAgg(fig,master=graphFrame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,graphFrame)
    toolbar.update()
    canvas.get_tk_widget().pack()
  
    
    



#General Configurations of the window
__background_color="#202124"
__background_f_color="#171717"
__button_color="#303134"
__button_text_color="white"
root=tk.Tk()
network=Network()
root.geometry("800x600")
root.resizable(width=False,height=False)
root.configure(bg=__background_color)
strvar=tk.StringVar()
strvar.set(">")
clusterProgress=[]
clusterLabelActive=[]

#Defining the Frames
topFrame=tk.Frame(root,bg=__background_color,width=800,height=500)
# middleFrame=tk.Frame(root,bg='yellow',width=800,height=130,padx=40)
bottomFrame=tk.Frame(root,width=800,bg=__background_f_color,height=100,padx=10)
topFrame.pack_propagate(0)
bottomFrame.pack_propagate(0)


utilzationFrame=tk.Frame(topFrame,bg=__background_color,width=250,height=500)
utilizaiton_lbl_frame=tk.Frame(utilzationFrame,bg=__background_color,height=20,width=40)
utilzation_progress_frame=tk.Frame(utilzationFrame,bg=__background_color,height=500,width=250)
graphFrame=tk.Frame(topFrame,bg="Grey",width=550,height=500)
utilzationFrame.grid_propagate(0)
utilizaiton_lbl_frame.grid_propagate(0)
utilzation_progress_frame.grid_propagate(0)
graphFrame.pack_propagate(0)



#Adding the widgets 
utilization_lbl=tk.Label(
    utilizaiton_lbl_frame,
    text="Utilization",
    font=('Arial', 13),
    background=__background_color,
    foreground=__button_text_color,
    width=10
)
    
listbox=tk.Listbox(
    utilzationFrame,
)

bar_btn=tk.Button(
    bottomFrame,
    text=" Bar Graph",
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,
    command=showBarGraph


)

line_btn=tk.Button(
    bottomFrame,
    text=" Line Graph",
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,
)

createNetwork_btn=tk.Button(
    bottomFrame,
    text="Create Network",
    command=createNetwork,
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,
    highlightcolor='red'

)

quit_btn=tk.Button(
    bottomFrame,
    text="QUIT ",
    command=quitSimulation,
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,

)

show_network_btn=tk.Button(
    bottomFrame,
    text="Show Network",
    command=showNetwork,
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,

)

simulation_btn=tk.Button(
    bottomFrame,
    text="Start Simulation",
    command=startSimulation,
    font=('Arial', 11),
    background=__button_color,
    activebackground=__background_color,
    foreground=__button_text_color,
    activeforeground=__button_text_color,

)




# display_label=tk.text(
#     middleFrame,
#     font=('Arial', 18),
#     height=1,
# )

# input_label=tk.Entry(
#     middleFrame,
#     text='Input',
#     font=('Arial', 18)
# )






#TopFrame 
topFrame.pack()
# topFrame.rowconfigure(0,weight=1)
utilzationFrame.pack(side=tk.LEFT,padx=20)
graphFrame.pack(side=tk.LEFT)
utilzationFrame.grid_columnconfigure(0, weight=1)
utilizaiton_lbl_frame.pack()
utilzation_progress_frame.pack()
# utilization_lbl.grid(row=0,column=0,pady=20,)
utilization_lbl.pack()


#BottomFrame
bottomFrame.pack()
bar_btn.pack(side='left',padx=(0,20))
line_btn.pack(side="left",padx=(0,20))
createNetwork_btn.pack(side='left',padx=(0,20))
quit_btn.pack(side='left',padx=(0,20))
show_network_btn.pack(side="left",padx=(0,20))
simulation_btn.pack(side='left',padx=(0,20))
result=[]
alogNames=["RandomAllocation"]


#Start the network simulation
broker=Broker(network)

root.mainloop()




