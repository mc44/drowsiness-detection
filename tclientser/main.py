import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Drowsiness App")
        customtkinter.set_default_color_theme("dark-blue")
        #self.app = customtkinter.CTk()
        screen_width = int(self.winfo_screenwidth()*0.6)
        screen_height = int(self.winfo_screenheight()*0.6)
        self.geometry(f"{screen_width}x{screen_height}")
        #self.app.grid_columnconfigure(0, weight=1)
        #self.app.grid_rowconfigure(2, weight=1)
        
        #Initialize
        self.frame = customtkinter.CTkFrame(self, height = screen_height, width = int(screen_width*0.5), bg_color="blue")
        #self.frame.grid_propagate(False)

        self.label = customtkinter.CTkLabel(self.frame, text = "Select mode", text_color="white")

        self.button = customtkinter.CTkButton(self.frame, text = "Student")
        self.button1 = customtkinter.CTkButton(self.frame, text = "Server")

        #Grid Placement
        self.frame.grid()
        
        #self.label.grid(row=0, column=0, padx=20, pady=20 )
        #self.button.grid(row=1, column=0, padx=20, pady=20 )
        #self.button1.grid(row=2, column=0, padx=20, pady=10)

app = App()
app.mainloop()