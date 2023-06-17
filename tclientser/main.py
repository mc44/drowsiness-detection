import customtkinter
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
import tkinter
from tkinter import messagebox, ttk
import re
from datetime import datetime
from pythonping import ping
import dbcalls
from notifypy import Notify
import getmodelverdict
import sqlite3

right_eye_landmarks = [33, 246, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
left_eye_landmarks = [362, 382, 381, 380, 374, 373, 390, 249, 466, 388, 387, 386, 385, 384, 398]
mouth_landmarks = [13, 14, 312, 317, 82, 87, 178, 402, 311, 81, 88, 95, 183, 42, 78, 318, 310, 324, 415, 308]
framecount = 1500
frame_reset_threshold = 900
currentstatus = "normal"
HEADERSIZE = 10
globalqueryqueue = []
cur_user = ""
cur_session = ""
global_stop = False

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

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

# MAIN


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.currentuser = ""
        self.session = ""
        #vars
        self.server = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)

        self.title("Drowsiness App")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        # self.app = customtkinter.CTk()
        self.screen_width = int(self.winfo_screenwidth() * 0.5)
        self.screen_height = int(self.winfo_screenheight() * 0.4)
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
        self.label1 = customtkinter.CTkLabel(
            frame, text="PC User", text_color="white"
        )
        self.entry = customtkinter.CTkEntry(frame, placeholder_text="FName LName")

        self.button = customtkinter.CTkButton(
            frame, text="Student", command=self.clientrun
        )
        self.button1 = customtkinter.CTkButton(frame, text="Server", command=self.serverrun)

        # Grid Placement
        frame.pack(pady=30)

        self.label.grid(row=0, column=0, columnspan = 2, padx=20, pady=5, sticky="ew")
        self.label1.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        self.button.grid(row=2, column=0, columnspan = 2,padx=20, pady=10, sticky="ew")
        self.button1.grid(row=3, column=0, columnspan = 2,padx=20, pady=10, sticky="ew")
        self.grid_columnconfigure((0, 4), weight=1)
        center(self)
        self.resizable(False, False)

        notification = Notify()
        notification.title = "Welcome to the App"
        notification.message = "Please select on whether you are a client or a server user!"
        notification.send()

    def validate(self):
        val = re.search("^[\w\d_-]+$", self.entry.get())
        #print(self.entry.get(), val)
        if (val is None):
            messagebox.showwarning(title="No name input", message="Please write a value in the PC User entry. Thanks")
            return False
        else:
            self.currentuser = self.entry.get()
            return True
        
    def validatelogin(self):
        val = re.search("^[\w\d_-]+$", self.entry.get())
        #print(self.entry.get(), val)
        if (val is None):
            messagebox.showwarning(title="No name input", message="Please write a value in the PC User entry. Thanks")
            return False
        else:
            #check if user exists
            text = ""
            result = dbcalls.get("Account", ["Name"], f"WHERE Name='{self.entry.get()}'")
            #print(result,"here")
            if result:
                dialog = customtkinter.CTkInputDialog(text="Type in password:", title="Login")
                text = dialog.get_input()
                if text != None:
                    if dbcalls.login(self.entry.get(),text):
                        self.currentuser = self.entry.get()
                        return True
            else:
                dialog = customtkinter.CTkInputDialog(text="Create a password:", title="Register")
                text = dialog.get_input()
                if text != None:
                    val = re.search("^[\w\d_-]+$", text)
                if val == None or text == None:
                    return False
                dbcalls.register(self.entry.get(), text)
                return True
        return False
    
    def inputserver_ip(self):
        dialog = customtkinter.CTkInputDialog(text="Input server private IP:", title="Ask for the server ip")
        self.server_ip = dialog.get_input()
        val = re.search("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d).){3}(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$", self.server_ip)
        #print(self.entry.get(), val)
        if (val is None):
            messagebox.showwarning(title="No input", message="Please input the server ip. Thanks")
            return False
        else:
            self.currentuser = self.entry.get()
            return True

    def onCloseOtherFrame(self, otherFrame):
        # cap.release()
        otherFrame.destroy()
        app.iconify()
        app.deiconify()
        if (self.server):
            self.server.close()
        try:
            global global_stop
            global_stop = True
            commitquery_queue()
            print("do_run to false, stop server thread")
            th.do_run = False
            ip = socket1.gethostbyname(socket1.gethostname())
            port = 5050
            test = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
            test.connect((ip, port))
            test.send(bytes(pack("0"+str(socket1.gethostname())), "utf-8"))
            test.close()
            
            #self.hostSocket.shutdown(socket1.SHUT_RDWR)
            #self.hostSocket.close()
        except Exception as e:
            print(e)

    def checkevent(self, event):
        print("iconify")
        startTray(stuapp)

    def update_gui(self, image):
        photo.paste(image)

    def refresh(self):
        try:
            self.server.close()
        except error:
            print("not yet connected", error)
            stuapp.label1.configure(text = "Connection Status: Not Connected")
        try: 
            ip = socket1.gethostbyname(socket1.gethostname())
            port = 5050
        
            self.server = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
            self.server.connect((ip, port))
            self.server.send(bytes(pack(str(socket1.gethostname())), "utf-8"))
            #change to server send pc name as connection status
            stuapp.label1.configure(text = f"Connection Status: Connected at {socket1.gethostname()}")
        except error:
            print(error)
            print("error connecting, please refresh")

    def update_frame(self, face_mesh, cap, nofaceframes, frames):
        # while cap.isOpened():
        success, image = cap.read()
        try:
            image = image_resize(image, height = 480)
            image = image[:, :, ::-1]
        except:
            print("imageread")
            self.run_status = False
        height = image.shape[0]
        width = image.shape[1]
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)
        lm_coord = []
        if results.multi_face_landmarks:
            for facial_landmarks in results.multi_face_landmarks:
                landmarks = facial_landmarks.landmark
                for i, landmark in enumerate(landmarks):
                    if i not in left_eye_landmarks and i not in right_eye_landmarks and i not in mouth_landmarks:
                        continue
                    x = landmark.x
                    y = landmark.y

                    cv2.circle(image, (int(landmark.x * width), int(landmark.y * height)), 2, (100,100,0), -1)
                    lm_coord.append([x, y])
            frames.append(lm_coord)
        else:
            nofaceframes+=1
            if nofaceframes>=frame_reset_threshold:
                frames = []
                nofaceframes = 0
                self.server.send(bytes(pack("1"+str("no_face")), "utf-8"))
        #model process
        #frame_coordinates = getmodelverdict.ExtractEyeAndMouthLandmarks(results, False)
        #frames.append(frame_coordinates)
        if len(frames)%100 == 0:
            print(len(frames))
        if len(frames)>framecount:
            t = Thread(target=lambda: getmodelverdict.modelpredict(frames,self), daemon = True)
            t.start()
            frames = []
            end_time = time.time()
            # Calculate the elapsed time
            elapsed_time = end_time - self.start_time
            print(elapsed_time)
            

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        
        mesh_image = cv2.flip(image, 1)
        image = Image.fromarray(mesh_image)
        self.update_gui(image)
        #print(k)
        #k += 1
        #decide result here
        #make format of things sent
        #self.server.send(bytes(pack(str("1result placeholder"+str(datetime.now()))), "utf-8"))
        if self.run_status:
            stuapp.after(1, lambda: self.update_frame(face_mesh, cap, nofaceframes, frames))
        else:
            print("loop stopped")
            #self.server.send(bytes(pack(str("1camera disconnect"+str(datetime.now()))), "utf-8"))


    def start_frame(self, frame):
        print("here atleast1")
        self.run_status = False
        global ip
        try: 
            server_ip = self.server_ip
            print(server_ip)
            #ip = socket1.gethostbyname(socket1.gethostname())
            port = 5050
        
            self.server = socket1.socket(socket1.AF_INET, socket1.SOCK_STREAM)
            self.server.connect((server_ip, port))
            self.server.send(bytes(pack("0"+str(self.entry.get())), "utf-8"))
            stuapp.label1.configure(text = f"Connection Status: Connected at {socket1.gethostname()}")
            #print(ping(server_ip, verbose=True))
        except error:
            print(error)
            print("error connecting, please refresh")
            return False

        self.initiate_frame(frame)    
        return True

        
    def initiate_frame(self,frame):
        print("here atleast")
        stuapp.button3.configure(state=tkinter.DISABLED)
        global cap
        cap = cv2.VideoCapture(int(self.optionmenu.get()))
        if not(cap is None or not cap.isOpened()):
            ret, imgframe = cap.read()
            imgframe = image_resize(imgframe, height = 480)
            imgframe = imgframe[:, :, ::-1]
            
            image = Image.fromarray(imgframe)
            global photo
            photo = ImageTk.PhotoImage(image)
            canvas = tkinter.Canvas(frame, width=photo.width(), height=photo.height())
            canvas.grid(row=2, column=0, columnspan=3)
            canvas.create_image((0, 0), image=photo, anchor="nw")
            self.run_status = True
            # Record the start time
            self.start_time = time.time()

            stuapp.after(2, lambda: self.update_frame(face_mesh, cap, 0, []))

    def stop_frame(self):
        try:
            cap.release()
            stuapp.button3.configure(state=tkinter.NORMAL)
        except:
            pass

    def clientrun(self, *args):
        if (not(self.validate())):
            return
        if (not(self.inputserver_ip())):
            return
        available_ports,working_ports,non_working_ports = list_ports()
        print(available_ports,working_ports,non_working_ports)
        #self.optionmenu_var = customtkinter.StringVar(value=working_ports[0])
        ports = [str(x) for x in working_ports]
        if working_ports==[]:
            messagebox.showwarning(title="No camera detected", message="Please make sure that a camera is available for use.")
            return
        global handler, stuapp, face_mesh
        self.withdraw()
        self.run_status = False
        stuapp = customtkinter.CTkToplevel()
        stuapp.title("Student Client")
        handler = lambda: self.onCloseOtherFrame(stuapp)
        stuapp.protocol("WM_DELETE_WINDOW", handler)
        self.sw = int(stuapp.winfo_screenwidth() * 0.8)
        self.sh = int(stuapp.winfo_screenheight() * 0.9)
        x = (self.winfo_screenwidth() / 2) - (self.sw / 2)
        y = (self.winfo_screenheight() / 2) - (self.sh / 2)
        stuapp.geometry(f"{self.sw}x{self.sh}+{x}+{y}")
        # Initialize
        mainframe = customtkinter.CTkFrame(
            stuapp, width=self.screen_width, height=self.screen_height
        )
        frame = customtkinter.CTkFrame(
            mainframe, width=self.screen_width, height=self.screen_height
        )
        frame1 = customtkinter.CTkFrame(
            mainframe, width=self.screen_width, height=self.screen_height
        )
        frame2 = customtkinter.CTkFrame(
            mainframe, border_color = '#00000', width = 10
        )

        stuapp.label = customtkinter.CTkLabel(
            frame, text=f"Student Dashboard: {self.entry.get()}", text_color="white"
        )
        stuapp.label1 = customtkinter.CTkLabel(
            frame, text="Connection Status: Not Connected", text_color="white"
        )
        stuapp.label2 = customtkinter.CTkLabel(
            frame1, text="Select Working Camera: ", text_color="white"
        )
        stuapp.label3 = customtkinter.CTkLabel(
            frame1, text="Camera ", text_color="white"
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
        # threading.Thread(target=self.update_frame(face_mesh,cap,k)).start()
        stuapp.button3 = customtkinter.CTkButton(
            frame1, text="Start Detecting", command=lambda: self.start_frame(mainframe)
        )
        stuapp.button4 = customtkinter.CTkButton(
            frame1, text="Stop Detecting", command=lambda: self.stop_frame()
        )
        #stuapp.button5 = customtkinter.CTkButton(
        #    frame, text="Refresh Connection", command=lambda: self.press
        #)
        
        self.optionmenu = customtkinter.CTkOptionMenu(frame1, values=ports, command=self.press )#, variable=self.optionmenu_var)
        
        # add camera output, detect and select camera
        # status check
        # detect and connect to client

        # Grid Placement
        mainframe.pack(pady=10)
        frame.grid(row=0, column=0,padx=5)
        frame2.grid(row=0, column=1,padx=5)
        frame1.grid(row=0, column=2,padx=5)
        #frame.pack(pady=10)
        #frame1.pack(pady=5)

        #frame
        stuapp.label.grid(row=0, column=0, columnspan=2 , padx=20, pady=5, sticky="ew")
        stuapp.label1.grid(row=2, column=0, columnspan=2 , padx=20, pady=5, sticky="ew")
        #stuapp.button5.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        stuapp.button1.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        #frame1
        stuapp.label3.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        stuapp.button3.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        stuapp.button4.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        stuapp.label2.grid(row=2, column=0,  padx=20, pady=5, sticky="ew")
        self.optionmenu.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        self.optionmenu.set("0")

        #mixed with frame (old ui)
        #stuapp.button3.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        #stuapp.button4.grid(row=4, column=1, padx=20, pady=10, sticky="ew")
        #stuapp.label2.grid(row=5, column=0,  padx=20, pady=5, sticky="ew")
        #self.optionmenu.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        
        stuapp.grid_columnconfigure((0, 4), weight=1)
        check = stuapp.button3.invoke()
        if not check:
            messagebox.showwarning(title="Can't find Server", message="Please make sure that a server application is running on the network, or you are connected to the same network.")
            self.onCloseOtherFrame(stuapp)
        # stuapp.resizable(False, False)
        # use working_ports
        
        #self.start_frame(frame)
        # For webcam input:
        # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    
    def changesession(self,serapp=""):
        global cur_session
        dialog = customtkinter.CTkInputDialog(text="Input Session name for db record:", title="Session Name")
        self.session = dialog.get_input()
        cur_session = self.session
        if serapp!="":
            serapp.label2.configure(text=f"Current Session: {self.session}")
    
    def press(self, a):
        self.stop_frame()
        stuapp.button3.invoke()

    def serverrun(self, *args):
        if (not(self.validatelogin())):
            return
        global handler, serapp, face_mesh, clients
        self.changesession()
        t = Thread(target=lambda: self.serverthread(), daemon = True)
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
            frame, text=f"User: {self.entry.get()}", text_color="white"
        )
        
        serapp.label1 = customtkinter.CTkLabel(
            frame, text=f"Current Ip: {socket1.gethostbyname(socket1.gethostname())}", text_color="white"
        )
        serapp.label2 = customtkinter.CTkLabel(
            frame, text=f"Current Session: {self.session}", text_color="white"
        )
        serapp.button1 = customtkinter.CTkButton(
            frame, text="Reselect Mode", command=handler
        )
        serapp.button2 = customtkinter.CTkButton(
            frame, text="See History", command=self.history
        )
        serapp.button3 = customtkinter.CTkButton(
            frame, text="Change Session", command=lambda:self.changesession(serapp)
        )

        # Grid Placement
        frame.pack(pady=10)

        serapp.label.grid(row=0, column=0, padx=20, pady=5, sticky="ew")
        serapp.label1.grid(row=0, column=1, padx=20, pady=5, sticky="ew")
        serapp.button1.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        serapp.button2.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        serapp.button3.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        serapp.label2.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.scrollable = customtkinter.CTkScrollableFrame(serapp, width = 1000, height=700)
        self.scrollable.pack(pady=10)
        global cur_user
        cur_user = self.entry.get()
        #print(cur_user,"1")
        #pc1 = ClientPC(self.scrollable, "testasdasdasdasdasdsad")
        #pc2 = ClientPC(self.scrollable, "asd")
        #pc3 = ClientPC(self.scrollable, "qwe")
        #pc4 = ClientPC(self.scrollable, "zxc")
        runsql_forinterval(serapp)

    def calltree(self, my_tree, user, search):
        dbcalls.filltree(my_tree,user,self.optionmenu.get(),search)

    def history(self):
        serapp.iconify()
        sw = int(serapp.winfo_screenwidth() * 0.6)
        sh = int(serapp.winfo_screenheight() * 0.7)
        x = (self.winfo_screenwidth() / 2) - (sw / 2)
        y = (self.winfo_screenheight() / 2) - (sh / 2)
        self.histapp = customtkinter.CTkToplevel(serapp)
        self.histapp.title("History")
        self.histapp.geometry(f"{sw}x{sh}+{x}+{y}")

        # constants
        width = 900
        height = 600
        pdown = 0.07
        data_screenshot = []
        label = customtkinter.CTkLabel(self, text="History")
        onmodify = tkinter.StringVar()
        tb_search = customtkinter.CTkEntry(self.histapp, textvariable=onmodify)
        tb_search.place(relx=0.06, rely=0.0305, relheight=0.03, relwidth=0.465)
        global cur_user
        id = dbcalls.get("Account", ["ID"], f"WHERE Name='{cur_user}'")
        sessions = dbcalls.getdistinct("History", ["Session"], f"WHERE AcctID='{id[0][0]}'")
        sessions.insert(0,"All")
        self.optionmenu = customtkinter.CTkOptionMenu(self.histapp, values=sessions, command=lambda a: self.calltree(my_tree, self.currentuser, str(tb_search.get())))#, variable=self.optionmenu_var)
        self.optionmenu.set("All")
        self.optionmenu.place(relx=0.55, rely=0.0295)
        #ch1 = customtkinter.CTkCheckBox(self.histapp, text='ID', variable=var1, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
        #ch2 = customtkinter.CTkCheckBox(self.histapp, text='Name', variable=var2, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
        #ch3 = customtkinter.CTkCheckBox(self.histapp, text='Gender', variable=var3, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
        #ch4 = customtkinter.CTkCheckBox(self.histapp, text='Year', variable=var4, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
        #ch5 = customtkinter.CTkCheckBox(self.histapp, text='Course', variable=var5, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
        # building tree view
        tree_frame = customtkinter.CTkFrame(self.histapp)
        tree_frame.place(relx=0.01, rely=0.025+pdown, relheight=0.7, relwidth=0.98)
        tree_scroll = customtkinter.CTkScrollbar(tree_frame)
        tree_scroll.pack(side="right", fill = "y")
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        
        my_tree['columns'] = ("Acct ID", "Session", "Time", "Status", "Student ID")
        # #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
        my_tree.column("#0", width=0, stretch=False)
        my_tree.column("Acct ID", anchor=tkinter.CENTER, width=40)
        my_tree.column("Session", anchor=tkinter.W, width=160)
        my_tree.column("Time", anchor=tkinter.CENTER, width=70)
        my_tree.column("Status", anchor=tkinter.CENTER, width=70)
        my_tree.column("Student ID", anchor=tkinter.CENTER, width=70)

        my_tree.heading("#0", text="#", anchor=tkinter.W)
        my_tree.heading("Acct ID",text="Account ID", anchor=tkinter.CENTER)
        my_tree.heading("Session", text="Session", anchor=tkinter.W)
        my_tree.heading("Time", text="Time", anchor=tkinter.CENTER)
        my_tree.heading("Status", text="Status", anchor=tkinter.CENTER)
        my_tree.heading("Student ID", text="Student ID", anchor=tkinter.CENTER)
        my_tree.pack(fill="both", expand=True)
        tree_scroll.configure(command=my_tree.yview)
        filters=[]
        dbcalls.filltree(my_tree, self.currentuser,self.optionmenu.get(), "")
        onmodify.trace("w", lambda name, index, mode: dbcalls.filltree(my_tree, self.currentuser, self.optionmenu.get(), str(tb_search.get())))
        self.histapp.protocol("WM_DELETE_WINDOW", lambda: self.closehist())

    def closehist(self):
        self.histapp.destroy()
        serapp.iconify()
        serapp.deiconify()

    def serverthread(self):
        global th
        self.hostSocket = socket(AF_INET, SOCK_STREAM)
        self.hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        hostIp = "0.0.0.0"
        ip = socket1.gethostbyname(socket1.gethostname())
        print(ip)
        gethostname = ""
        portNumber = 5050
        #portnumber = int(os.getenv("PL_CREDENTIAL_SERVER_PORT", "55955"))
        self.hostSocket.bind((hostIp, portNumber))
        self.hostSocket.listen()
        print ("Waiting for connection...")
        th = threading.current_thread()
        while getattr(th, "do_run", True):
            print("hello")
            clientSocket, clientAddress = self.hostSocket.accept()
            print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
             # Receive data from the client
            data = clientSocket.recv(1024).decode()
            #print(data,"here")
            if data == "DiscoverServer":
                # Broadcast response to client
                clientSocket.send(ip.encode())
                clientSocket.close()
            elif(customtkinter.CTkToplevel.winfo_exists(serapp)==1):
                fullmsg = data[HEADERSIZE:]
                if fullmsg[0]=="0":
                    gethostname=fullmsg[1:]
                clients.add(clientSocket)
                newframe = ClientPC(self.scrollable, gethostname)
                thread = Thread(target=clientThread, args=(clientSocket, clientAddress, newframe), daemon = True)
                thread.start()
        
        #it doesnt reach here
        self.hostSocket.close()
        print("socket down exit loop")

