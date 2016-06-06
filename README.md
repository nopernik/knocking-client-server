# knocking-client-server
Knocking server in 50 lines with scapy 

It will listen to RAW packet data with specific passphrase, then if found it will do whatever you want.
With support of multiple clients in parallel.

# Dependencies:
iptables, python-scapy

# Config:

iptables -P INPUT DROP

iptables -A INPUT -i lo -j ACCEPT
