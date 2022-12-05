import requests, sys, json, time
from multidict import MultiDict

filename = sys.argv[1]

for line in open(filename, 'r'):
   if 'Cmd' in line:
      jsoncmd = json.loads(line)
      Command = jsoncmd['Cmd']
      Delay   = jsoncmd['Delay']
      print("\nCMD:", Command, " , Delay: ", Delay)
      if 'Delete_All' in Command:
         reqobj = requests.post("http://localhost:5000/" + Command)
         
   elif 'sign_1' in line:
      tmparr  = line.split('&')
      newlist = []
      for eacharr in tmparr:
         pair = eacharr.split('=')
         newpair = (pair[0],pair[1])
         newlist.append(newpair)
      new_md = MultiDict(newlist)
      print(new_md)
    
      if 'Set_' in Command:
         reqobj = requests.post("http://localhost:5000/" + Command, data=new_md)
      time.sleep(Delay)


#rdata = MultiDict(sign_1='on',sign_2='on',pixels='12,9109504,13,255')
#rdata = MultiDict(sign_1='on',sign_2='on',pixels='12,0,13,0')
#print(rdata)
# rdata = {'sign_1':'on','sign_2':'on",'cursorx'=0,'cursory':17,'sign_text':'T','red':0,'green':200,'blue':0}

#r = requests.post("http://localhost:5000/Set_Pixels", data=rdata)
#r = requests.post("http://localhost:5000/Set_Text", data=rdata)
#r = requests.get("http://localhost:5000")
#print(r.text)
