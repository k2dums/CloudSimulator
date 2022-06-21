import pandas as pd
import Graph
import matplotlib.pyplot as plt


df=pd.read_excel("values.xls")
bplot=df.boxplot()
bplot.set_ylabel('time (s)')
plt.show()

names=[]
values=[]
for col in df:
    names.append(col)
    values.append(df[col].mean())
Graph.Graph.plotBarGraph(names,values)
