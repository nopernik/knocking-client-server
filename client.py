#!/usr/bin/python

from random import randint
import time
import socket

# Knocking server's IP address
IPADDR = '127.0.0.1'

PASSPHRASE = 'open sesame'

def send_packet():
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
   s.connect((IPADDR, randint(1000,65535)))
   s.send(PASSPHRASE.encode('hex'))
   s.close()

while 1:
   send_packet()
   time.sleep(5)

