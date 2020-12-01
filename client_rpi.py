import time

import cv2
import imagezmq
from imutils.video import VideoStream

from AudioStreamer import AudioStreamerRecorder

image_hub = imagezmq.ImageSender("tcp://192.168.1.14:5555")
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
# audio_recorder = AudioStreamerRecorder("127.0.0.1", 5654)
# audio_recorder.start()
while True:
    frame = picam.read()
    image_hub.send_image("ringer", frame)

