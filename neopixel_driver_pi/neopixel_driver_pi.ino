#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <Arduino_JSON.h>
#include <Fonts/FreeSerif9pt7b.h>
#include <Fonts/FreeSerifBold9pt7b.h>
#include <Fonts/FreeMonoBold9pt7b.h>

#define PIN_NORTH_SIGN  46
#define PIN_SOUTH_SIGN  52
#define TILE_COLUMNS    6  
// 6
#define TILE_ROWS       5  
// 5
#define NEO_RED         9109504

 // Use Arduino Due because SRAM is high, 96KB, Mega is 8KB
Adafruit_NeoMatrix matrix1 = Adafruit_NeoMatrix(32, 8, TILE_COLUMNS, TILE_ROWS, PIN_NORTH_SIGN,
  NEO_TILE_TOP   + NEO_TILE_LEFT   + NEO_TILE_ROWS   + NEO_TILE_ZIGZAG +
  NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB + NEO_KHZ800);

Adafruit_NeoMatrix matrix2 = Adafruit_NeoMatrix(32, 8, TILE_COLUMNS, TILE_ROWS, PIN_SOUTH_SIGN,
  NEO_TILE_TOP   + NEO_TILE_LEFT   + NEO_TILE_ROWS   + NEO_TILE_ZIGZAG +
  NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB + NEO_KHZ800);

JSONVar jsonObject;

// ===================== Setup =====================
void setup() {
  Serial.begin(57600);
  SerialUSB.begin(115200);
  Neopixel_Initial();
}

// =================================================

int x = 0;
int nbright = 1;
int color_cycle = 0;
int bright_inc = 10;
byte channel = 0;

// ==================== LOOP =======================

void loop() {
  static unsigned long count = 0;
  char c;
  if (SerialUSB.available()) {
    
     String input;
     
     while(SerialUSB.available()) {
       c = SerialUSB.read();
       input += c;
     }
     jsonObject = JSON.parse(input);
     if (JSON.typeof(jsonObject) == "undefined") {
        Serial.println("Parsing input failed!");
     } else {
        Command_Run();
     }
  }
}
