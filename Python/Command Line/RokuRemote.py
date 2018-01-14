import sys; import socket; import time; import re; import xml.etree.ElementTree;
if sys.version_info[0]>2:raw_input=input
helpMessage="""Commands:
home; 'Home' key
type:args; Sends text to roku
left; 'left' key
right; 'right' key
up; 'up' key
down; 'down' key
select; 'OK' key
ok; 'OK' key"""
ssdpMessage="""M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
Man: "ssdp:discover"
ST: roku:ecp

"""
#Gets device version
def getRokuType(rokuIP):
	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((rokuIP, 8060));
		s.send("GET /query/device-info HTTP/1.1\r\n\r\n")
		contentLentgh=int(re.findall(r'\r\nContent-Length: (\d+)\r\n', str(s.recv(1024)))[0])
		rokuData=xml.etree.ElementTree.fromstring(str(s.recv(contentLentgh)))
		return rokuData.find("model-name").text
	except Exception:return getRokuType(rokuIP)
#Sends commands to rokus
def sendCommand(rokuIP, command):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((rokuIP, 8060));
	s.send("POST /"+command+" HTTP/1.1\r\n\r\n");
def sendText(rokuIP, text):
	for char in text:
		sendCommand(rokuIP, "keypress/lit_"+char)
		time.sleep(0.1)
#Discovers rokus
def discoverRokus():
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(ssdpMessage, ("239.255.255.250", 1900));
	return re.findall(r'LOCATION: http://(.*):8060', str(s.recvfrom(1024)))[0]
#Repetitevly scans for x seconds
def scanRokus(seconds):
	endTime=time.time()+seconds
	allRokus=[]
	while(time.time()<endTime):
		rokuIP=discoverRokus()
		if rokuIP in allRokus: continue
		allRokus.append(rokuIP)
	return allRokus
#Code Starts Here
selectedRokuIP=None
#Check for command line arguments
if "--scan" in sys.argv:
	if len(sys.argv)>=(sys.argv.index("--scan")+2):
		try: eval(sys.argv[sys.argv.index("--scan")+1])
		except Exception: print("Invalid expression or number")
		scanRokus(eval(sys.argv[sys.argv.index("--scan")+1])) #Optionally change eval() to int()
	else: print("Seconds for scan required (example: 'RokuRemote --scan 1.5')")
	sys.exit()
if "--ip" in sys.argv:
	if len(sys.argv)<(sys.argv.index("--ip")+2):
		rokuIP=sys.argv[sys.argv.index("--scan")+1]
	else:print("No ip given after --ip"); sys.exit()
#User selects roku here
if selectedRokuIP==None:
	print("Scanning...\n")
	allRokus=scanRokus(5)
	for index, rokuIP in enumerate(allRokus):
		print(str(index)+":\nIP: '"+rokuIP+"'\nType: '"+getRokuType(rokuIP)+"'\n")
	sys.stdout.write("Enter Selected Roku Number: ")
	while 1:
		try:selectedRokuIP=allRokus[eval(raw_input())]; break
		except Exception: print("\nInvalid expression or number"); sys.stdout.write("Enter Selected Roku Number: ")
	print("Using Roku IP: '"+rokuIP+"'")
else:print("Using Pre-Set IP: '"+rokuIP+"'")
print("Type q/quit to quit, or h/help for more commands")
#Main Loop Here
while 1:
	command=raw_input()
	if command=="q" or command=="quit": sys.exit()
	elif command=="h" or command=="help": print(helpMessage)
#	elif command=="up"
#TODO: Implement all commands
	else:print("Bad command")
"""
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((rokus[chosenRoku], 8060));
while 1:
	s.send("POST /keypress/home HTTP/1.1\r\n\r\n"); time.sleep(2.5);
"""