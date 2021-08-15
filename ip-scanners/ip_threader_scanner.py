import socket
import time
import threading
from queue import Queue

#Scanning activity
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = s.connect((target_IP, port))
        with print_lock:
            print(port, 'is open')
        connection.close()
    except:
        pass

 #Threads activity
 #Every thread get a port from the queue and scans it
def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

#validate input Ip addr
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

# Getting User Inputs : IP, start port, last port
target = input('Enter the IP addr to be scanned: ')
target_start_port = input('Enter first port to scan: ')
target_last_port = input('Enter last port to scan: ')

#Validates inputs
check_start = target_start_port.isnumeric
check_last = target_last_port.isnumeric
check_ip = validate_ip(target)
check_major = int(target_last_port)>int(target_start_port)
valid_inputs = check_ip and check_last and check_start and check_major and target_last_port < 50000 and target_start_port < 50000
if(valid_inputs):

    #starting scan
    target_IP = socket.gethostbyname(target)
    print ('Starting scan on host: ', target_IP)

    #create queue
    q = Queue()
    startTime = time.time()

    #creating threads
    for x in range(100):
        t = threading.Thread(target = threader)
        t.daemon = True
        t.start()

    #scanning from start to finish
    #entering every port inside the queue
    for worker in range(int(target_start_port), int(target_last_port)):
        q.put(worker)
    
    q.join()
    print('Time taken:', time.time() - startTime)
else:
    print("bad inputs: Host  must be and IP addr, ports must be numerics and <50000 and first port < last port ")