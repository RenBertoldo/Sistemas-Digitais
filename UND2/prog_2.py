import mraa
import socket
import time
import threading
from datetime import datetime

#ENTRADAS E SAIDAS
CardiacSensor = mraa.Aio(0)
LedPWM = mraa.Pwm(3)
LedPWM.period_ms(2)
LedPWM.enable(True)

ButtonPin = mraa.Gpio(23)
ButtonPin.dir(mraa.DIR_IN)
LedPin = mraa.Gpio(24)
LedPin.dir(mraa.DIR_OUT)


ListADC = []
envia = False
Liga = False
adc = 0.0
maxValue = 0.0

#Rebimento de dados
def Sender():
    global ListADC, Liga,envia
    HOST = '10.13.113.237'  # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    while Liga:
        if envia:
            msg = ListADC[-1]
            udp.sendto (msg, dest)
            print (msg,"\n")
            envia = False
    udp.close()

def ReadAdc():
    global adc,Liga,ListADC,envia,maxValue
    while Liga:
        adc = CardiacSensor.readFloat()*10

        if adc > maxValue :
                maxValue = adc
        

        adc = maxValue - adc
        #ListADC.extend(adc)
        #print("Valor do ADC: ",adc,"\n")
        envia = True
        LedPWM.write(adc)
        #print("Valor escrito no PWM: ")
        #print(adc,"\n")
        print adc
        time.sleep(0.0002)
        

def Button():
    global Liga
    while True:
        if(ButtonPin.read()!=0):
            continue
        else:
            time.sleep(0.05)
            if(ButtonPin.read()==1):
               if(Liga == True):
                    Liga = False
                    LedPin.write(0)
                else:
                    Liga = True
                    LedPin.write(1)
            else:
                continue    
#count usa tempo em Microsegundos
def conta():
    global Liga
    tempoInicial = datetime.now()
    tempoAtual = datetime.now()
    Period = 60 #microsecond
    while True :
        tempoAtual = datetime.now()
        if (tempoInicial.minute-tempoAtual.minute < 1 ):
            Liga = True
        else :
            tempoInicial = datetime.now()
            Liga = False
    
try:
    
    ThreadCount = threading.Thread(target = conta)
    ThreadButton = threading.Thread(target = Button)
    ThreadADC = threading.Thread(target = ReadAdc)
    ThreadSend = threading.Thread(target = Sender)
    
    ThreadADC.start()
    ThreadButton.start()
    ThreadCount.start()
    ThreadSend.start()

    #ThreadADC.join()
    #ThreadPWM.join()
    #ThreadCount.join()
    #ThreadSend.join()

except :
        print "Nao funcionou"
