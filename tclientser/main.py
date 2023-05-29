import customtkinter
import tkinter as tk
import client
import pystray
import PIL.Image
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from socket import *
import socket as socket1
#socket import * overlaps with import socket, import * is needed for initiatinng server, socket1 is needed for shutdownz
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
from PIL import Image, ImageTk
import cv2
import threading
from threading import Thread


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.deiconify()


# Show main app window
def deicon():
    icon.stop()
    app.iconify()
    app.deiconify()


# MAIN


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Drowsiness App")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        # self.app = customtkinter.CTk()
        self.screen_width = int(self.winfo_screenwidth() * 0.3)
        self.screen_height = int(self.winfo_screenheight() * 0.2)
        self.eval("tk::PlaceWindow . center")
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        # self.app.grid_columnconfigure(0, weight=1)
        # self.app.grid_rowconfigure(2, weight=1)

        # Initialize
        frame = customtkinter.CTkFrame(self)
        # self.frame.grid_propagate(False)

        self.label = customtkinter.CTkLabel(
            frame, text="Select mode", text_color="white"
        )

        self.button = customtkinter.CTkButton(
            frame, text="Student", command=self.clientrun
        )
        self.button1 = customtkinter.CTkButton(frame, text="Server", command=self.serverrun)

        # Grid Placement
        frame.pack(pady=10)

        self.label.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        self.button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.grid_columnconfigure((0, 3), weight=1)
        center(self)
        self.resizable(False, False)

    def onCloseOtherFrame(self, otherFrame):
        # cap.release()
        otherFrame.destroy()
        app.iconify()
        app.deiconify()
        if (server):
            server.close()
        try:
            print("do_run to false, stop server thread")
            th.do_run = False
            hostSocket.shutdown(socket1.SHUT_RDWR)
            hostSocket.close()
        except Exception as e:
            print(e)

    def checkevent(self, event):
        print("iconify")
        startTray(stuapp)

    def update_gui(self, image):
        photo.paste(image)

    def refresh(self):
        global server
        try:
            server.close()
        except error:
            print("not yet connected", error)
            stuapp.label1.configure(text = "Connection Status: Not Connected")
        try: 
            ip = socket1.gethostbyname(socket1.gethostname())
            port = 5050
        
            server = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
            server.connect((ip, port))
            server.send(bytes(str(socket1.gethostname()), "utf-8"))
            #change to server send pc name as connection status
            stuapp.label1.configure(text = f"Connection Status: Connected at {socket1.gethostname()}")
        except error:
            print(error)
            print("error connecting, please refresh")

    def update_frame(self, face_mesh, cap, k):
        # while cap.isOpened():
        success, image = cap.read()
        try:
            image = image[:, :, ::-1]
        except:
            print("imageread")

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                )
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
                )
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
                )
        # Flip the image horizontally for a selfie-view display.
        mesh_image = cv2.flip(image, 1)
        image = Image.fromarray(mesh_image)
        self.update_gui(image)
        #print(k)
        #k += 1
        stuapp.after(1, lambda: self.update_frame(face_mesh, cap, k))

    def start_frame(self, frame):
        global ip, server
        try: 
            ip = socket1.gethostbyname(socket1.gethostname())
            port = 5050
        
            server = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
            server.connect((ip, port))
            server.send(bytes(str(socket1.gethostname()), "utf-8"))
            stuapp.label1.configure(text = f"Connection Status: Connected at {socket1.gethostname()}")
        except error:
            print(error)
            print("error connecting, please refresh")
        

        stuapp.button3.configure(state=tk.DISABLED)
        global cap
        cap = cv2.VideoCapture(0)
        ret, imgframe = cap.read()
        imgframe = imgframe[:, :, ::-1]
        image = Image.fromarray(imgframe)
        global photo
        photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(frame, width=photo.width(), height=photo.height())
        canvas.grid(row=5, column=0, columnspan=2)
        canvas.create_image((0, 0), image=photo, anchor="nw")
        self.update_frame(face_mesh, cap, 1)

    def stop_frame(self):
        cap.release()
        stuapp.button3.configure(state=tk.NORMAL)

    def clientrun(self, *args):
        global handler, stuapp, face_mesh
        self.withdraw()
        stuapp = customtkinter.CTkToplevel()
        stuapp.title("Student Client")
        handler = lambda: self.onCloseOtherFrame(stuapp)
        stuapp.protocol("WM_DELETE_WINDOW", handler)
        sw = int(stuapp.winfo_screenwidth() * 0.5)
        sh = int(stuapp.winfo_screenheight() * 0.7)
        x = (self.winfo_screenwidth() / 2) - (sw / 2)
        y = (self.winfo_screenheight() / 2) - (sh / 2)
        stuapp.geometry(f"{sw}x{sh}+{x}+{y}")
        # Initialize
        frame = customtkinter.CTkFrame(
            stuapp, width=self.screen_width, height=self.screen_height
        )

        stuapp.label = customtkinter.CTkLabel(
            frame, text="Student Dashboard", text_color="white"
        )
        stuapp.label1 = customtkinter.CTkLabel(
            frame, text="Connection Status: Not Connected", text_color="white"
        )

        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        stuapp.button1 = customtkinter.CTkButton(
            frame, text="Reselect Mode", command=handler
        )
        stuapp.button2 = customtkinter.CTkButton(
            frame, text="Minimize to Tray", command=lambda: startTray(stuapp)
        )

        # threading.Thread(target=self.update_frame(face_mesh,cap,k)).start()
        stuapp.button3 = customtkinter.CTkButton(
            frame, text="Start Detecting", command=lambda: self.start_frame(frame)
        )
        stuapp.button4 = customtkinter.CTkButton(
            frame, text="Stop Detecting", command=lambda: self.stop_frame()
        )
        stuapp.button5 = customtkinter.CTkButton(
            frame, text="Refresh Connection", command=lambda: self.refresh()
        )

        # add camera output, detect and select camera
        # status check
        # detect and connect to client

        # Grid Placement
        frame.pack(pady=10)

        stuapp.label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        stuapp.label1.grid(row=2, column=0,  padx=20, pady=5, sticky="ew")
        stuapp.button5.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        stuapp.button1.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        stuapp.button2.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        stuapp.button3.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        stuapp.button4.grid(row=4, column=1, padx=20, pady=10, sticky="ew")
        stuapp.grid_columnconfigure((0, 4), weight=1)
        # stuapp.resizable(False, False)
        # use working_ports
        # available_ports,working_ports,non_working_ports = list_ports()

        
        self.start_frame(frame)
        # For webcam input:
        # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def serverrun(self, *args):
        global handler, serapp, face_mesh, clients
        t = Thread(target=lambda: self.serverthread())
        t.start()
        clients = set()
        self.withdraw()
        serapp = customtkinter.CTkToplevel()
        serapp.title("Server Client")
        handler = lambda: self.onCloseOtherFrame(serapp)
        serapp.protocol("WM_DELETE_WINDOW", handler)
        sw = int(serapp.winfo_screenwidth() * 0.7)
        sh = int(serapp.winfo_screenheight() * 0.8)
        x = (self.winfo_screenwidth() / 2) - (sw / 2)
        y = (self.winfo_screenheight() / 2) - (sh / 2)
        serapp.geometry(f"{sw}x{sh}+{x}+{y}")
        frame = customtkinter.CTkFrame(
            serapp, width=self.screen_width, height=self.screen_height
        )

        serapp.label = customtkinter.CTkLabel(
            frame, text="Server Dashboard", text_color="white"
        )
        serapp.button1 = customtkinter.CTkButton(
            frame, text="Reselect Mode", command=handler
        )

        # Grid Placement
        frame.pack(pady=10)

        serapp.label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        serapp.button1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        #pc1 = ClientPC(serapp)

    def serverthread(self):
        global th, hostSocket
        hostSocket = socket(AF_INET, SOCK_STREAM)
        hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        hostIp = socket1.gethostbyname(socket1.gethostname())
        gethostname = "test123"
        portNumber = 5050
        hostSocket.bind((hostIp, portNumber))
        hostSocket.listen()
        print ("Waiting for connection...")
        th = threading.current_thread()
        while getattr(th, "do_run", True):
            print("hello")
            clientSocket, clientAddress = hostSocket.accept()
            clients.add(clientSocket)
            print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
            newframe = ClientPC(serapp, gethostname)
            thread = Thread(target=clientThread, args=(clientSocket, clientAddress, newframe))
            thread.start()
        
        #it doesnt reach here
        print("socket down exit loop")

