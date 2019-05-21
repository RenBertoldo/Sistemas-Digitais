import threading
import matplotlib.pypol as plt
import matplotlib.animation as animation
from matplotlib import style
import socket

ListADC = []

def ServerConnect():
    global ListADC
    HOST = ''              # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (HOST, PORT)
    udp.bind(orig)
    while True:
        msg, cliente = udp.recvfrom(1024)
        ListADC.extend(float(msg))
        
    udp.close()

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global ListADC
    graph_data = recived
    lines = graph_data.split('\n')
    ys = []
    while(True):
        ys.append(ListADC[-1])


    ax1.clear()
    ax1.plot(ys)

thread1 = threading.Thread(target=ServerConnect)
thread1.start()


ani= animation.FuncAnimation(fig, animate,interval=100)
plt.show()

