from gpiozero import AngularServo
from time import sleep

ServoPIN = 24 
#servo = AngularServo(ServoPIN, min_pulse_width=0.0006, max_pulse_width=0.0023)
servo = AngularServo(ServoPIN, initial_angle=90, min_angle=0, max_angle=180, min_pulse_width=1/1000, max_pulse_width=25/10000)

while (True):
    servo.angle = 10
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = -10
    sleep(2)
