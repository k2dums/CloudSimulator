import pandas as pd
import Graph
import matplotlib.pyplot as plt
import sys

if not(sys.argv):
    print("[Error]: No file given")
    sys.exit()
try :
    df=pd.read_excel(f"{sys.argv[1]}.xls")
    df=pd.DataFrame(df)
except Exception as er:
    print (er)
    print("[Error] No such file")
    sys.exit()
df.insert(0,'Iteration',range(1,1+len(df)))
print(type(df))
df.boxplot(by="Iteration")
plt.show()
df.drop('Iteration', inplace=True, axis=1)
bplot=df.plot(kind='box')
bplot.set_ylabel("time(Seconds)")
plt.show()




# names=[]
# values=[]
# for col in df:
#     names.append(col)
#     values.append(df[col].mean())
# Graph.Graph.plotBarGraph(names,values)
