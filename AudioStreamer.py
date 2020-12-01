import socket
import threading

import pyaudio as pyaudio

from EasySocket import EasySocketClient, EasySocketServer

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


class AudioStreamerRecorder(threading.Thread):
    def socket_data_received(self, data):
        True

    def socket_closed(self, easy_socket):
        True

    def __init__(self, ip, port):
        self.connect = True

        threading.Thread.__init__(self)
        self.audio = pyaudio.PyAudio()

        self.easy_socket = EasySocketClient(None, self.socket_data_received, self.socket_closed)
        self.easy_socket.create_socket(ip, port)



    def run(self):
        stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while True:
            in_data = stream.read(CHUNK)
            try:
                self.easy_socket.send_to_server(in_data)
            except ConnectionResetError:
                self.audio.close(stream)
                self.connect = False
                break

    def connected(self):
        return self.connect


class AudioStreamerListener:

    def audio_received(self, data):
        self.stream.write(data)

    def __init__(self, ip, port):
        # Audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
        self.client_socket = EasySocketClient(None, self.audio_received)
        self.client_socket.create_socket(ip, port)
        self.client_socket.start()

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class AudioStreamerServer:


    # forward data to client
    def socket_data_audio_received(self, socket, address, data):
        self.audio_server_from_listener.send_to_all(data)

    def socket_data_listener_received(self, socket, address, data):
        True

    def __init__(self, ip, port_recorder, port_listener):
        self.audio_server_from_recorder = EasySocketServer(ip, port_recorder, self.socket_data_audio_received)
        self.audio_server_from_listener = EasySocketServer(ip, port_listener, self.socket_data_listener_received)
        self.audio_server_from_listener.start()
        self.audio_server_from_recorder.start()

