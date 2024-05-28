import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QT)

preview_config = picam2.create_preview_configuration({"size": (800,600)})
picam2.configure(preview_config)

picam2.start()

while True:
	1
	
