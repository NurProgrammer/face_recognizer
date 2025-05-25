from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
#from PIL import ImageTk, Image
from gender_prediction import emotion,ageAndgender

# Modern color scheme
COLORS = {
    'primary': '#8E44AD',      # Purple
    'secondary': '#FFC300',    # Yellow
    'accent': '#2C3E50',       # Dark Blue/Black
    'text': '#ECF0F1',         # Light Gray (for text on dark backgrounds)
    'bg': '#1A1A1A',          # Dark Background
    'white': '#FFFFFF',        # White
    'dark_purple': '#6C3483',  # Darker Purple for hover
    'dark_yellow': '#F39C12',  # Darker Yellow for hover
    'light_bg': '#2D2D2D',     # Lighter background for contrast
    'black': '#000000'         # Black for button text
}

# Custom styles
BUTTON_STYLE = {
    'borderwidth': 0,
    'padx': 20,
    'pady': 10,
    'border': 0
}

names = set()

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold")
        self.header_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.button_font = tkfont.Font(family='Helvetica', size=12)
        
        self.title("Face Recognition System")
        self.resizable(False, False)
        self.geometry("800x600")
        self.configure(bg=COLORS['bg'])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        
        container = tk.Frame(self, bg=COLORS['bg'])
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg=COLORS['bg'])
        
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLORS['bg'])
        
        # Create main container with padding
        main_container = tk.Frame(self, bg=COLORS['bg'], padx=40, pady=40)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = tk.Label(main_container, 
                        text="Face Recognition System",
                        font=controller.title_font,
                        fg=COLORS['text'],
                        bg=COLORS['bg'])
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="ew")
        
        # Image
        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(main_container, image=render, bg=COLORS['bg'])
        img.image = render
        img.grid(row=1, column=1, rowspan=3, padx=(40, 0), sticky="nsew")
        
        # Buttons Container
        button_container = tk.Frame(main_container, bg=COLORS['bg'])
        button_container.grid(row=1, column=0, sticky="nsew")
        
        # Buttons with new color scheme
        button1 = tk.Button(button_container,
                          text="Sign Up",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['secondary'],
                          activebackground=COLORS['dark_yellow'],
                          activeforeground=COLORS['black'],
                          command=lambda: controller.show_frame("PageOne"),
                          **BUTTON_STYLE)
        
        button2 = tk.Button(button_container,
                          text="Check User",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['primary'],
                          activebackground=COLORS['dark_purple'],
                          activeforeground=COLORS['black'],
                          command=lambda: controller.show_frame("PageTwo"),
                          **BUTTON_STYLE)
        
        button3 = tk.Button(button_container,
                          text="Quit",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['accent'],
                          activebackground=COLORS['light_bg'],
                          activeforeground=COLORS['black'],
                          command=lambda: self.on_closing(),
                          **BUTTON_STYLE)
        
        # Button Layout with new styling
        button1.grid(row=0, pady=10, sticky="ew")
        button2.grid(row=1, pady=10, sticky="ew")
        button3.grid(row=2, pady=10, sticky="ew")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLORS['bg'])
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'], padx=40, pady=40)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = tk.Label(main_container,
                        text="Register New User",
                        font=controller.header_font,
                        fg=COLORS['text'],
                        bg=COLORS['bg'])
        title.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Name Entry
        name_label = tk.Label(main_container,
                            text="Enter your name",
                            font=('Helvetica', 12),
                            fg=COLORS['text'],
                            bg=COLORS['bg'])
        name_label.grid(row=1, column=0, padx=5, pady=10)
        
        self.user_name = tk.Entry(main_container,
                                font=('Helvetica', 12),
                                bg=COLORS['light_bg'],
                                fg=COLORS['text'],
                                insertbackground=COLORS['text'],  # Cursor color
                                relief="flat",
                                highlightthickness=1,
                                highlightbackground=COLORS['primary'])
        self.user_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        button_container = tk.Frame(main_container, bg=COLORS['bg'])
        button_container.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.buttoncanc = tk.Button(button_container,
                                  text="Cancel",
                                  font=controller.button_font,
                                  fg=COLORS['black'],
                                  bg=COLORS['accent'],
                                  activebackground=COLORS['light_bg'],
                                  activeforeground=COLORS['black'],
                                  command=lambda: controller.show_frame("StartPage"),
                                  **BUTTON_STYLE)
        
        self.buttonext = tk.Button(button_container,
                                 text="Next",
                                 font=controller.button_font,
                                 fg=COLORS['black'],
                                 bg=COLORS['secondary'],
                                 activebackground=COLORS['dark_yellow'],
                                 activeforeground=COLORS['black'],
                                 command=self.start_training,
                                 **BUTTON_STYLE)
        
        self.buttonclear = tk.Button(button_container,
                                   text="Clear",
                                   font=controller.button_font,
                                   fg=COLORS['black'],
                                   bg=COLORS['primary'],
                                   activebackground=COLORS['dark_purple'],
                                   activeforeground=COLORS['black'],
                                   command=self.clear,
                                   **BUTTON_STYLE)
        
        self.buttoncanc.grid(row=0, column=0, padx=10)
        self.buttonext.grid(row=0, column=1, padx=10)
        self.buttonclear.grid(row=0, column=2, padx=10)

    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLORS['bg'])
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'], padx=40, pady=40)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = tk.Label(main_container,
                        text="User Authentication",
                        font=controller.header_font,
                        fg=COLORS['text'],
                        bg=COLORS['bg'])
        title.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Username Entry
        name_label = tk.Label(main_container,
                            text="Enter your username",
                            font=('Helvetica', 12),
                            fg=COLORS['text'],
                            bg=COLORS['bg'])
        name_label.grid(row=1, column=0, padx=5, pady=10)
        
        self.user_name = tk.Entry(main_container,
                                font=('Helvetica', 12),
                                bg=COLORS['light_bg'],
                                fg=COLORS['text'],
                                insertbackground=COLORS['text'],
                                relief="flat",
                                highlightthickness=1,
                                highlightbackground=COLORS['primary'])
        self.user_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Dropdown menu
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(main_container, self.menuvar, *names)
        self.dropdown.config(bg=COLORS['light_bg'],
                           fg=COLORS['text'],
                           font=('Helvetica', 12),
                           relief="flat",
                           highlightthickness=1,
                           activebackground=COLORS['primary'],
                           activeforeground=COLORS['text'])
        self.dropdown["menu"].config(bg=COLORS['light_bg'],
                                   fg=COLORS['text'],
                                   font=('Helvetica', 12))
        
        # Buttons
        button_container = tk.Frame(main_container, bg=COLORS['bg'])
        button_container.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.buttoncanc = tk.Button(button_container,
                                  text="Cancel",
                                  font=controller.button_font,
                                  fg=COLORS['black'],
                                  bg=COLORS['accent'],
                                  activebackground=COLORS['light_bg'],
                                  activeforeground=COLORS['black'],
                                  command=lambda: controller.show_frame("StartPage"),
                                  **BUTTON_STYLE)
        
        self.buttonext = tk.Button(button_container,
                                 text="Next",
                                 font=controller.button_font,
                                 fg=COLORS['black'],
                                 bg=COLORS['secondary'],
                                 activebackground=COLORS['dark_yellow'],
                                 activeforeground=COLORS['black'],
                                 command=self.next_foo,
                                 **BUTTON_STYLE)
        
        self.buttonclear = tk.Button(button_container,
                                   text="Clear",
                                   font=controller.button_font,
                                   fg=COLORS['black'],
                                   bg=COLORS['primary'],
                                   activebackground=COLORS['dark_purple'],
                                   activeforeground=COLORS['black'],
                                   command=self.clear,
                                   **BUTTON_STYLE)
        
        self.buttoncanc.grid(row=0, column=0, padx=10)
        self.buttonext.grid(row=0, column=1, padx=10)
        self.buttonclear.grid(row=0, column=2, padx=10)

    def next_foo(self):
        if self.user_name.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.user_name.get()
        self.controller.show_frame("PageFour")  
        
    def clear(self):
        self.user_name.delete(0, 'end')
        
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))
            
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLORS['bg'])
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'], padx=40, pady=40)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = tk.Label(main_container,
                        text="Data Collection",
                        font=controller.header_font,
                        fg=COLORS['text'],
                        bg=COLORS['bg'])
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Status label
        self.numimglabel = tk.Label(main_container,
                                   text="Number of images captured = 0",
                                   font=('Helvetica', 12),
                                   fg=COLORS['text'],
                                   bg=COLORS['bg'])
        self.numimglabel.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Buttons
        button_container = tk.Frame(main_container, bg=COLORS['bg'])
        button_container.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.capturebutton = tk.Button(button_container,
                                     text="Capture Data Set",
                                     font=controller.button_font,
                                     fg=COLORS['black'],
                                     bg=COLORS['secondary'],
                                     activebackground=COLORS['dark_yellow'],
                                     activeforeground=COLORS['black'],
                                     command=self.capimg,
                                     **BUTTON_STYLE)
        
        self.trainbutton = tk.Button(button_container,
                                   text="Train The Model",
                                   font=controller.button_font,
                                   fg=COLORS['black'],
                                   bg=COLORS['primary'],
                                   activebackground=COLORS['dark_purple'],
                                   activeforeground=COLORS['black'],
                                   command=self.trainmodel,
                                   **BUTTON_STYLE)
        
        self.capturebutton.grid(row=0, column=0, padx=10)
        self.trainbutton.grid(row=0, column=1, padx=10)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=COLORS['bg'])
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'], padx=40, pady=40)
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = tk.Label(main_container,
                        text="Face Recognition Features",
                        font=controller.header_font,
                        fg=COLORS['text'],
                        bg=COLORS['bg'])
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Buttons with new color scheme
        button1 = tk.Button(main_container,
                          text="Face Recognition",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['secondary'],
                          activebackground=COLORS['dark_yellow'],
                          activeforeground=COLORS['black'],
                          command=self.openwebcam,
                          **BUTTON_STYLE)
        
        button2 = tk.Button(main_container,
                          text="Emotion Detection",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['primary'],
                          activebackground=COLORS['dark_purple'],
                          activeforeground=COLORS['black'],
                          command=self.emot,
                          **BUTTON_STYLE)
        
        button3 = tk.Button(main_container,
                          text="Gender and Age Prediction",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['primary'],
                          activebackground=COLORS['dark_purple'],
                          activeforeground=COLORS['black'],
                          command=self.gender_age_pred,
                          **BUTTON_STYLE)
        
        button4 = tk.Button(main_container,
                          text="Go to Home Page",
                          font=controller.button_font,
                          fg=COLORS['black'],
                          bg=COLORS['accent'],
                          activebackground=COLORS['light_bg'],
                          activeforeground=COLORS['black'],
                          command=lambda: controller.show_frame("StartPage"),
                          **BUTTON_STYLE)
        
        # Button Layout with equal spacing
        button1.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        button2.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        button3.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        button4.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

    def openwebcam(self):
        main_app(self.controller.active_name)
        
    def gender_age_pred(self):
        ageAndgender()
        
    def emot(self):
        emotion()


app = MainUI()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()

