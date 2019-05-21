
List<int> heartBeatArray = new ArrayList();

boolean sendInterruption = false;

void main() {

	

	int clockDivisionTarget = "Clock Galileo"/1000;
	int clockDivisionCount = 0;


	while(true){
		
		if(sendInterruption){

			sendImageToPC(makeImage(heartBitArray));

			heartBeatArray = new ArrayList();


			sendInterruption = false;
		}
		else{
			if(clockDivisionCount >= clockDivisionTarget){
				//Pega o valor do sensor
				heartBeatArray.add(sensorImput.getValue());
				clockDivisionCount=0;
			}	
			else{
				clockDivisionCount++;
			}
		
		}
		

	}

} 

void sendInfoToPC(int heartBeat){


}

void ThreadFunction(){

	int clockDivisionTarget = "Click Galileo"*5;
	int clockDivisionCount = 0;

	while(true){

		if(clockDivisionCount == clockDivisionTarget){
			//Provoca a interrupção 
			sendInterruption = true;
			clockDivisionCount=0;
		}	
		else{
			clockDivisionCount++;
		}


	}

}
	
