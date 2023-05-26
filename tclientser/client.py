
import socket
import pystray
import PIL.Image
import customtkinter
#from main import center, deicon

def reachout():
    ip = "127.0.0.1"
    port = 7500
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    string = input("Enter string: ")
    server.send(bytes(string, "utf-8"))

    server.close()

if __name__ == "__main__":
    reachout()
    print("test")