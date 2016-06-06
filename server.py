#!/usr/bin/python
#
# Knocking Server in 50 lines vs scapy (without comments and white spaces :)
# __author__: Alexander Korznikov
# Distribute/modify/upgrade as you wish.
#

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import os
import time
from threading import Thread

PASSPHRASE = 'open sesame' # it is your password, should be identical in agent.py
TIMEOUT = 10    # time out for an IP address to delete from list and block access

class z:
   targets = {} # {x.x.x.x:{timestamp:xxxxx,active:Bool,closed:Bool} }
   pass
   
def open_access(ip):
   print 'Opening %s' % ip   #do something with this ip like:  
   #os.system('iptables -A INPUT -s %s -p 22 -j ACCEPT' % ip)

def close_access(ip):
   print 'Closing %s' % ip   #do something with this ip like:  
   #os.system('iptables -D INPUT -s %s -p 22 -j ACCEPT' % ip)

def start_sniff(null):   
   def check(pkt):
      try:
         if pkt.load.decode('hex') == PASSPHRASE:
            ip = pkt['IP'].src
            if not ip in z.targets.keys():
               z.targets.update({ip:{'closed': True}})
            z.targets[ip].update({'timestamp':time.time()})
            if z.targets[ip]['closed'] == True:         # do not open access again for specific IP (only once)
               z.targets[ip].update({'closed': False})
               z.targets[ip].update({'active': True})
               open_access(pkt['IP'].src)
      except:
         pass
   sniff(prn=check, filter='udp')
      
print 'Starting sniffer...'
sniffer = Thread(target=start_sniff, args=(0,))
sniffer.start()

try:
   while 1:
      print 'Active clients: %d %s' % (len(z.targets.keys()),', '.join(z.targets.keys()))
      for ip in z.targets.keys():
         try:
            if z.targets[ip]['closed'] == False and z.targets[ip]['active']:
               if (time.time() - z.targets[ip]['timestamp']) > 10:
                  close_access(ip)  
                  del z.targets[ip]
         except KeyError:
            pass
      time.sleep(TIMEOUT)

except KeyboardInterrupt:
   os.kill(os.getpid(),15)      # easy way to stop sniff() :)