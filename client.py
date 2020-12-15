import threading
from tkinter import Tk, Label, Button

import cv2
import imagezmq

from AudioStreamer import AudioStreamerRecorder
from EasySocket import EasySocketClient

serverIp = "127.0.0.1"

image_hub = imagezmq.ImageSender("tcp://" + serverIp + ":5555")
cap = cv2.VideoCapture(0)


class Client(threading.Thread):
    def init_audio(self):
        audio_recorder = AudioStreamerRecorder(serverIp, 5654)
        audio_recorder.start()
        return audio_recorder

    def __init__(self):
        threading.Thread.__init__(self)
        self.audio_recorder = self.init_audio()


    def run(self):
        while True:
            ret, frame = cap.read()
            image_hub.send_image("ringer", frame)

            # if dead, restart
            if not self.audio_recorder.connected():
                self.audio_recorder = self.init_audio()

client = Client()

client.start()


class Ring:
    def __init__(self):
        self.socket_client = EasySocketClient(None, self.on_server_receided, self.on_disconnected)
        self.socket_client.create_socket(serverIp, 5568)
        self.socket_client.start()

    def on_server_receided(self):
        pass

    def on_disconnected(self):
        pass

    def ring(self):
        self.socket_client.send_to_server(True)


ring = Ring()

fenetre = Tk()
champ_label = Label(fenetre, text="Doorbell :)")
champ_label.pack()

bouton_quitter = Button(fenetre, text="Sonner", command=ring.ring)
bouton_quitter.pack()
fenetre.mainloop()

