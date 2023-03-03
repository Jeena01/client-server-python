from socket import *;
HOST = '127.0.0.1'
PORT=12000
# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)

print("Started ftp client...")

def openconn(port_number):
  try:
    print("opening connection on ", port_number)
    PORT = int(port_number)
    sock.connect((HOST, PORT))
    print("connection opened")
  except:
    print("Could not open connection on requested port number")

def get(filename):
  try:
    s="PUT"
    sock.sendall(s.encode("utf-8"))
  except:
    print("Make sure connection is established")
    return
  try:
    sock.send(filename.encode("utf-8"))
    response=sock.recv(1024).decode()
    if(response=="false"):
      print("File does not exist on server.")
      return
    file = open(filename,"wb")
    file_bytes = b""
    done=False
    while not done:
      data= sock.recv(1024)
      if file_bytes[-5:] == b"<EOF>":
        done=True
      else:
        file_bytes+=data
    file.write(file_bytes[:-5])
  except:
    print("error retrieving file")
  

def put(filename):
  print("Uploading, ",filename)
  try:
    file=open(filename,"rb")
  except:
    print("File does not exist")
    return
  try:
    s="PUT"
    sock.sendall(s.encode("utf-8"))
  except:
    print("Make sure connection is established")
  try:
    sock.send(filename.encode("utf-8"))
    data=file.read()
    sock.sendAll(data)
    sock.send(b"<EOF>")
    print("uploaded file successfully")
  except:
    print("error uploading file")


def close():
  print("closing")
  s="CLOSE"
  try:
    sock.sendall(s.encode("utf-8"))
    sock.close()
  except:
    print("Make sure connection is established")


def quit():
  print("quitting")
  try:
    s="QUIT"
    sock.sendall(s.encode("utf-8"))
    sock.close()
  except:
    print("Make sure connection is established")

while True:
  prompt = input("\n Enter command: ")
  if prompt[:4].upper()=="OPEN":
    openconn(prompt[5:])
  elif prompt[:3].upper()=="GET":
    get(prompt[4:])
  elif prompt[:3].upper()=="PUT":
    put(prompt[4:])
  elif prompt[:5].upper()=="CLOSE":
    close()
  elif prompt[:4].upper()=="QUIT":
    quit()