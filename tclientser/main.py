import customtkinter
import client
import pystray
import PIL.Image

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
        screen_width = int(self.winfo_screenwidth()*0.3)
        screen_height = int(self.winfo_screenheight()*0.2)
        self.eval('tk::PlaceWindow . center')
        self.geometry(f"{screen_width}x{screen_height}")
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
        otherFrame.destroy()
        app.iconify()
        app.deiconify()

    def checkevent(self, event):
        print("iconify")
        startTray(stuapp)


    def clientrun(self, *args):
        global handler, stuapp
        self.withdraw()
        stuapp = StudentApp()
        handler = lambda: self.onCloseOtherFrame(stuapp)
        #Initialize
        frame = customtkinter.CTkFrame(stuapp)

        stuapp.label = customtkinter.CTkLabel(frame, text = "Student Dashboard", text_color="white")

        stuapp.button1 = customtkinter.CTkButton(frame, text = "Reselect Mode", command = handler)
        stuapp.button2 = customtkinter.CTkButton(frame, text = "Minimize to Tray", command = lambda: startTray(stuapp))

        #add camera output, detect and select camera
        #status check
        #detect and connect to client

        #Grid Placement
        frame.pack(pady = 10)
        
        stuapp.label.grid(row=0, column=0, padx=20, pady=5, sticky ="ew")
        stuapp.button1.grid(row=2, column=0, padx=20, pady=10, sticky ="ew")
        stuapp.button2.grid(row=3, column=0, padx=20, pady=10, sticky ="ew")
        stuapp.grid_columnconfigure((0, 3), weight=1)
        center(stuapp)
        stuapp.resizable(False, False)
        stuapp.protocol("WM_DELETE_WINDOW", handler)







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


def Studentrun():
     stuapp = StudentApp()

def startTray(stuapp):
    global icon
    stuapp.withdraw()
    image = PIL.Image.open("drowsiness-detection/tclientser/images/awake-logo.png")
    icon = pystray.Icon("Awake", image, menu=pystray.Menu(
        pystray.MenuItem("Show App", lambda: showstudent_closetray(stuapp), default=True)
    ))
    icon.run()

class StudentApp(customtkinter.CTkToplevel):
    def __init__(self):
        global handler
        super().__init__()

        self.title("Student Client")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        #self.app = customtkinter.CTk()
        screen_width = int(self.winfo_screenwidth()*0.5)
        screen_height = int(self.winfo_screenheight()*0.2)
        x = (self.winfo_screenwidth()/2) - (screen_width/2)
        y = (self.winfo_screenheight()/2) - (screen_height/2)
        self.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        #self.app.grid_columnconfigure(0, weight=1)
        #self.app.grid_rowconfigure(2, weight=1)
        
        


if __name__ == "__main__":
        global app
        app = App()
        app.mainloop()