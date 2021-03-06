from flask import Flask, render_template, request, json
import serial, time, requests
from datetime import datetime
from datetime import timedelta
import threading , math, astral
from astral.sun import sun

DataJson = {}

# ===================== Serial class ===================

class MySerial:
   ser = serial.Serial()

   # ---------------------------
   #def __init__(self, portcom):
   def __init__(self):
      self.ser.baudrate = 115200
      self.ser.timeout = 1

   def setTimeout(self, timeoutsec):
      self.ser.timeout = timeoutsec

   # ---------------------------
   def findPort(self):  # find Arduino serial port
      def testConnection():
         try:
            self.ser.open()
            self.serWrite('{"cmd":"TestConnection"}')
            readline = self.ser.readline()
            print(readline.decode())
            self.ser.close()

            return (readline.decode().rstrip() == "OK")
         except:
            return False

      self.ser.port = '/dev/ttyACM0'
      print(self.ser.port)
      if testConnection():
         return "Port: " + self.ser.port
      self.ser.port = '/dev/ttyACM1'
      print(self.ser.port)
      if testConnection():
         return "Port: " + self.ser.port
         return
      self.ser.port = '/dev/ttyACM2'
      print(self.ser.port)
      if testConnection():
         return "Port: " + self.ser.port
         return

   # ---------------------------
   def serOpen(self):
      try: 
         self.ser.open()
         print("Port: ", self.ser.port)
      except Exception as e:
         # print ("Error open serial port: " , str(e))
         self.findPort()
         # self.ser.close()
         try: 
            self.ser.open()
            print("Port: ", self.ser.port)
         except Exception as e:
            # print ("Error open serial port: " , str(e))
            exit()

   # ---------------------------
   def serClose(self):
      self.ser.close()

   # ---------------------------
   def serWrite(self, message):
      if self.ser.isOpen():
         #time.sleep(0.001)
         try:
            self.ser.flushInput() #flush input buffer, discarding all its contents
            self.ser.flushOutput()
            #time.sleep(0.1)
            self.ser.write(str.encode(message))  
         except Exception as e:
            print ("Error to write communication ...")
      else:
         print("Cannot open serial port")

   # ---------------------------
   def serReadline(self):
      if self.ser.isOpen():
         return self.ser.readline()
      else:
         print("Cannot open serial port")

mySerial = MySerial()

# ===================== Main Webpage ===================

app = Flask(__name__)

@app.route('/')
def mainhome():
   print(mySerial.findPort())
   return render_template('simple-sender.html')

# ===================== Set Text =====================

@app.route('/Set_Text', methods=['POST'])
def settext():
   data = getSignNumber()
   data["cmd"]   = "SetText"
   data["X"]     = request.form['cursorx']
   data["Y"]     = request.form['cursory']
   data["Size"]  = request.form['textsize']
   data["Red"]   = request.form['red']
   data["Green"] = request.form['green']
   data["Blue"]  = request.form['blue']
   data["Text"]  = request.form['sign_text']
   data["Font"]  = request.form['font']

   json_obj     = json.dumps(data)
   print(json_obj)
   mySerial.serOpen()
   mySerial.serWrite( json_obj )
   mySerial.serClose()
   return json.dumps({'Command Received':'Set_Text'})

# ===================== Set Background Color ==========

@app.route('/Set_Background', methods=['POST'])
def setbackground():
   data = getSignNumber()
   data["cmd"]   = "SetBackground"
   data["Redback"]   = request.form['redback']
   data["Greenback"] = request.form['greenback']
   data["Blueback"]  = request.form['blueback']

   json_obj     = json.dumps(data)
   print(json_obj)
   mySerial.serOpen()
   mySerial.serWrite( json_obj )
   mySerial.serClose()
   return json.dumps({'Command Received':'Set_Background'})

# ====================== Delete All ============================

@app.route('/Delete_All', methods=['POST'])
def Delete_All():
   dimTimer.stop() 

   print("Delete All ..... ")
   data = getSignNumber()

   data["cmd"]   = "DeleteAll"
   json_obj     = json.dumps(data)

   mySerial.serOpen()
   # mySerial.serWrite('{"cmd":"DeleteAll"}');
   mySerial.serWrite( json_obj )
   mySerial.serClose()
   return json.dumps({'Command Received':'Delete_All'})

# ====================== Default display ========================

@app.route('/Default_Display', methods=['POST'])
def Default_Display():
   dimTimer.stop() 

   print("Default display ..... ")
   data = getSignNumber()

   data["cmd"]   = "Default"
   json_obj     = json.dumps(data)

   mySerial.serOpen()
   mySerial.serWrite( json_obj )
   mySerial.serClose()
   return json.dumps({'Command Received':'Default'})