def clientThread(clientSocket, clientAddress, clientframe):
    newmsg = True
    fullmsg = ""
    complete = False
    while True:
        try:
            message = clientSocket.recv(1024)
            if message:
                if newmsg:
                    fullmsg = ""
                    msglen = int(message[:HEADERSIZE])
                    newmsg = False
                    complete = False
                
                fullmsg += message.decode("utf-8")

                if len(fullmsg)-HEADERSIZE == msglen:
                    complete = True
                    fullmsg = fullmsg[HEADERSIZE:]
                    newmsg=True
                    print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ fullmsg)

                if complete:
                    #print(fullmsg, "complete")
                    if (fullmsg[0]=="0"):
                        clientframe.change_name(fullmsg[1:])
                    if (fullmsg[0]=="1"):
                        if fullmsg[1:]=="Not Drowsy":
                            clientframe.normal()
                        elif fullmsg[1:]=="no_face":
                            clientframe.no_face()
                        elif fullmsg[1:]=="Drowsy":
                            clientframe.drowsy()
                    for client in clients:
                        if client is not clientSocket:
                            client.send(pack((clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ fullmsg)).encode("utf-8"))
        except:
            print("abrupt disconnect")
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break
        if not message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break

    clientframe.forget()
    clientSocket.close()

def pack(message):
    message = f'{len(message):<{HEADERSIZE}}' + message
    return message

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

