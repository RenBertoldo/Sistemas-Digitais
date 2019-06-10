import mraa
import socket
import time
import threading
from datetime import datetime

#ENTRADAS E SAIDAS

#--------------------------------------------------------------------------
#   Objeto                   | Porta fisica
#--------------------------------------------------------------------------

# Sensor
CardiacSensor = mraa.Aio(2)#-----Porta A2

# Botao
BtOnOff = mraa.Aio(0)#-----------Porta A2

# Saida para o Led
LedPWM = mraa.Gpio(3)#-----------Porta IO3
LedPWM.dir(mraa.DIR_OUT)

# Saida para o speaker
SpeakerPWM = mraa.Gpio(2)#-------Porta IO2
SpeakerPWM.dir(mraa.DIR_OUT)


# Saida de dados para FPGA
bit1 = mraa.Gpio(4)#-------------Porta IO4
bit1.dir(mraa.DIR_OUT)          
bit2 = mraa.Gpio(5)#-------------Porta IO5
bit2.dir(mraa.DIR_OUT)
bit3 = mraa.Gpio(6)#-------------Porta IO6
bit3.dir(mraa.DIR_OUT)
bit4 = mraa.Gpio(7)#-------------Porta IO7
bit4.dir(mraa.DIR_OUT)
bit5 = mraa.Gpio(8)#-------------Porta IO8
bit5.dir(mraa.DIR_OUT)
bit6 = mraa.Gpio(9)#-------------Porta IO9
bit6.dir(mraa.DIR_OUT)
bit7 = mraa.Gpio(10)#------------Porta IO10
bit7.dir(mraa.DIR_OUT)
bit8 = mraa.Gpio(11)#------------Porta IO11
bit8.dir(mraa.DIR_OUT)
bit9 = mraa.Gpio(12)#------------Porta IO12
bit9.dir(mraa.DIR_OUT)
bit10 = mraa.Gpio(13)#-----------Porta IO12
bit10.dir(mraa.DIR_OUT)


# VARIAVEIS

#--------------------------------------------------------------------------
# Nome              | Funcao 
#--------------------------------------------------------------------------

history= []#------------- Armazenar os valores medidos no ADC    
max_history = 250 #------ Limitar o numero maximo de valores armazenados no historico

envia = False #---------- Habilita o envio de dados para a FPGA 
Liga = False #------------ Habilita o funcionamento do sistema

adc = 0.0  #------------- Armazena o valor medido no sensor
heatBeats = 0 #---------- Armazena a contagem de batimentos cardiacos


# Envia os dados para a FPGA
def send():
        global Liga,adc


        while True:

                while Liga:
                        
                        try:
                                # Convertendo o valor do adc para um vetor binario de 10 bits
                
                                binary = [int(x) for x in '{:010b}'.format(adc)]

                                # Associando o valor de cada bit a um dos pinos
                                # do menos para o mais significativo.

                                bit10.write(binary[9])
                                bit9.write(binary[8])
                                bit8.write(binary[7])
                                bit7.write(binary[6])
                                bit6.write(binary[5])
                                bit5.write(binary[4])
                                bit4.write(binary[3])
                                bit3.write(binary[2])
                                bit2.write(binary[1])
                                bit1.write(binary[0])

                                # Limitando a transmicao a frequencia de Nyquest.
                                time.sleep(0.002)
                        except:
                                c = 0

# Mede os batimentos cardiacos
def heatBeat():
        global Liga,heatBeats,delta
        
        while True:
                initial_time = time.time()

                while Liga:

                        # Aguarda 1 segundo entre cada exibicao
                        time.sleep(1)

                        # Afere o intervalo de tempo desde a ultima medicao
                        delta = time.time() - initial_time

                        # Para uma medicao mais precisa, aguarda-se 10 segundos para comecar
                        if delta >= 10:
                                bpm = round((heatBeats) * (60/delta)) 

                                if Liga == True:
                                        print ("BPM: ",bpm,"Tempo de medicao: ",round(delta),"Contagem de batimentos: ",heatBeats)

                        # Apos 1 minuto, reinicia a medicao
                        if delta >= 60:
                                heatBeats = 0
                                initial_time = time.time()

                heatBeats = 0
                        
                        
                        
