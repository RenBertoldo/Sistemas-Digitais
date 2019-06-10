import mraa
import socket
import time
import threading
from datetime import datetime

#ENTRADAS E SAIDAS
CardiacSensor = mraa.Aio(2)
LedPWM = mraa.Gpio(3)
SpeakerPWM = mraa.Gpio(2)


LedPWM.dir(mraa.DIR_OUT)
SpeakerPWM.dir(mraa.DIR_OUT)

bit1 = mraa.Gpio(4)      #Porta IO4
bit1.dir(mraa.DIR_OUT)          
bit2 = mraa.Gpio(6)      #Porta IO6
bit2.dir(mraa.DIR_OUT)
bit3 = mraa.Gpio(7)      #Porta IO7
bit3.dir(mraa.DIR_OUT)
bit4 = mraa.Gpio(8)      #Porta IO8
bit4.dir(mraa.DIR_OUT)
bit5 = mraa.Gpio(9)      #Porta IO9
bit5.dir(mraa.DIR_OUT)
bit6 = mraa.Gpio(10)      #Porta I10
bit6.dir(mraa.DIR_OUT)
bit7 = mraa.Gpio(11)      #Porta I11
bit7.dir(mraa.DIR_OUT)
bit8 = mraa.Gpio(12)      #Porta I12
bit8.dir(mraa.DIR_OUT)


history= []
envia = False
Liga = True
adc = 0.0
max_history = 250


    
heatBeats = 0

def send():
        global adc

        while Liga:
                binary = [int(x) for x in '{:010b}'.format(adc)]

                print "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"
                print binary

                #bit10.write(binary[0])
                #bit9.write(binary[1])
                bit8.write(binary[7])
                bit7.write(binary[6])
                bit6.write(binary[5])
                bit5.write(binary[4])
                bit4.write(binary[3])
                bit3.write(binary[2])
                bit2.write(binary[1])
                bit1.write(binary[0])

                time.sleep(1)

def heatBeat():
        global heatBeats
        
        initial_time = time.time()
        while Liga:

                time.sleep(1)
                delta = time.time() - initial_time

                bpm = round((heatBeats) * (60/delta)) 
                print ("BPM: ",bpm,"Tempo de medicao: ",round(delta),"Contagem de batimentos: ",heatBeats)

                if delta >= 60:
                        heatBeats = 0
                        initial_time = time.time()
                        
                        
                        
                


def ReadAdc():
    global adc,Liga,history,max_history,heatBeats
    
    Up = False

    while Liga:
        
        adc = CardiacSensor.read()

        history.append(adc)
        history = history[-max_history:]

        minima,maxima = min(history),max(history)

        thressholdon = (minima + maxima * 3)//4
        thressholdoff = (minima + maxima)// 2



        if adc > thressholdon :
                Up = True
                
        
        if adc < thressholdoff:

                if Up == True:
                        Up = False
                        heatBeats = heatBeats + 1
                        LedPWM.write(1)
                        SpeakerPWM.write(1)
                else:
                        LedPWM.write(0)
                        SpeakerPWM.write(0)


        

        time.sleep(0.002)
        



    
try:
    ThreadADC = threading.Thread(target = ReadAdc)
    ThreadBPM = threading.Thread(target = heatBeat)
    ThreadSend = threading.Thread(target = send)
    
    ThreadADC.start()
    ThreadSend.start()
    #ThreadBPM.start()

except :
        print "Nao funcionou"
