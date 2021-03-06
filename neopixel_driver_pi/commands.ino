void Command_Run() {
  String Cmd = JSON.stringify(jsonObject["cmd"]); Cmd.replace("\"","");
  Serial.print(Cmd);
  Serial.print("========");
  Serial.println();
  if (Cmd.equals("DeleteAll")) {
     Delete_All();
  } else if (Cmd.equals("Default")) {
     Neopixel_Default();
  } else if (Cmd.equals("TestConnection")) {
     Serial.print("test connection OK");
     SerialUSB.println("OK");
  } else if (Cmd.equals("SetText")) {
     Set_Text();
  } else if (Cmd.equals("SetBackground")) {
     Set_Background(2);
  } else if (Cmd.equals("Test_NightBrightness")) {
     Test_Dimmer(70);
  } else if (Cmd.equals("SetPixels")) {
     Set_Pixels();
  } else if (Cmd.equals("SavePixel")) {
     Get_Pixels();
  //} else if (Cmd.equals("Red_Background")) {
  //   Set_Background(1);
  //} else if (Cmd.equals("Green_Background")) {
  //   Set_Background(2);
  //} else if (Cmd.equals("Blue_Background")) {
  //   Set_Background(3);
  }
}

// ============== Background Color ===============
void Set_Background(byte colortype) {
  int r = Json_parse_int("Redback");
  int g = Json_parse_int("Greenback");
  int b = Json_parse_int("Blueback");
  //switch ( colortype) {
  //  case 1:
      matrix1.fillScreen(matrix1.Color(r,g,b));
      matrix2.fillScreen(matrix1.Color(r,g,b));
   //   break;
   // case 2:
   //   matrix1.fillScreen(matrix1.Color(0,50,0));
    //  matrix2.fillScreen(matrix1.Color(0,50,0));
    //  break;
   // case 3:
   //   matrix1.fillScreen(matrix1.Color(0,0,50));
    //  matrix2.fillScreen(matrix1.Color(0,0,50));
    //  break;
    //default:
    //  Delete_All();
    //  break;
  //}
  matrix1.show();
  matrix2.show();
}

// ============== Delete All ===============
void Delete_All() {
  matrix1.fillScreen(0);
  matrix1.show();
  matrix2.fillScreen(0);
  matrix2.show();
}

// ============== Test Dimmer ===============
void Test_Dimmer(int bright) {
  uint32_t pixcol[256*TILE_COLUMNS*TILE_COLUMNS], pixcolor,pixnight;
  uint32_t r, g, b;
  for (int nn=0; nn < 256*TILE_COLUMNS*TILE_COLUMNS ; nn++) {
    pixcol[nn] = matrix1.getPixelColor(nn);
    
    if (pixcol[nn] > 0) {
      b = (pixcol[nn] & 255  ) * bright / 255;
      g = int(((pixcol[nn]>>8)&255) * bright / 255)<<8;
      r = int((pixcol[nn]>>16) * bright / 255)<<16;
      matrix1.setPixelColor(nn, b+g+r);
    }
  }
  matrix1.show();
  delay(3000);
  for (int nn=0; nn < 256*TILE_COLUMNS*TILE_COLUMNS ; nn++) {
    if (pixcol[nn] > 0) {
      matrix1.setPixelColor(nn, pixcol[nn]);
    }
  }
  matrix1.show();
}

// ============== Set Cursor ===============
void Set_Cursor() { 
  int x = Json_parse_int("X");
  int y = Json_parse_int("Y");
  if (channel & 1) {
     matrix1.setCursor(x,y);
  }
  if (channel & 2) {
     matrix2.setCursor(x,y);
  }
}

// ============== Set Colors ===============
void Set_TextColor() { 
  int r = Json_parse_int("Red");
  int g = Json_parse_int("Green");
  int b = Json_parse_int("Blue");
  if (channel & 1) {
     matrix1.setTextColor(matrix1.Color(r, g, b));
  }
  if (channel & 2) {
     matrix2.setTextColor(matrix1.Color(r, g, b));
  }
}

// ============== Set Text ===============
void Set_Text() {
  channel = Json_parse_int("Channel");
  Set_Cursor();
  Set_TextColor();
  Set_Font();
  
  if (channel & 1) {
     matrix1.setTextSize(Json_parse_int("Size"));
     matrix1.print(Json_parse_str("Text"));
     matrix1.show();
  }
  if (channel & 2) {
     matrix2.setTextSize(Json_parse_int("Size"));
     matrix2.print(Json_parse_str("Text"));
     matrix2.show();
  }
}

// ============== Set Pixels ===============
void Set_Pixels() {
  channel = Json_parse_int("Channel");
  JSONVar pp = JSON.parse(jsonObject["Pixels"]); // pair of pixel# & color
  
  for (int nn=0; nn < pp.length()/2 ; nn++) {
    if (channel & 1) {
       matrix1.setPixelColor(int(pp[nn*2]), int(pp[nn*2+1]));
       //matrix1.show();
    }
    if (channel & 2) {
       matrix2.setPixelColor(int(pp[nn*2]), int(pp[nn*2+1]));
       //matrix2.show();
    }
  }

  if (channel & 1) {
    matrix1.show();
  }
  if (channel & 2) {
    matrix2.show();
  }
  SerialUSB.println("OK");
}

// ============== Get Pixels ===============
void Get_Pixels() {
  uint32_t pixcolor;
  for (int nn=0; nn < 256*TILE_COLUMNS*TILE_COLUMNS ; nn++) {
    pixcolor = matrix1.getPixelColor(nn);
    Serial.println(pixcolor);
    if (pixcolor > 0) {
       SerialUSB.println(nn);
       SerialUSB.println(pixcolor);
    }
  }
}

// ============== Set Font ==================
void Set_Font() {
  String font = Json_parse_str("Font");
  if (font == "Default") {
    matrix1.setFont();
    matrix2.setFont();
  } else if (font == "FreeSerif9pt7b") {
    matrix1.setFont(&FreeSerif9pt7b);
    matrix2.setFont(&FreeSerif9pt7b);
  } else if (font == "FreeSerifBold9pt7b") {
    matrix1.setFont(&FreeSerifBold9pt7b);
    matrix2.setFont(&FreeSerifBold9pt7b);
  } else if (font == "FreeMonoBold9pt7b") {
    matrix1.setFont(&FreeMonoBold9pt7b);
    matrix2.setFont(&FreeMonoBold9pt7b);
  }
  
}
