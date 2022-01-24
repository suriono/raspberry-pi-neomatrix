// ================= Initial ==================================

void Neopixel_Initial() {

  delay(5000);
  
  matrix1.begin();
  matrix1.setTextWrap(false); 
  matrix1.setBrightness(200);  // from 0 to 255
  matrix1.fillScreen(0); 
  
  matrix2.begin();
  matrix2.setTextWrap(false); 
  matrix2.setBrightness(200);  // from 0 to 255
  matrix2.fillScreen(0); 

  for (byte nn=1 ; nn<3; nn++) {
    Neopixel_SetText(nn, 2, matrix1.Color(0, 255, 0),    "OPEN",   0, 13);
    Neopixel_SetText(nn, 2, matrix1.Color(255, 0, 0),    "Hearts", 50, 0);
    Neopixel_SetText(nn, 2, matrix1.Color(29, 219, 159), "Minds",  72, 16);
    Neopixel_SetText(nn, 2, matrix1.Color(237, 23, 100), "Doors",  134, 8);
    Neopixel_SetText(nn, 1, matrix1.Color(255, 0, 0), "www.RiverHillsUMC.org",  0, 32);
  }
  matrix1.show();
  matrix2.show();
}

// ==================== Set Text =========================

void Neopixel_SetText(byte channel, byte textsize, uint32_t color, String text, int x, int y) {
  if (channel & 1) {
    matrix1.setTextSize(textsize);
    matrix1.setTextColor(color);
    matrix1.setCursor(x,y);
    matrix1.print(text);
  }
  if (channel & 2) {
    matrix2.setTextSize(textsize);
    matrix2.setTextColor(color);
    matrix2.setCursor(x,y);
    matrix2.print(text);
  }
}
