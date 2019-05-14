import mraa
import socket
import time
import Threa
#Interrupcao
interrupt = False
#ENTRADAS E SAíDAS
CardiacSensor = mraa.Aio(0)
LedPWM = mraa.pwm(3)
LedPWM.period_us(700)
LedPWM.enable(True)

HOST = '10.13.100.146'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
tcp.bind(orig)
#tcp.listen(1)
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data




def main():
    
    x = mraa.Aio(0)

    adc = x.read()

