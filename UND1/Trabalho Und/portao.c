#include <avr/io.h>
#include <inttypes.h>
#include <avr/interrupt.h>

// CONTADOR PARA CONTROLE DO PORTÃO

// SETAR PWM 0 ~ 1023
// PINOS PB1/PWM(LED_AMARELO) PC0/ADC PB0/BOTAO PC4/LED
volatile uint8_t timeSec = 2;
volatile uint8_t dif = 0;
volatile uint8_t 
int TempoInicial1,TempoInicial2,TempoInicial3;
bool ligar = false;
bool aberto = false,parado = false,fechado = true;
volatile uint8_t x = 0;
volatile uint8_t seg = 0;

ISR(TIMER0_OVF_vect)
{
  x++;
  if(x == 61){
    seg++;
    x=0; 
  }
  
}


int main()
{
    bool flag1=false,flag2=false;
    bool abrir = false,parar = true;
    
    // valores iniciais dos sinais PWM
    OCR1A = 0;
    
    // configuracao do PWM
    //FAST PWM 10 bits (Modo 7) sem invers�o
    TCCR1A = _BV(COM1A1) | _BV(WGM10) | _BV(WGM11);
    TCCR1B = _BV(CS11) | _BV(WGM12);
    
    // PB1/OC1A como sa�da
    DDRB |= _BV(PORTB1);
    
    // valor inicial da vari�vel auxiliar
    uint16_t valorAD=0, before = 0;
    
    //Configura��o do AD
    ADMUX  |= _BV(REFS0); //Utiliza VCC como referência 
    ADCSRA |= _BV(ADEN)|_BV(ADPS2)|_BV(ADPS1)|_BV(ADPS0);  //Habilita o AD e utiliza prescale selection de 128
    
    DDRD |= _BV(PORTD3); //PD3 como saída
    PORTD |= _BV(PORTD3); // ACENDE O PIND3
    DDRB &= 0b11111110; // PINO PB0 como entrada
    PORTB |= 0x00;
    
    // CONTA COM O CONTADOR 0
    TCCR0A |= 0x00;//_BV(WGM01)|_BV(WGM00);
	  TCCR0B |= _BV(CS02) | _BV(CS00);;  // 1/1024 prescale
	  TIMSK0 |= _BV(TOIE0);   // Enable timer0 overflow interrupt(TOIE0)
    sei();//Habilita interrupção 
    


    while(1)
    {
      if ((PINB & 0x01))
      {
        if(parar == true && abrir == false ){ // Esta fechado e vai abrir
          abrir = true;
          parar = false;
        }/*else if(abrir == true && parar == false ){ // estava abrindo e vai ficar aberto/parado
          parar = true;
        }*/else if(abrir == true && parar == true){ // EStava aberto e vai começar a fechar
          abrir = false;
          parar = false;
        }/*else{ // Está fechado
          abrir = false;
          parar = true;
        }*/
      if (valorAD >= 512){
        if(parar == true && abrir == false){
          abrir = true;
          parar = false;
        }else if(abrir == true && parar == false){
          parar = true;
        }
      }/*
      if(valorAD < 512){
        if(abrir == true && parar == true){
          abrir = false;
          parar = false;
        }else if(abrir == false && parar == false){
          parar = true;
        }
      }*/
      if(abrir == true && parar == false){
        if(!flag1){
        TempoInicial1 = seg;
        flag2 = true;
        }
        dif = seg - TempoInicial1;        
        PORTD = 0x00;
        while(dif < timeSec ){
          dif = seg - TempoInicial1;
          OCR1A = uint8_t((timeSec-dif)*1023);
        }
        OCR1A = 0;
        parar = true;
        flag1 = false;
        PORTD |= _BV(PORTD3);
      }
      
      if(!flag1){
        TempoInicial1 = seg;
        flag1 = true;
        }
        
        PORTD = 0x00;
        funcionar = true;
        OCR1A = ADC;
        if(parar){
          OCR1A = 1024;  
        }        
        aberto = true;
        flag1 = false;
        PORTD |= _BV(PORTD3);   
      /*else if ((valorAD > 511) )
      { 
        if(!flag2){
        TempoInicial2 = seg;
        flag2 = true;
        }
        if(seg - TempoInicial2 == timeSec){
          funcionar = false;
          TempoInicial2 = 0;
        }       
        PORTD = 0x00;
        funcionar = true;
        while(funcionar){
          if((seg-TempoInicial2)<=(timeSec/2)){
            OCR1A = 1023;
          }else
          {
            OCR1A = 256; 
          }  
        }
        OCR1A = 1;
        aberto = true;
        flag2 = false;
        PORTD |= _BV(PORTD3);
      }*/
      /*
      else if(aberto){
        TempoInicial3 = seg;
        if(seg - TempoInicial3 == 20){
          fechar = true;
          TempoInicial3 = 0;
        }
        PORTD = 0b00000000;
        while(fechar){
          if((seg-TempoInicial3)<=(timeSec/2)){
            OCR1A = 1023;
          }else
          {
            OCR1A = 256; 
          }  
        }
        OCR1A = 1;
        aberto = false;
        PORTD = 0b10000000;
        }*/
    }
}
