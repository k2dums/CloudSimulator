
import tkinter.ttk
import tkinter as tk
import time
import sys

from Network import Network,Layer
from Broker import Broker,Algorithm
from Task import Task
from Graph import Graph
from TaskGenerator import TaskGenerator
from threading import Thread

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
    # network.createAndLayerSpecs()
    network.dummyNetwork()
 
 
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


def showNetwork():
    pass

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
    tasks=TaskGenerator.generatenoTask(20)
    broker.setResourceList(tasks)
    broker.resourceAllocationAlgorithmStatic(Algorithm._WeightedRoundRobin)
    # broker.startDynamicSimuation()
    showUtilization()
    t1=Thread(target=broker.startDynamicSimuation)
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
    pass
    



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
# middleFrame.pack_propagate(0)
bottomFrame.pack_propagate(0)

utilzationFrame=tk.Frame(topFrame,bg=__background_color,width=200,height=500)
utilizaiton_lbl_frame=tk.Frame(utilzationFrame,bg=__background_color,height=50,width=200)
utilzation_progress_frame=tk.Frame(utilzationFrame,bg=__background_color,height=450,width=200)
graphFrame=tk.Frame(topFrame,bg=__background_color,width=600,height=500)
utilzationFrame.grid_propagate(0)
utilizaiton_lbl_frame.grid_propagate(0)
utilzation_progress_frame.grid_propagate(0)
graphFrame.pack_propagate(0)



#Adding the widgets 
utilization_lbl=tk.Label(
    utilzationFrame,
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

utilzation_btn=tk.Button(
    bottomFrame,
    text="Show Utilization",
    command=showUtilization,
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
utilzationFrame.pack(side=tk.LEFT,padx=40)
utilzationFrame.grid_columnconfigure(0, weight=1)
utilizaiton_lbl_frame.pack()
utilzation_progress_frame.pack()
utilization_lbl.grid(row=0,column=0,pady=20,)
# listbox.pack(expand=True,fill="both")
# utilzationFrame.rowconfigure(0,weight=1)
graphFrame.pack(side=tk.LEFT)
fig=Figure(figsize = (5, 3), dpi = 100)
y = [i**2 for i in range(101)]
plot1=fig.add_subplot(111)
plot1.plot(y)
canvas=FigureCanvasTkAgg(fig,master=graphFrame)
canvas.draw()
canvas.get_tk_widget().pack(expand=True,fill='both')
toolbar=NavigationToolbar2Tk(canvas,graphFrame)



#MiddleFrame
# middleFrame.pack()
# display_label.pack(pady=(20,5),fill='x')
# input_label.pack(fill='x')
# old_stdout=sys.stdout
# sys.stdout=DisplayLabel(display_label)

#BottomFrame
bottomFrame.pack()
bar_btn.pack(side='left',padx=(0,20))
line_btn.pack(side="left",padx=(0,20))
createNetwork_btn.pack(side='left',padx=(0,20))
utilzation_btn.pack(side='left',padx=(0,20))
show_network_btn.pack(side="left",padx=(0,20))
simulation_btn.pack(side='left',padx=(0,20))




#Start the network simulation
broker=Broker(network)

root.mainloop()




