from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import time
import datetime
from pyowm.owm import OWM
from phone import open_video
from App2 import camera

# api_key = ""  # Enter your own API Key
# owm = OWM(api_key)
# mgr = owm.weather_manager()
# observation = mgr.weather_at_place('Paris,FR')
# weather = observation.weather
# print(weather)

try:
    import client
except:
    print("Failed to connect to the server.")


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.label = Label(text='', font=("Helvetica", 60), background="#87CEEB")
        self.label.place(x=210, y=20)
        self.label_date = Label(text='', font=("Helvetica", 25), background="#87CEEB")
        self.label_date.place(x=230, y=100)
        self.label0 = Label(text="Météo :", font=("Helvetica", 20), background="#87CEEB")  # This is the head label
        self.label1 = Label(text="Enter the City :")
        self.label2 = Label(text="Temperature :")
        self.label3 = Label(text="Humidity :")
        self.label4 = Label(text="Description  :")
        self.label0.place(x=260, y=160)
        self.label1.place()
        self.label2.place()
        self.label3.place()
        self.label4.place()
        self.update_clock()

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


def camera_launch():
    camera()
    print("oui")


fenetre = Tk()
app = App(fenetre)
fenetre.title("Ecran d'accueil")
fenetre.config(bg="#87CEEB")  # arriere plan bleu
fenetre.geometry("640x480")
fenetre.maxsize(640, 480)
fenetre.minsize(640, 480)
fenetre.after(1000, App.update_clock(app))
btn_open_portal = Button(fenetre, text="\n     Ouvrir portail     \n")
btn_open_portal.place(x=100, y=360)
btn_open_camera = Button(fenetre, text="\n    Ouvrir caméra    \n", command=camera_launch)
btn_open_camera.place(x=260, y=360)
btn_open_settings = Button(fenetre, text="\n          Options          \n")
btn_open_settings.place(x=421, y=360)
fenetre.mainloop()
