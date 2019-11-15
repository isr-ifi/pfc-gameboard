#include <Arduino.h>
#include <definitions.h>
#include <Adafruit_PN532.h>


/*
   Information about tags we use:

   TAG Type       PAGES   USER START    USER STOP
   --------       -----   ----------    ---------
   NTAG 213       45      4             39

*/



//Initializes a given NFC sensor.
//Timeout (per sensor) is set in the library's Adafruit_PN532.h file
void initialize_sensor(Adafruit_PN532 sensor, int id){

    // TODO might be needed
    //digitalWrite(SENSOR1, HIGH);

    sensor.begin();
    uint32_t versiondata = sensor.getFirmwareVersion();
    //If no sensor found, return
    if (!versiondata) {
      Serial.print("Didn't find Sensor #"); Serial.println(id);
    }
    else{
      //Sensor Found
      sensorCount++;
      Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
      Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
      Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
      //Configure sensor to read RFID tags
      sensor.SAMConfig();
    }
}

//Reads an NFC tag and returns data contained within
//Params: Sensor, sensor ID (number), whether to be print additional info or not)
void readTag(Adafruit_PN532 sensor, int id, bool verbose){
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  //Buffer to store the returned UID
  uint8_t uidLength;                        //Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  uint8_t pageNumber = 9; //Number of pages to read. Max is 45, we only use the first 9
  success = sensor.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

  if (success) {
    //Print card UID if any is found
    if(verbose)
      Serial.print("Found card with UID "); sensor.PrintHex(uid, uidLength);
    uint8_t data[32];

    for (uint8_t i = 7; i <= pageNumber; i++) //Start at 7, because we don't need non-user data / format encoding stuff
    {
      success = sensor.ntag2xx_ReadPage(i, data);

      //Verbose logging of card data
      if(verbose){
        // Display the current page number
        Serial.print("PAGE ");
        if (i < 10)
        {
          Serial.print("0");
          Serial.print(i);
        }
        else
        {
          Serial.print(i);
        }
        Serial.print(": ");

        // Display the results, depending on 'success'
        if (success)
        {
          // Dump the page data
          sensor.PrintHexChar(data, 4);
        }
        else
        {
          Serial.println("Unable to read the requested page!");
        }
      }

      //Non-Verbose: return only relevant data
      else{
        if (success)
        {
          //Dump page data
          //sensor.PrintHex(data, 4);
          String txt((char*) data);
          //String txt(reinterpret_cast<char*>(data));
          BTSerial.println(txt);
        }
      }

    }
  }

}
