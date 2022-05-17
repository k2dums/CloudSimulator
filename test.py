# import threading
# import time


# ans=[]
# def fun1(name,delay):
#     for i in range(6):
#         print(ans,time.time())
#         time.sleep(delay)
# def fun2(name,delay):
#     for i in range(6):
#         ans.append(i)
#         time.sleep(1)
# t1=threading.Thread(target=fun1,args=('Norbu',1))
# t2=threading.Thread(target=fun2,args=('Diks',1.4))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print('Done')

from Network import Network
from Broker import Broker
network=Network()
network.dummyNetwork()
broker=Broker(network)
broker.ga_vs_lot()