# ====================== Save Pixels ============================

@app.route('/SavePixels', methods=['POST'])
def savepixel():
   dimTimer.stop() 

   pixelcolors = []
   mySerial.serOpen()
   mySerial.serWrite('{"cmd":"SavePixel"}');
   fp = open("lastPixels.json", "w")
   readsave = mySerial.serReadline()
   while len(readsave):
      pixelcolors.append(int(readsave.decode()))
      readsave = mySerial.serReadline()
   mySerial.serClose()
   pixeljson = {}
   pixeljson["Pixels"] = pixelcolors
   DataJson["Pixels"]  = pixelcolors
   # print(DataJson["Pixels"])
   json.dump(pixeljson, fp)
   fp.close()

   dimTimer.restart() 
   return json.dumps({'Command Received':'Save'})

# ===================== Open Saved Pixels file ========================

def openSavedFile():
   try:
      global DataJson
      fp = open("lastPixels.json", "r")
      print("Load lastPixels.json file")
      DataJson = json.load(fp) 
      fp.close()
      return True
   except:
      print("Cannot open lastPixels.json file") 
      return False

# ===================== Get Sign number ========================

def getSignNumber():
   data = {}
   try:
      sign1 = request.form['sign_1']
      channel = 1
   except:
      channel = 0
   try:
      Sign2 = request.form['sign_2']
      channel = channel + 2
   except:
      pass
   data["Channel"] = str(channel)
   return data

# ====================== Load Saved Pixels ============================

@app.route('/Load_SavePixels', methods=['POST'])
def loadpixel():
   if openSavedFile():
      global DataJson
      dimTimer.stop() 
      data = getSignNumber()
      data["Pixels"] = str(DataJson["Pixels"]) 

      data["cmd"]   = "SetPixels"
      json_obj     = json.dumps(data)
      mySerial.serOpen()
      mySerial.serWrite( json_obj )
      mySerial.serClose()
      dimTimer.restart() 

   return json.dumps(data["Pixels"])

# ===================== Set Brightness =====================

def set_Brightness(bright):
   if openSavedFile():
      global DataJson
      newData = {}
      newp = []
      #print(DataJson["Pixels"])
      #print(len(DataJson["Pixels"]))
      count = 0
      for eachp in DataJson["Pixels"]:
         if count % 2:
            b = int((eachp & 255) * bright / 255)
            g = int(((eachp >> 8) & 255) * bright / 255) << 8
            r = int((eachp >> 16) * bright / 255) << 16 
            newcolor = b + g + r
            newp.append(newcolor)
            #newp.append(eachp)
         else:
            newp.append(eachp)

         count = count + 1
      
      data = getSignNumber()
      data["Pixels"] = str(newp)
      data["cmd"]   = "SetPixels"
      json_obj     = json.dumps(data)
      mySerial.serOpen()
      mySerial.serWrite( json_obj )
      mySerial.serClose()

# ====================== Undo ============================

@app.route('/Undo', methods=['POST'])
def undo():
   data = getSignNumber()
   data["cmd"]   = "SetText"
   data["X"]     = request.form['cursorx']
   data["Y"]     = request.form['cursory']
   data["Red"]   = "0"
   data["Green"] = "0"
   data["Blue"]  = "0"
   data["Text"]  = request.form['sign_text']
   data["Size"]  = request.form['textsize']

   json_obj     = json.dumps(data)
   print(json_obj)
   mySerial.serOpen()
   mySerial.serWrite( json_obj )
   mySerial.serClose()

   return json.dumps({'Command Received':'Undo'})

# ================== Test Night Time Brightness ========

@app.route('/Test_NightBrightness', methods=['POST'])
def nightbrightness():
   mySerial.serOpen()
   mySerial.serWrite('{"cmd":"Test_NightBrightness"}');
   mySerial.serClose()
   print("Test Night Brightness")

   return json.dumps({'Command Received':'Test_NightBrightness'})

# ===================== Set Text =====================

