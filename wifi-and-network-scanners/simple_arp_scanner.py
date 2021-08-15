from scapy.all import ARP, Ether, srp

#IP addr for the local network
target_ip = "192.168.1.1/24"

# create ARP packet
arp = ARP(pdst=target_ip)

# create the Ether broadcast packet
ether_broadc = Ether(dst="ff:ff:ff:ff:ff:ff")

# stacking them
packet = ether_broadc/arp

#sending and reciving packets
recived = srp(packet, timeout=3, verbose=0)[0]


network_devices = []

for sent, received in recived:
    # for each response, append ip and mac address to the list
    network_devices.append({'ip': received.psrc, 'mac': received.hwsrc})

# print network_devices
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for device in network_devices:
    print("{:16}    {}".format(device['ip'], device['mac']))