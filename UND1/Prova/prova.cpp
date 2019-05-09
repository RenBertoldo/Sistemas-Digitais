/*  
    Centro de Tecnologia
    Graduacao em Engenharia de Computacao
    Sistemas Digitais - Prof. Sergio Natan Silva
    Aluno: Renan Lucas Ribeiro Bertoldo

    O código asseguir possui como referencias
    utilizando o MC ATMEGA328p (Arduino UNO)
    No arduino a pinagem com os seus respectivos sao
    (D1)FAN = OCR1A = PB1
    (D2)RESISTOR = OCR2A = PB3
    Sensor de Temperatura(A1) = ADC0 = PC0
    Sensor de Temperatura(A2) = ADC2 = PC2
    Sensor de Umidade = ADC4 = PC4
    Chave(HiZ) = PB0
    (L1)LED = PD3
    (L2)LED = PD4
    (L3)LED = PD5

    A partir do Arduino UNO com Frenquencia de 16MHZ
    O tempo de contagem foi usado um prescale de 1/1024 - TIMER0
    com um periodo de 16,3 ms. 
    Foram usados para os PWMs o modo PWM 10bits (modo 7) sem inversao
    Foram usados para os PWMs o prescale de 1/256 resultando 62,5kHz de frequencia
    Nos ADCs foram usados um prescale de 1/128 e Utiliza VCC como referencia
    Os ADCs usam a resolução padrao de 10bits (ADLAR = 0)
*/
#include <avr/io.h>
#include <inttypes.h>
#include <avr/interrupt.h>

volatile uint8_t cont = 0;
volatile bool conv = false;

ISR(TIMER0_OVF_vect)
{
  cont++;
  if(cont == 31){ // A cada 0,5s habilita a conversão
    conv = true;
    cont = 0;
  }
}

int main(){

    uint16_t ADCTempIN = 0,ADCUmi = 0,ADCTempOUT = 0;
    
    // valores iniciais dos sinais PWM
    OCR1A = 0; // FAN
    OCR2A = 0; // RESISTOR
    
    // configuracao dos PWMs

    //  FAST PWM 10 bits (Modo 7) sem invers�o
    
    // PWM do FAN
    // Scale 1/256 CSx2 CSx1 62,5kHz
    TCCR1A = _BV(COM1A1) | _BV(WGM10) | _BV(WGM11);
    TCCR1B = _BV(CS12) |_BV(CS11) | _BV(WGM12);
    
    // PWM do Resistor
    // Scale 1/256 CSx2 CSx1 62,5kHz
    TCCR2A = _BV(COM2A1) | _BV(WGM20) | _BV(WGM21);
    TCCR1B = _BV(CS22) | _BV(CS21) | _BV(WGM22);

    // CONTA COM O CONTADOR 0
    TCCR0A |= 0x00;//_BV(WGM01)|_BV(WGM00);
	TCCR0B |= _BV(CS02) | _BV(CS00);;  // 1/1024 prescale
	TIMSK0 |= _BV(TOIE0);   // Enable timer0 overflow interrupt(TOIE0)
    sei();//Habilita interrupção 

    // PB1/OC1A e PB3/OC2A como saida
    DDRB |= _BV(PORTB1)|_BV(PORTB3);
    
    //Configuracao do AD
    ADMUX  |= _BV(REFS0); //Utiliza VCC como referência 
    ADCSRA |= _BV(ADEN)|_BV(ADPS2)|_BV(ADPS1)|_BV(ADPS0);  //Habilita o AD e utiliza prescale selection de 128
    // VAI USAR ADC0 para TempIN, ADC2 para TempOUT e ADC4 para Umidade

    //Configuracao de botao
    DDRB &= 0b11111110; // PINO PB0 como entrada
    PORTB |= 0x00; // HiZ

    //Configuracao de LEDS
    DDRD |= _BV(PORTD3) | _BV(PORTD4) | _BV(PORTD5); //PD3,PD4,PD5 como saida
    PORTD &= 0x00; // Mantem tudo apagado

    while(1){
        // Quando habilitado, faz as conversoes, depois que acabar desabilita e espera
        // o contador para poder fazer as conversoes novamente.
        if(conv == true){
            
            ADMUX &= 0b01000000;
            ADCSRA |= _BV(ADSC); 
            while(!(ADCSRA & 0x10)); 
            ADCTempIN = ADC;
            
            ADMUX &= 0b01000010;
            ADCSRA |= _BV(ADSC); 
            while(!(ADCSRA & 0x10)); 
            ADCTempOUT = ADC;

            ADMUX &= 0b01000100;
            ADCSRA |= _BV(ADSC); 
            while(!(ADCSRA & 0x10)); 
            ADCUmi = ADC;
            
            conv = false;
        }
        // quando habilitado o botao
        if(PINB & 0x01){
            // se for menor que 20 graus ele
            if(ADCTempIN<(0.1*1024)){
                PORTD &= 0b00001000; //ACENDE LED1 (L1)
                OCR1A = 0;
                OCR2A = 0;
            }
            if(ADCTempOUT > (0.6*1024)){
                PORTD &= 0b00010000; // ACENDE LED2 (L2)
                OCR1A = 0;
                OCR2A = 0;
            }else{
                PORTD &= 0b00100000; //ACENDE LED3 (L3)
                if(ADCUmi == 1024){
                    OCR1A = (0.25*1023); //Q(t) 25
                    OCR2A = 1023; //P(t) 100
                }
                else if(ADCUmi < 1024){
                    OCR1A = (0.5*1023); //Q(t) 50%
                    OCR2A = (0.5*1023); //P(t) 50%
                }else if((ADCUmi < (0.5*1024))){
                    OCR1A = 1023; // Q(t) 100%
                    OCR2A = (0.25*1023); //P(t) 25%
                }else if((ADCUmi < (0.25*1024))){
                    OCR1A = 0;
                    OCR2A = 0;
                    PORTD &= 0x00;
                }
            }
        }
        PORTD = 0x00;
    }
}