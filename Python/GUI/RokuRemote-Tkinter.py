import sys; import socket; import time; import re; import xml.etree.ElementTree; import urllib;
if sys.version_info[0]>2: import tkinter as tk; import tkinter.messagebox as tkMessageBox
else: import Tkinter as tk; import tkMessageBox
#Message to scan for rokus
ssdpMessage="""M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
Man: "ssdp:discover"
ST: roku:ecp

"""
#Functions for rokus
def urlencode(x):
	if sys.version_info[0] < 3:return urllib.quote_plus(x)
	else:return urllib.parse.quote_plus(x)
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
		sendCommand(rokuIP, "keypress/lit_"+urlencode(char))
		time.sleep(0.1)
#Discovers rokus
def discoverRokus():
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(ssdpMessage, ("239.255.255.250", 1900));
	s.settimeout(1)
	try: return re.findall(r'LOCATION: http://(.*):8060', str(s.recvfrom(1024)))[0]
	except socket.timeout: return None
#Repetitevly scans for x seconds
def scanRokus(seconds):
	startTime=time.time()
	allRokus=[]
	while(time.time()<startTime+seconds):
		rokuIP=discoverRokus()
		if rokuIP==None: continue;# print("Timed Out");
		if rokuIP in allRokus: continue
		allRokus.append(rokuIP)
	return allRokus
#Functions for buttons, etc
selectedRokuIP=None
def switchToControl(evt):
	global selectedRokuIP
	if not len(RokuList.curselection()):
		tkMessageBox.showinfo("Error", "Please select a roku.")
		return False
	selectedRokuIP=RokuList.get(RokuList.curselection()[0])
	CRFrame.pack_forget()
	RCFrame.pack(fill=tk.BOTH, expand=tk.YES)
def updateRokuList():
	RokuList.delete(0, tk.END)
	allRokus=scanRokus(5)
	for rokuIP in allRokus:
		RokuList.insert(tk.END, rokuIP)
#Code starts here/Main loop for Tkinter
root=tk.Tk()
root.title("Roku Remote")
CRFrame=tk.Frame(root) #Choose Roku Frame
CRFrame.pack(fill=tk.BOTH, expand=tk.YES)
RokuList=tk.Listbox(CRFrame, selectmode=tk.SINGLE)
RokuList.bind('<<ListboxSelect>>', switchToControl)
RokuList.pack(fill=tk.BOTH, expand=tk.YES)
ScanButton=tk.Button(CRFrame, command=updateRokuList, text="Scan")
ScanButton.pack(fill=tk.BOTH, expand=tk.YES)
RCFrame=tk.Frame(root) #Roku Controls Frame
#Roku Buttons Here
backBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="BACK", command=lambda: sendCommand(selectedRokuIP, "keypress/Back"))
backBtn.grid(row=0, column=0)
upBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="UP", command=lambda: sendCommand(selectedRokuIP, "keypress/Up"))
upBtn.grid(row=0, column=1)
homeBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="HOME", command=lambda: sendCommand(selectedRokuIP, "keypress/Home"))
homeBtn.grid(row=0, column=2)
leftBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="LEFT", command=lambda: sendCommand(selectedRokuIP, "keypress/Left"))
leftBtn.grid(row=1, column=0)
okBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="OK", command=lambda: sendCommand(selectedRokuIP, "keypress/Select"))
okBtn.grid(row=1, column=1)
rightBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="RIGHT", command=lambda: sendCommand(selectedRokuIP, "keypress/Right"))
rightBtn.grid(row=1, column=2)
downBtn=tk.Button(RCFrame, bg="purple3", fg="snow", text="DOWN", command=lambda: sendCommand(selectedRokuIP, "keypress/Down"))
downBtn.grid(row=2, column=1)

root.mainloop()