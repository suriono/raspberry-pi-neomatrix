// ===================================================

void Neopixel_Initial() {

  delay(5000);
  
  matrix.begin();
  matrix2.begin();
  matrix.setTextWrap(false); 
  matrix2.setTextWrap(false);
  matrix.setBrightness(200);  // from 0 to 255
  matrix2.setBrightness(200);
  matrix.fillScreen(0); 
  //matrix.setTextSize(1);
  //matrix.fillScreen(0); 
  //matrix.setTextColor(matrix.Color(0, 0, 10));
  //matrix.print(F(" UZ"));
  
  
  //   // so no big surge of current at the beginning
  
  matrix.setTextSize(2);
  
  matrix.setCursor(0,13);
  matrix.setTextColor(matrix.Color(0, 255, 0));
  matrix.print(F("OPEN"));

  matrix.setCursor(50,0);
  matrix.setTextColor(matrix.Color(255, 0, 0));
  matrix.print(F("Hearts"));

  matrix.setTextColor(matrix.Color(29, 219, 159));
  matrix.setCursor(72,16);
  matrix.print(F(" Minds"));

  matrix.setTextColor(matrix.Color(237, 23, 100));
  matrix.setCursor(146,8);
  matrix.print(F("Door"));

  matrix.setTextSize(1);
  matrix.setTextColor(matrix.Color(255, 0, 0));
  matrix.setCursor(0,32);
  matrix.print(F("www.RiverHillsUMC.org"));

  matrix.show();
}
