
import socket
import pystray
import PIL.Image
import customtkinter
#from main import center, deicon

def reachout():
    ip = socket.gethostbyname(socket.gethostname())
    port = 5050
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    server.send(bytes(str(socket.gethostname()), "utf-8"))
    #while socket is connected or server is accessible
    while True:
        msg = input("Enter string: ")
        server.send(bytes(msg, "utf-8"))

    server.close()

if __name__ == "__main__":
    reachout()
    print("test")