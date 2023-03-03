from socket import *
HOST = '127.0.0.1'
PORT = 12000
# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)
print("Started ftp server...")
sock.bind((HOST, PORT))
sock.listen()
# listen for a connection
conn, addr = sock.accept()

print("Connected to " , addr)

def close():
  conn.close()


def quit():
  conn.close()
  sock.close()

def put():
  
  filename=conn.recv(1024).decode()
  print("Uploading ",filename)
  #file_size=conn.recv(1024).decode()

  file = open(filename,"wb")
  print("opened")
  file_bytes = b""
  done=False
  while not done:
    data= conn.recv(1024)
    if file_bytes[-5:] == b"<EOF>":
      done=True
    else:
      file_bytes+=data
  print("write successful")
  file.write(file_bytes[:-5])




def get():
  print("get")
  filename=conn.recv(1024)
  try:
    file=open(filename,"rb")
    conn.send("true".encode("utf-8"))
    data=file.read
    conn.sendall(data)
    sock.send(b"<EOF>")
  except:
    conn.send("false".encode("utf-8"))

    



while (True):
 data = conn.recv(1024).decode("utf-8").upper()
 #print(data)
 conn.sendall(data.encode("utf-8"))
 if data == "QUIT":
    quit()
 elif data== "CLOSE":
   close()
 elif data== "GET":
   get()
 elif data== "PUT":
   put()



