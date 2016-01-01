### IMPORTS ######################################
import argparse
import opc
import time
import re


from pythonosc import dispatcher
from pythonosc import osc_server

### GLOBAL ######################################

### this is dirty AF, but we'll go with it for a bit yeah? ok.

addressList = ['0006666881F2','00066678832A']
currentMacAddress = ''

### FADE CANDY ############################################

client = opc.Client('127.0.0.1:7890',long_connection=True, verbose=True)
commands = ['swipe','trail','blink','off']

### OPEN TO ABELTON ########################################
## no idea how to do this ATM 
## Maybe just use an internal Python sound thing....

### MUSE HANDLER ######################################
def muse_handler(unused_addr,args,mConfig):
	
	#print("[{0}] ~ {1}".format(args[0], mConfig))

	global currentMacAddress

	## sends an str that looks like a dict but is malformed, stripping out the Mac Address
	## unique to each muse
	
	x = mConfig.split(',')
	dirtyAddress = x[0] 
	cleanAddress = re.sub(r'[^\w\s]','',dirtyAddress)
	finalAddress = cleanAddress[8:] #its always gonna be mac_addr

	#print("Mac Address:", finalAddress)

	if finalAddress in addressList:
		currentMacAddress = finalAddress

			
### DATA HELPERS ######################################

def blink_handler(unused_addr,args,blinkBoolean):
	"""
	Boolean for Blink 
	"""
	if blinkBoolean == 1:
		if currentMacAddress == addressList[0]:
			print("Muse-{0}: Blink1: ".format(currentMacAddress))
			fade_candy_sender(commands[0],currentMacAddress)
		elif currentMacAddress == addressList[1]:
			print("Muse-{0}: Blink2: ".format(currentMacAddress))
			fade_candy_sender(commands[0],currentMacAddress)
		

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
	"""
	Raw EEG Floats
	"""
	#print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)
	if ch1 > 850:
		if currentMacAddress == addressList[0]:
			print("Muse-{0}: {1}".format(currentMacAddress,ch1))
			fade_candy_sender(commands[1],currentMacAddress)

def jaw_handler(unused_addr,args,clenchBool):
	"""
	Senses if the person's jaw is clenched or not (boolean).
	"""
	if clenchBool == 1:
		if currentMacAddress == addressList[0]:
			print("Muse-{0}: Clench: ".format(currentMacAddress))
			fade_candy_sender(commands[0],currentMacAddress)



def fade_candy_sender(command,IDer):
	"""
	This sends certain commands to the fade candy client. 
	"""
	
	print("!fade_candy_sender", command,IDer)

	if command == commands[0]:
		pass
	elif command == commands[1]:
		pass
	elif command == commands[2]:
		pass
	elif command == commands[3]:
		pass

def send_to_abelton(command):
	"""
	This sends certain commands to the ableton for noise
	"""
	print("!fade_candy_sender", command)

	if command == commands[0]:
		pass
	elif command == commands[1]:
		pass
	elif command == commands[2]:
		pass
	elif command == commands[3]:
		pass

### RUN IT #################################################

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip",
						default="127.0.0.1",
						help="The ip to listen on")
	parser.add_argument("--port",
						type=int,
						default=5002,
						help="The port to listen on")
	args = parser.parse_args()

	### CALL DATA HANDLERS  ######################################

	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/debug", print)
	dispatcher.map("/muse/config", muse_handler,"Which Muse")
	dispatcher.map("/muse/elements/blink", blink_handler,"Blink")

	server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)  ## enter server and port on command line

	print("Serving on {}".format(server.server_address))
	server.serve_forever()