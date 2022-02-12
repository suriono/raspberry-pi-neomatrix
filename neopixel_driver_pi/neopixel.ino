// ================= Initial ==================================

void Neopixel_Initial() {
  delay(5000);
  
  matrix1.begin();             matrix2.begin();
  matrix1.setTextWrap(false);  matrix2.setTextWrap(false); 
  
  Neopixel_Default();
}

// ==================== Default Text =====================

void Neopixel_Default() {
  matrix1.setBrightness(200); matrix2.setBrightness(200);
  matrix1.fillScreen(0);      matrix2.fillScreen(0); 
  for (byte nn=1 ; nn<3; nn++) {
    matrix1.setFont(&FreeSerif9pt7b);
    matrix2.setFont(&FreeSerif9pt7b);
    //Neopixel_SetText(nn, 2, matrix1.Color(0, 255, 0),    "OPEN",   0, 13);
    //Neopixel_SetText(nn, 2, matrix1.Color(255, 0, 0),    "Hearts", 50, 0);
    //Neopixel_SetText(nn, 2, matrix1.Color(29, 219, 159), "Minds",  72, 16);
    //Neopixel_SetText(nn, 2, matrix1.Color(237, 23, 100), "Doors",  134, 8);
    Neopixel_SetText(nn, 1, matrix1.Color(0, 255, 0),    "OPEN",   0, 23);
    Neopixel_SetText(nn, 1, matrix1.Color(255, 0, 0),    "Hearts", 55, 11);
    Neopixel_SetText(nn, 1, matrix1.Color(29, 219, 159), "Minds",  80, 28);
    Neopixel_SetText(nn, 1, matrix1.Color(237, 23, 100), "Doors",  140, 19);
    matrix1.setFont(); matrix2.setFont();
    Neopixel_SetText(nn, 1, matrix1.Color(255, 0, 0), "www.RiverHillsUMC.org",  32, 32);
  }
  matrix1.show();  matrix2.show();
}

// ==================== Set Text =========================

void Neopixel_SetText(byte thischannel, byte textsize, uint32_t color, String text, int x, int y) {
  if (thischannel & 1) {
    matrix1.setTextSize(textsize);
    matrix1.setTextColor(color);
    matrix1.setCursor(x,y);
    matrix1.print(text);
  }
  if (thischannel & 2) {
    matrix2.setTextSize(textsize);
    matrix2.setTextColor(color);
    matrix2.setCursor(x,y);
    matrix2.print(text);
  }
}
