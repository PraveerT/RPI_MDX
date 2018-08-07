/*
    This is a demo to test gas library
    This code is running on Xadow-mainboard, and the I2C slave is Xadow-gas
    There is a ATmega168PA on Xadow-gas, it get sensors output and feed back to master.
    the data is raw ADC value, algorithm should be realized on master.

    please feel free to write email to me if there is any question

    Jacky Zhang, Embedded Software Engineer
    qi.zhang@seeed.cc
    17,mar,2015
*/

#include <Adafruit_Sensor.h>

#include "DHT.h"

#define DHTPIN A1     

#define DHTTYPE DHT11 
#include <Wire.h>
#include "MutichannelGasSensor.h"
DHT dht(DHTPIN, DHTTYPE);
void setup()
{
    Serial.begin(115200);  // sta
    gas.begin(0x19);//the default I2C address of the slave is 0x04
    gas.powerOn();
    dht.begin();
}

void loop()
{
    delay(60000);
    float a,b,c,d,e,f,g,h;
    
    
    
    
    //---DHT
    
    
  float p = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float pr = dht.readTemperature(true);
  float hif = dht.computeHeatIndex(pr, p);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(pr, p, false);

  // Check if any reads failed and exit early (to try again).
 

    a= gas.measure_NH3();



    b= gas.measure_CO();
  


    c= gas.measure_NO2();




    d = gas.measure_C3H8();
   

    e = gas.measure_C4H10();
  



    f = gas.measure_CH4();
  



    g = gas.measure_H2();
   

   

    h = gas.measure_C2H5OH();
 
 
 Serial.print(a);
 Serial.print(",");
 Serial.print(b);
 Serial.print(",");
 Serial.print(c);
 Serial.print(",");
 Serial.print(d);
 Serial.print(",");
 Serial.print(e);
 Serial.print(",");
 Serial.print(f);
 Serial.print(",");
 Serial.print(g);
 Serial.print(",");
 Serial.print(h);
 Serial.print(",");
 Serial.print(p);
 Serial.print(",");
 Serial.print(t);
 Serial.print(",");
 Serial.print(hic);
 Serial.println();
 
}