def clientsrefresh(clients):
    pass

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

import time

class ClientPC(customtkinter.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        # Initialize
        # self.frame.grid_propagate(False)
        self.configure(width=300)
        self.label = customtkinter.CTkLabel(
            self, text=f"PC ID: {name}", text_color="white"
        )
        self.label1 = customtkinter.CTkLabel(
            self, text=f"Status: Not Drowsy", text_color="white"
        )

        self.button = customtkinter.CTkButton(
            self, text="Student", command=print("s")
        )
        #self.button1 = customtkinter.CTkButton(self, text="See History", command=print("s"))

        # Grid Placement
        self.pack(pady=10)
        self.img = ImageTk.PhotoImage(Image.open("./images/pc_green.png"))
        self.canvas = tkinter.Canvas(self, width=self.img.width(), height=self.img.height())
        self.canvas.grid(row=0, column=0,padx=5,pady=5)
        self.canvas.create_image(5, 5, image=self.img, anchor="nw")
        self.label.grid(row=0, column=1, columnspan = 2, padx=20, pady=5, sticky="ew")
        self.label1.grid(row=0, column=3, padx=20, pady=5, sticky="ew")
        #button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        #self.button1.grid(row=0, column=4, padx=20, pady=10, sticky="ew")
        #grid_columnconfigure((0, 3), weight=1)
        self.name = name
        self.status = ""
        self.normal()
        self.notification = Notify()
        self.notification.title = "Status Detection"
        self.notification.message = ""
        #self.notification.send()
        
        

    def forget(self):
        self.label.destroy()
        self.label1.destroy()
        self.button.destroy()
        self.destroy()
        print("frame removed")
    
    def change_name(self,name):
        self.label.configure(text=f"PC ID: {name}")
        self.name = name
        print(self.name,name)
        #self.normal()
    
    def normal(self):
        if self.status!="normal":
            dbrequest(self.name,time.time()*1000,"normal")
        self.img.paste(Image.open("./images/pc_green.png"))
        self.configure(border_color="green", border_width=1)
        self.label1.configure(text=f"Status: Not Drowsy")

    def no_face(self):
        if self.status!="no_face":
            dbrequest(self.name,time.time()*1000,"no_face")
            self.notification.message = f"No face detected for {frame_reset_threshold/30} seconds"
            self.notification.send()
        self.img.paste(Image.open("./images/pc_red.png"))
        self.configure(border_color="yellow", border_width=1)
        self.label1.configure(text=f"Status: No Face   ")
    
    def drowsy(self):
        if self.status!="drowsy":
            dbrequest(self.name,time.time()*1000,"drowsy")
            self.notification.message = f"Are you alright? The model thinks your drowsy"
            self.notification.send()
        self.img.paste(Image.open("./images/pc_red.png"))
        self.configure(border_color="red", border_width=1)
        self.label1.configure(text=f"Status: Drowsy    ")

def dbrequest(name,time,status):
    global cur_user, cur_session, globalqueryqueue
    conn = sqlite3.connect("db.db")
    try:
        id = conn.execute("SELECT ID FROM Account WHERE Name='{}'".format(cur_user)).fetchall()
    except Exception as e:
        print("on db request", e)
    #print("SELECT ID FROM Account WHERE Name='{}'".format(cur_user))
    #print(id,"dbpush")
    conn.close()
    query = f"INSERT INTO History (AcctID, Session, Time, Status, StudentID) VALUES ('{id[0][0]}','{cur_session}','{time}','{status}','{name}')"
    globalqueryqueue.append(query)

def commitquery_queue():
    global globalqueryqueue
    db=sqlite3.connect('db.db')
    if len(globalqueryqueue)!=0:
        while len(globalqueryqueue)>0:
            query = globalqueryqueue.pop()
            try:
                db.execute(query)
            except Exception as e:
                print(e, "error on: ", query)
        try:
            db.commit()
            print("committ success")
        except:
            print(e, "error on commit")
    else:
        print("empty queue")
    db.close()

def runsql_forinterval(serapp):
    global stuapp, global_stop
    if not global_stop:
        commitquery_queue()
        serapp.after(120000, lambda: runsql_forinterval(serapp))

if __name__ == "__main__":
    global app
    app = App()
    app.mainloop()
