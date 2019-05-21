import mraa
import socket
import time
import threading
from datetime import datetime

#ENTRADAS E SAIDAS
CardiacSensor = mraa.Aio(0)
LedPWM = mraa.Pwm(3)
LedPWM.period_us(100)
LedPWM.enable(True)

ListADC = []
envia = False

#Rebimento de dados
def Sender():
    global ListADC
    HOST = '192.168.1.10'  # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    while Liga:
        if envia:
            msg = ListADC[-1]
            udp.sendto (msg, dest)
            envia = False
    udp.close()

def ReadAdc():
    global adc,Liga,ListADC,envia
    while Liga:
        adc = CardiacSensor.readFloat()
        ListADC.extend(adc)
        print("Valor do ADC: ",adc,"\n")
        envia = True
        

def WritePWM():
    global adc,Liga
    while Liga:
        LedPWM.write(adc)
        print("Valor escrito no PWM: ")
        print(adc,"\n")

#count usa tempo em Microsegundos
def conta():
    global Liga
    tempoInicial = datetime.now()
    tempoAtual = 0
    Period = 60 #microsecond
    while True :
        tempoAtual = datetime.now()
        if (tempoInicial.minute-tempoAtual.minute < 1 ):
            Liga = True
        else :
            tempoInicial = datetime.now()
            Liga = False
        else:
                pass

    
def main():
    
    ThreadCount = threading.Thread(target = conta)
    ThreadPWM = threading.Thread(target = WritePWM)
    ThreadADC = threading.Thread(target = ReadAdc)
    ThreadSend = threading.Thread(target = Send)
    
    ThreadADC.start()
    ThreadPWM.start()
    ThreadCount.start()
    ThreadSend.start()

    ThreadADC.join()
    ThreadPWM.join()
    ThreadCount.join()
    ThreadSend.join()

if __name__ == '__main__':
    main()    
