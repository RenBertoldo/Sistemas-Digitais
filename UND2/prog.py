import mraa
import socket
import time
from threading import Thread
from datetime import datetime

#ENTRADAS E SAIDAS
CardiacSensor = mraa.Aio(0)
LedPWM = mraa.Pwm(3)
LedPWM.period_ms(2)
LedPWM.enable(True)

ListADC = []
envia = False
Liga = True
adc = 0.0

#Rebimento de dados
def Sender():
    print("Sender iniciado")
    global ListADC, Liga,envia
    HOST = '10.13.110.92'  # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    while Liga:
        if envia:
            msg = str(ListADC[-1])
            udp.sendto (msg, dest)
            #print("valor enviado",msg,"\n")
            envia = False
    udp.close()

def ReadAdc():
    global adc,Liga,ListADC,envia
    print("Lendo ADC")
    while Liga:
        adc = CardiacSensor.readFloat()
        ListADC.append(adc)
        LedPWM.write(adc)
        #print("Valor do ADC: ",ListADC[-1],"\n")
        envia = True
        

def WritePWM():
    global adc,Liga
    print ("Rodando PWM")
    while Liga:
        LedPWM.write(adc)
        print("Valor escrito no PWM: ",adc,"\n")


#count usa tempo em Microsegundos
def conta():
    global Liga
    print ("Contando")
    tempoInicial = datetime.now()
    tempoAtual = datetime.now()
    while True :
        tempoAtual = datetime.now()
        if (tempoInicial.minute-tempoAtual.minute < 40 ):
            Liga = True
        elif (tempoInicial.minute-tempoAtual.minute == 100 ) :
            tempoInicial = datetime.now()
            Liga = False
    
try:
    
    ThreadCount = Thread(target = conta)
    ThreadPWM = Thread(target = WritePWM)
    ThreadADC = Thread(target = ReadAdc)
    ThreadSend = Thread(target = Sender)
    print ("Criaram as Threads\n")
    ThreadCount.start()
    ThreadADC.start()
    ThreadPWM.start()
    ThreadSend.start()
    print ("As threads startaram")
    #ThreadADC.join()
    #ThreadPWM.join()
    #ThreadCount.join()
    #ThreadSend.join()
    #print ("As threads deram Join")
except :
        print "Nao funcionou"
