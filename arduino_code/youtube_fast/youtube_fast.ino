#include <SPI.h>
#include "SH1106_SPI.h"

#define USE_FRAME_BUFFER

#ifdef USE_FRAME_BUFFER
SH1106_SPI_FB lcd;
#else
SH1106_SPI lcd;
#endif
void setup(void)
{
	Serial.begin(1000000);
	lcd.begin(0,1);
	lcd.print(F("Preparing benchmark"));
#ifdef USE_FRAME_BUFFER
	lcd.renderAll();
#endif
	delay(1000);
}

int i = 0;

bool data_flag = false;

char magic[5] = {0xDE, 0xEA, 0xDB, 0xEE, 0xEF};
char magic_iterator = 0;
void loop(void) 
{
  if(!data_flag)
  {
    while(Serial.available() > 0)
    {
      char character = Serial.read();
      lcd.print(character);
      if(magic[magic_iterator] ==  character)
      {
        if(magic_iterator == 4)
        {
          data_flag = true;
          magic_iterator = 0;
          //lcd.begin(0,1);
          //lcd.print(F("recognised"));
          //lcd.renderAll();
          break;
        }
        magic_iterator++;
      }
      else
      {
        magic_iterator = 0;
      }
    }
  }
  
  if(data_flag)
  {
    i = 0;
    while(i < 1024)
    {
      if(Serial.available())
      {
        lcd.setBuffer(i,Serial.read());
        i++;
      }
    }
    lcd.renderAll();
    data_flag = false;
  }

  


 /*
 lcd.setBuffer(i,0b10101010);

  for(i = 1; i<1024; i++)
  {
    lcd.setBuffer(i,0b0);
  }
  
	lcd.renderAll();
  delay(1);
  */
}