# Leitura do Sensor
def ReadAdc():
        global adc,Liga,history,max_history,heatBeats
    
        Up = False # Armazena a subida de um batimento de modo a evitar medicoes redundantes

        while True:
                while Liga:
        
                        # Leitura do sensor
                        adc = CardiacSensor.read()

                        # Insere valor medido no vetor de historico
                        history.append(adc)

                        # Limita o tamanho do historico
                        history = history[-max_history:]

                        # Determinacao dos valores de picos e minimos do historico
                        minima,maxima = min(history),max(history)

                        # Determinacao de valores de pico e minimo da pulsacao
                        thressholdon = (minima + maxima * 3)//4
                        thressholdoff = (minima + maxima)// 2

                        # Percebe uma subida do batimento
                        if adc > thressholdon :
                                Up = True
                
                        # Percebe uma descida do batimento
                        if adc < thressholdoff:

                                # Tendo agora uma descida na medicao apos uma subida anterior
                                if Up == True:
                                        # Desativa flag de subida
                                        Up = False

                                        # Incrementa o contador de batidas
                                        heatBeats = heatBeats + 1

                                        # Ascende o led e manda um pulso para o speaker
                                        LedPWM.write(1)
                                        SpeakerPWM.write(1)

                                # Sendo um movimento de descida da batida nao precedida por uma subida
                                else:
                                       # Desativa o led e o speaker
                                        LedPWM.write(0)
                                        SpeakerPWM.write(0)


        
                                
                        # Limita o funcionamento a frequencia de Nyquest
                        time.sleep(0.002)
        


# Gerenciamento do botao
def ButtonOnOff():
    global Liga
    print "\n----------------------------------------------------------------\n\n\n       QUARTETO FANTASTICO EQUIPAMENTOS HOSPITALARES \n\n\n----------------------------------------------------------------\n\n\n"

    print "INSTRUCOES\n - Coloque o dispositivo de medicao no dedo indicador\n - Precione o botao por 1 segundo para ligar ou desligar o sistema."
    while True:
                
                if(round(BtOnOff.readFloat())==0):
                        continue

                else:
                        time.sleep(1)
                        if round(BtOnOff.readFloat())==1:
                           
                                if Liga == True:
                                        Liga = False

                                        LedPWM.write(1)
                                        time.sleep(0.5)
                                        LedPWM.write(0)
                                        time.sleep(0.5)
                                        LedPWM.write(1)
                                        time.sleep(0.5)
                                        LedPWM.write(0)

                                        # Desliga saidas
                                        bit10.write(0)
                                        bit9.write(0)
                                        bit8.write(0)
                                        bit7.write(0)
                                        bit6.write(0)
                                        bit5.write(0)
                                        bit4.write(0)
                                        bit3.write(0)
                                        bit2.write(0)
                                        bit1.write(0)
                                        LedPWM.write(0)
                                        SpeakerPWM.write(0)


                                        print "\nSistema OFF"

                                else:

                                        LedPWM.write(1)
                                        time.sleep(0.5)
                                        LedPWM.write(0)
                                        time.sleep(0.5)
                                        LedPWM.write(1)
                                        time.sleep(0.5)
                                        LedPWM.write(0)

                                        Liga = True
                                        print "\nSistema ON"
                                        print "Calculando. Por favor, aguarde."
                       
                        else:
                                continue   

# Inicialisa as Threads
try:
    ThreadADC = threading.Thread(target = ReadAdc)
    ThreadBPM = threading.Thread(target = heatBeat)
    ThreadSend = threading.Thread(target = send)
    ThreadReadBTonOff= threading.Thread(target = ButtonOnOff)
    
    ThreadADC.start()
    ThreadSend.start()
    ThreadBPM.start()
    ThreadReadBTonOff.start()

except :
        print "Nao funcionou"
