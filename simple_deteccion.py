import RPi.GPIO as GPIO
import pigpio
import time

# GPIO
sensor_pin = 17

# Instanciamos los objetos
pi = pigpio.pi()

pi.set_mode(sensor_pin, pigpio.INPUT)
pi.set_pull_up_down(sensor_pin, pigpio.PUD_UP)

while True:
	print(pi.read(sensor_pin))
	time.sleep(1)
