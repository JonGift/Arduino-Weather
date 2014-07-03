//All of my led's connected to ports. Skipped over 5 to debug.
int led = 8;
int led2 = 9;
int led3 = 10;
int led4 = 11;
int led6 = 2;
int led7 = 3;

void setup() {
  Serial.begin(9600); //Serial with Python
  pinMode(led, OUTPUT); //turn on the lights
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led6, OUTPUT);
  pinMode(led7, OUTPUT);
}

void off(int pynum) { //turn off the important lights when sent the correct data.
  if(pynum > 0 && pynum < 6){
    digitalWrite(led, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);
  }
}

void loop(){
  Serial.write(1);
  delay(1000);
  if(Serial.available() > 0){ //if Python speaks.
    const char x = Serial.read(); //take some data from Python.
    int something = atoi(&x); //make it an int.
    off(something); //check to see if the first four led's updated.
    if(something == 1){ //do the cool stuff.
      digitalWrite(led, HIGH);
    }else if(something == 2){
      digitalWrite(led2, HIGH);
    }else if(something == 3){
      digitalWrite(led3, HIGH);
    }else if(something == 4){
      digitalWrite(led4, HIGH);
    }else if(something == 6){
      digitalWrite(led6, HIGH);
      digitalWrite(led7, LOW);
    }else if(something == 7){
      digitalWrite(led7, HIGH);
      digitalWrite(led6, LOW);
    }

  }
}
    