def clientThread(clientSocket, clientAddress, clientframe):
    while True:
        message = clientSocket.recv(1024).decode("utf-8")
        print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
        for client in clients:
            if client is not clientSocket:
                client.send((clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message).encode("utf-8"))

        if not message:
            clientframe.forget()
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break

    clientSocket.close()

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while (
        len(non_working_ports) < 5
    ):  # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print(
                    "Port %s is working and reads images (%s x %s)" % (dev_port, h, w)
                )
                working_ports.append(dev_port)
            else:
                print(
                    "Port %s for camera ( %s x %s) is present but does not reads."
                    % (dev_port, h, w)
                )
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports, non_working_ports


# CLIENT AREA
def exit_action(icon, stuapp):
    print("Closing tray")
    icon.visible = False
    icon.stop()
    app.destroy()


def showstudent_closetray(stuapp):
    icon.visible = False
    icon.stop()
    stuapp.deiconify()


def startTray(stuapp):
    global icon
    stuapp.withdraw()
    image = PIL.Image.open("drowsiness-detection/tclientser/images/awake-logo.png")
    icon = pystray.Icon(
        "Awake",
        image,
        menu=pystray.Menu(
            pystray.MenuItem(
                "Show App", lambda: showstudent_closetray(stuapp), default=True
            )
        ),
    )
    icon.run()

class ClientPC(customtkinter.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        # Initialize
        # self.frame.grid_propagate(False)

        self.label = customtkinter.CTkLabel(
            self, text=f"PC #: {name}", text_color="white"
        )
        self.label1 = customtkinter.CTkLabel(
            self, text=f"Status: ", text_color="white"
        )

        self.button = customtkinter.CTkButton(
            self, text="Student", command=print("s")
        )
        self.button1 = customtkinter.CTkButton(self, text="Server", command=print("s"))

        # Grid Placement
        self.pack(pady=10)

        self.label.grid(row=0, column=0, columnspan = 2, padx=20, pady=5, sticky="ew")
        self.label1.grid(row=0, column=2, padx=20, pady=5, sticky="ew")
        #button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.button1.grid(row=0, column=3, padx=20, pady=10, sticky="ew")
        #grid_columnconfigure((0, 3), weight=1)

    def forget(self):
        self.label.destroy()
        self.label1.destroy()
        self.button1.destroy()
        self.destroy()
        print("frame removed")


if __name__ == "__main__":
    global app
    app = App()
    app.mainloop()
