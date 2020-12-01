import socket
import threading

hostname = socket.gethostname()

local_ip = "127.0.0.1"  # socket.gethostbyname(hostname)

from imagezmq import imagezmq

from AudioStreamer import AudioStreamerServer
from EasySocket import EasySocketServer


print("Starting video server")
video_server = EasySocketServer(local_ip, 5567, lambda x: True)
video_server.start()

print("Starting sound server")
audio_server = AudioStreamerServer(local_ip, 5654, 5655)


class Video_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.image_hub = imagezmq.ImageHub()

    def run(self):
        while True:
            # read the frame from the camera and send it to the server
            belling, image = self.image_hub.recv_image()
            self.image_hub.send_reply(b'OK')

            try:
                video_server.send_to_all(image)
            except ConnectionResetError:
                pass


class Ring_server:
    def __init__(self):

        self.ring_server = EasySocketServer(local_ip, 5568, self.on_ring)
        self.client_server = EasySocketServer(local_ip, 5569, self.on_phone_received)
        self.ring_server.start()
        self.client_server.start()

    def on_ring(self, socket, adress, payload):
        self.client_server.send_to_all(True)
        print("Ring")

    def on_phone_received(self, socket, address, payload):

        print("Open video")




ring = Ring_server()
vt = Video_thread()
vt.start()


