import customtkinter
import tkinter as tk
import client
import pystray
import PIL.Image
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
from PIL import Image, ImageTk
import cv2
import threading

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
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

#Show main app window
def deicon():
      icon.stop()
      app.iconify()
      app.deiconify()


#MAIN


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Drowsiness App")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        #self.app = customtkinter.CTk()
        self.screen_width = int(self.winfo_screenwidth()*0.3)
        self.screen_height = int(self.winfo_screenheight()*0.2)
        self.eval('tk::PlaceWindow . center')
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        #self.app.grid_columnconfigure(0, weight=1)
        #self.app.grid_rowconfigure(2, weight=1)
        
        #Initialize
        frame = customtkinter.CTkFrame(self)
        #self.frame.grid_propagate(False)

        self.label = customtkinter.CTkLabel(frame, text = "Select mode", text_color="white")

        self.button = customtkinter.CTkButton(frame, text = "Student", command= self.clientrun)
        self.button1 = customtkinter.CTkButton(frame, text = "Server")

        #Grid Placement
        frame.pack(pady = 10)
        
        self.label.grid(row=0, column=0, padx=20, pady=5, sticky ="ew")
        self.button.grid(row=1, column=0, padx=20, pady=10, sticky ="ew")
        self.button1.grid(row=2, column=0, padx=20, pady=10, sticky ="ew")
        self.grid_columnconfigure((0, 3), weight=1)
        center(self)
        self.resizable(False, False)

    def onCloseOtherFrame(self, otherFrame):
        #cap.release()
        otherFrame.destroy()
        app.iconify()
        app.deiconify()

    def checkevent(self, event):
        print("iconify")
        startTray(stuapp)

    def update_gui(self, image):
        photo.paste(image)

    def update_frame(self, face_mesh, cap,k):
        #while cap.isOpened():
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
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
        # Flip the image horizontally for a selfie-view display.
        mesh_image = cv2.flip(image, 1)
        image = Image.fromarray(mesh_image)
        self.update_gui(image)
        print(k)
        k+=1
        stuapp.after(1, lambda: self.update_frame(face_mesh,cap,k))

    def start_frame(self, frame):
        stuapp.button3.configure(state=tk.DISABLED)
        global cap
        cap = cv2.VideoCapture(0)
        ret, imgframe = cap.read()
        imgframe = imgframe[:, :, ::-1]
        image = Image.fromarray(imgframe)
        global photo
        photo = ImageTk.PhotoImage(image)
        canvas = tk.Canvas(frame, width=photo.width(), height=photo.height())
        canvas.grid(row=4, column=0, columnspan=2)
        canvas.create_image((0,0), image=photo, anchor='nw')
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
        sw = int(stuapp.winfo_screenwidth()*0.5)
        sh = int(stuapp.winfo_screenheight()*0.7)
        x = (self.winfo_screenwidth()/2) - (sw/2)
        y = (self.winfo_screenheight()/2) - (sh/2)
        stuapp.geometry(f"{sw}x{sh}+{x}+{y}")
        #Initialize
        frame = customtkinter.CTkFrame(stuapp, width = self.screen_width, height=self.screen_height)

        stuapp.label = customtkinter.CTkLabel(frame, text = "Student Dashboard", text_color="white")
        
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        stuapp.button1 = customtkinter.CTkButton(frame, text = "Reselect Mode", command = handler)
        stuapp.button2 = customtkinter.CTkButton(frame, text = "Minimize to Tray", command = lambda: startTray(stuapp))
        
        #threading.Thread(target=self.update_frame(face_mesh,cap,k)).start()
        stuapp.button3 = customtkinter.CTkButton(frame, text = "Start Detecting", command = lambda: self.start_frame(frame))
        stuapp.button4 = customtkinter.CTkButton(frame, text = "Stop Detecting", command = lambda: self.stop_frame())

        #add camera output, detect and select camera
        #status check
        #detect and connect to client

        #Grid Placement
        frame.pack(pady = 10)
        
        stuapp.label.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky ="ew")
        stuapp.button1.grid(row=2, column=0, padx=20, pady=10, sticky ="ew")
        stuapp.button2.grid(row=2, column=1, padx=20, pady=10, sticky ="ew")
        stuapp.button3.grid(row=3, column=0, padx=20, pady=10, sticky ="ew")
        stuapp.button4.grid(row=3, column=1, padx=20, pady=10, sticky ="ew")
        stuapp.grid_columnconfigure((0, 3), weight=1)
        #stuapp.resizable(False, False)
        #use working_ports
        #available_ports,working_ports,non_working_ports = list_ports()
        self.start_frame(frame)
        # For webcam input:
        #drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        
        
            
                
def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 5: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports






#CLIENT AREA   
def exit_action(icon,stuapp):
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
    icon = pystray.Icon("Awake", image, menu=pystray.Menu(
        pystray.MenuItem("Show App", lambda: showstudent_closetray(stuapp), default=True)
    ))
    icon.run()

        
        


if __name__ == "__main__":
        global app
        app = App()
        app.mainloop()