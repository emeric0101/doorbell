from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import time
import datetime
from pyowm.owm import OWM
from phone import open_video
from Camera_view import camera
import sys

# api_key = ""  # Enter your own API Key
# owm = OWM(api_key)
# mgr = owm.weather_manager()
# observation = mgr.weather_at_place('Paris,FR')
# weather = observation.weather
# print(weather)

try:
    import client
except:
    print("Failed to import client.")


class App(Frame):  # fenêtre principale (ecran accueil)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.label = Label(text='', font=("Helvetica", 60), background="#87CEEB")
        self.label.place(x=210, y=20)
        self.label.pack()
        self.label_date = Label(text='', font=("Helvetica", 25), background="#87CEEB")
        self.label_date.place(x=230, y=100)
        # self.label0 = Label(text="", font=("Helvetica", 20), background="#87CEEB")  # This is the head label
        # self.label1 = Label(text="")
        # self.label2 = Label(text="")
        # self.label3 = Label(text="")
        # self.label4 = Label(text="")
        # self.label0.place(x=260, y=160)
        # self.label1.place(x=260, y=160)
        # self.label2.place(x=260, y=160)
        # self.label3.place(x=260, y=160)
        # self.label4.place(x=260, y=160)
        # self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M")
        date = datetime.datetime.now()
        now_date = (str(date.day) + "/" + str(date.month) + "/" + str(date.year))
        self.label.configure(text=now)
        self.label_date.configure(text=now_date)
        self.after(1000, self.update_clock)


def warn_failed_to_connect():
    messagebox.showerror("Erreur", "Impossible de se connecter au serveur.\nMerci de vérifier qu'il est en marche et "
                                   "ensuite redémarrer l'application et réassayer.")
    if messagebox.askyesno("Redémarrer ?", "Voulez vous quiter le programme"):
        sys.exit()


def warn_missing():
    messagebox.showwarning("Erreur", "Cette action est indisponible")


def camera_launch():
    try:
        camera()
    except ConnectionRefusedError:
        print("Error : connection refused")
        warn_failed_to_connect()


root = Tk()
app = App(root)  # fenêtre principale (ecran accueil)
root.wm_title("Ecran d'accueil")
root.config(bg="#87CEEB")  # arriere plan bleu
root.geometry("640x480")
root.maxsize(640, 480)
root.minsize(640, 480)
root.resizable(0, 0)
root.after(1000, App.update_clock(app))
btn_open_portal = Button(root, text="\n     Ouvrir portail     \n", command=warn_missing)
btn_open_portal.place(x=100, y=360)
btn_open_camera = Button(root, text="\n    Ouvrir caméra    \n", command=camera_launch)
btn_open_camera.place(x=260, y=360)
btn_open_settings = Button(root, text="\n          Options          \n", command=warn_missing)
btn_open_settings.place(x=421, y=360)
root.mainloop()
