#640x480-SBGGR10_1X10 - Selected unicam format: 640x480-pBAA

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_and_capture_file("test.jpg")

