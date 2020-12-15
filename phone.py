import wave
from time import sleep
import PIL.Image     # run pip install Pillow
import PIL.ImageTk
import cv2
import pyaudio

from playsound import playsound

from AudioStreamer import AudioStreamerListener
from EasySocket import EasySocketClient

ip_client = "127.0.0.1"
chunk = 1024

win_name = "DOORBELL"

video_frame = None


def on_video_received(data):
    global video_frame
    video_frame = data


def play_wave(filename):
    playsound(filename)


def open_video():
    socket_client = EasySocketClient(None, on_video_received, lambda x: True)
    socket_client.create_socket(ip_client, 5567)
    socket_client.start()
    # audio_client = AudioStreamerListener("127.0.0.1", 5655)
    # audio_client
    sleep(5)
    cv2.destroyWindow(win_name)
    print("Ring :)")
    socket_client.close()


def on_ring_received(data):
    play_wave('ring.wav')
    open_video()


def start_loop():
    while True:
        ring_client = EasySocketClient(None, on_ring_received, lambda x: True)
        ring_client.create_socket(ip_client, 5569)
        ring_client.start()

        while ring_client.is_alive():
            pass
