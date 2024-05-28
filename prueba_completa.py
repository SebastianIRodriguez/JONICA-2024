#saca fotos 640×480 con una exposición de 10ms

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.start()
picam2.capture_file("test1.jpg")
picam2.capture_file("test2.jpg")
picam2.capture_file("test3.jpg")
