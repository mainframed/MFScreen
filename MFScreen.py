#!/usr/bin/python

##################################################################
# Script to connect to a 3270 server and take a screenshot	 #
#                                                                #
# Requirements: Python, s3270 and optionally x3270               #
# Created by: Soldier of Fortran (@mainframed767)                #
# Usage: Given a hostname[:port] or file of hosts[:ports] 	 #
# connects and takes a screenshot of the first screen            #
#                                                                #
# Copyright GPL 2012                                             #
##################################################################

from py3270 import EmulatorBase
import time #needed for sleep
import sys 
import argparse #needed for argument parsing
import platform #needed for OS check


from blessings import Terminal
t = Terminal()

def Grab_Screen(hostname):
	command = 'printtext(html,' + hostname + '.html)'
	em.exec_command(command)

def Connect_to_ZOS(hostname):
	#connects to the target machine and sleeps for 'sleep' seconds
	em.connect(hostname)
	#em.connect(results.target)
	time.sleep(results.sleep)

print t.bold + '''

      8""8""8 8""""   8""""8                             
      8  8  8 8       8      eeee eeeee  eeee eeee eeeee 
      8e 8  8 8eeee   8eeeee 8  8 8   8  8    8    8   8 
      88 8  8 88          88 8e   8eee8e 8eee 8eee 8e  8 
      88 8  8 88      e   88 88   88   8 88   88   88  8 
      88 8  8 88      8eee88 88e8 88   8 88ee 88ee 88  8 						                                           

						By: Soldier of Fortran
						   (@mainframed767)

''' + t.normal


#start argument parser
parser = argparse.ArgumentParser(description='MF Screen - A script to capture the first screen of a mainframe',epilog='Get it!')
parser.add_argument('-m','--mainframe', help='target IP address or Hostname and port: TARGET[:PORT] default port is 23',dest='target')
parser.add_argument('-f','--file', help='a file containing a listing of hosts[:ports] to connect to.',dest='hosts')
parser.add_argument('-s','--sleep',help='Seconds to sleep between actions (increase on slower systems). The default is 1 second.',default=1,type=int,dest='sleep')
#parser.add_argument('-t','--tor',help='Use TOR proxy to connect. Syntax is TYPE:HOSTNAME:PORT for any TOR proxy. Most likely socks5d:localhost:9050',dest='tor')
args = parser.parse_args()
results = parser.parse_args() # put the arg results in the variable results


#if results.tor is not None: # Create the argument to pass s3270
#	tor_proxy = '-proxy ' + results.tor


if platform.system() == 'Darwin': #'Darwin'
	class Emulator(EmulatorBase):
		s3270_executable = 'MAC_Binaries/s3270'
		#if results.tor is not None: s3270_args = ['tor_proxy']
elif platform.system() == 'Linux':
	class Emulator(EmulatorBase):
		s3270_executable = '/usr/bin/s3270' #this assumes s3270 is in your $PATH. If not then you'll have to change it
		#if results.tor is not None: s3270_args = ['tor_proxy']
elif platform.system() == 'Windows':
	class Emulator(EmulatorBase):
		s3270_executable = 'Windows_Binaries/ws3270.exe'
		#if results.tor is not None: s3270_args = ['tor_proxy']
else:
	print t.red + t.bold + '      [!] Your Platform:', platform.system(), 'is not supported at this time. Windows support should be available soon' + t.normal
	sys.exit()


if not results.target and not results.hosts:
	print t.red + t.bold + '      [!] You gotta specify a host or a file. Try -h for help.' + t.normal
	sys.exit()

if not results.hosts:
	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Target:',
	print t.white(results.target) + t.normal
	print t.green_bold + '      [   ] Multiple targets file:' + t.normal
if not results.target:
	print t.green_bold + '      [   ] Target:'
	print t.green_bold + '      [' + t.white_bold + ' X ' + t.green +'] Multiple targets file:', 
	print t.white(results.hosts) + t.normal
	
if results.sleep > 1:
	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Sleep set to:',
	print t.white(str(results.sleep)) + t.normal
else:
	print  t.green_bold + '      [   ] Sleep set to:',
	print t.white(str(results.sleep)) + t.normal

#if results.tor is not None:
#	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Tor Proxy:',
#	print t.white(results.tor) + t.normal
#else:
#	print t.green_bold + '      [   ] Tor Proxy:' + t.normal


print ''

if not results.hosts: #enter single server mode	
	em = Emulator()
	print t.blue_bold + '      +     Connecting to:',
	print t.white(results.target)	
	try:
		Connect_to_ZOS(results.target)
		print t.green_bold('      +     Connected')
		print t.blue_bold + '      +     Grabbing screen to', 
		print t.white(results.target + '.html')
		Grab_Screen(results.target)	
		em.terminate()
	except Exception:
		print t.red + t.bold + '      [!] Connection to:', results.target, 'FAILED!' + t.normal
	except IOError:
		print t.red + t.bold + '      [!] Connection to TOR proxy:', results.tor, 'FAILED!' + t.normal
	
else:
	hostsfile=open(results.hosts) #open the usernames file
	for hostnames in hostsfile:
		em = Emulator()
		print t.blue_bold + '      +     Connecting to:',
		print t.white(hostnames.strip())	
		try:
			Connect_to_ZOS(hostnames.strip())
			print t.green_bold('      +     Connected')
			print t.blue_bold + '      +     Grabbing screen to', 
			print t.white(hostnames.strip() + '.html')
			Grab_Screen(hostnames.strip())
			em.terminate() # And we're done. Close the connection
		except IOError:
			print t.red + t.bold + '      [!] Connection to TOR proxy:', results.tor, 'FAILED!' + t.normal
		except Exception, err:
			print t.red + t.bold + '      [!] Connection to:', hostnames.strip(), 'FAILED!' + t.normal