@app.route('/Set_Pixels', methods=['POST'])
def setpixel():
   data = getSignNumber()
   data["cmd"]    = "SetPixels"
   pixelpts = request.form['pixels'].split(',')
   num = []
   colo = []
   nn = 0
   for x in pixelpts:
      if nn%2:
         colo.append(x)
      else:
         num.append(x)
      nn = nn + 1
   zip_obj = zip(num, colo)

   groupnumber = 300   # number of pixels sent each time
   mySerial.setTimeout(0.1*groupnumber)
   mySerial.serOpen()

   nn = 0
   for loc, color in zip_obj:
      if nn % groupnumber == 0:  # beginning of a group of array
         jstr = "[" + loc + "," + color 
      elif nn % groupnumber < groupnumber-1:
         jstr = jstr + "," + loc + "," + color 
      else:
         data["Pixels"] = jstr + "," + loc + "," + color + "]"
         json_obj       = json.dumps(data)
         print(json_obj)
         mySerial.serWrite( json_obj )
        # if mySerial.serReadline() == b'OK':
         if mySerial.serReadline() == b'OK\r\n':
            print("OK")
         else:
            print("Fail to send pixel")
            return "Fail to send pixel"
      nn = nn + 1
   if nn % groupnumber < groupnumber:
      data["Pixels"] = jstr + "]"
      json_obj       = json.dumps(data)
      print(json_obj)
      mySerial.serWrite( json_obj )
#      print(mySerial.serReadline())
      if mySerial.serReadline() == b'OK\r\n':
         print("OK")
      else:
         print("Fail to send pixel")
         return "Fail to send pixel"
       
   mySerial.serClose()
   return json.dumps({'Command Received':'Set_Pixels'})

# ====================== Calculate Dusk and Dawn =========================

def get_Calc_Dusk_Dawn():
   city = astral.LocationInfo('Minneapolis', 'US', 'US/Central', 44.74683 , -93.193575)
   sunloc = sun(city.observer, date=datetime.now())
   sunrise , sunset = sunloc["sunrise"], sunloc["sunset"]
   sunrisemin = (int(sunrise.hour)-5) *60 + int(sunrise.minute)
   sunsetmin  = (int(sunset.hour)-5)  *60 + int(sunset.minute)
   #sunrisemin = (int(sunrise.hour)-5) *60 + int(sunrise.minute)
   print("\n====== Getting Sunrise and Sunset from internet =======")
   print("        Sunrise = %s, Sunset = %s minutes\n" % (sunrisemin, sunsetmin), end ='')
   print("=======================================================\n")
   return sunrisemin , sunsetmin

# ================ Background whether to dim at night ============

class TimerDim():
   def __init__(self, interval):
      self.isDim          = False
      self.isCheckSunTime = False
      self.lasttime       = time.time()
      self.interval       = interval
      self.thread = threading.Thread(target=self.run, args=())
      self.thread.daemon  = True         # Daemonize thread
      self.thread.start()                # Start the execution
      try:
         self.sunrise , self.sunset = get_Calc_Dusk_Dawn()
      except:
         self.sunrise , self.sunset = 360 , 1080  # default sunrise/set

   def run(self):
      while True:
         elapsed = time.time() - self.lasttime

#         if elapsed > self.interval and self.isCheckSunTime:
         if self.isCheckSunTime:
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            now_minutes = int((now - midnight).seconds / 60)

            print("Interval checking: Now = %s, Sunrise = %s, Sunset = %s minutes" % (now_minutes, self.sunrise, self.sunset), end ='')

            if now_minutes > self.sunset or now_minutes < self.sunrise:
               print(" Nighttime, ", end = "")
               if not self.isDim:  # has not been dimmed yet
                  try:
                     self.sunrise , self.sunset = get_Calc_Dusk_Dawn()
                  except:
                     pass
# added in the future
#                  set_Brightness(15)
                  self.isDim = True
                  print("     =======   Time to dim =====")
            else:
               print(", Daytime, ", end = "")
               if self.isDim:  # has not been undimmed yet
                  self.sunrise , self.sunset = get_Calc_Dusk_Dawn()
# added in the future
#                  set_Brightness(80)
                  self.isDim = False
                  print("     =======   Time to NOT to dim ====")

            # self.lasttime = time.time()
            print("Elapsed: %.1f" % (elapsed))
            time.sleep(self.interval)
         else:
            print("== Not checking Sun Time ==== Elapsed: %f" %(elapsed))
            time.sleep(600)
      print("========Exiting Sun Time Thread ====")

   def stop(self):
      self.isCheckSunTime = False  # global to stop dimTimer thread
      self.isDim          = False
      self.lasttime       = time.time()
      print("========Stop Sun Time Dimmer Thread ====")

   def restart(self):
      self.isCheckSunTime = True  # global to stop dimTimer thread
      print("========Restart Sun Time Dimmer Thread ====")

# ====================== Web IP and Port ============================

if __name__=="__main__":

   dimTimer = TimerDim(60)

   app.run(host= '0.0.0.0',port=5000,debug=True)

# ===================== General Initialization ======================


