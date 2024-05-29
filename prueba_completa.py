#saca fotos 640×480 con una exposición de 10ms

from picamera2 import Picamera2

picam2 = Picamera2()
picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.start()
#picam2.capture_file("test1.jpg")
#picam2.capture_file("test2.jpg")
#picam2.capture_file("test3.jpg")

import RPi.GPIO as GPIO
import pigpio
import VL53L0X
import time

# Utils
servo_derecha = 1050
servo_izquierda = 2000
servo_estable = 1530
motor_frenado = 1500
motor_girando = 1600

# GPIO
servo_pin = 17
motor_pin = 23
led_pin = 25

# Frecuencias
led_freq = 1000
servo_freq = 50

# Instanciamos los objetos
pi = pigpio.pi()
tof = VL53L0X.VL53L0X()

# Damos la funcionalidad adecuada a los GPIOs
pi.set_mode(servo_pin, pigpio.OUTPUT)
pi.set_mode(motor_pin, pigpio.OUTPUT)
pi.set_mode(led_pin, pigpio.OUTPUT)

pi.set_PWM_frequency( servo_pin, servo_freq )
pi.set_PWM_frequency( motor_pin, servo_freq )
pi.set_PWM_frequency( led_pin, led_freq )
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
#tof.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)
#tof.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
#tof.start_ranging(VL53L0X.VL53L0X_LONG_RANGE_MODE)
#tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
"""
while True:
	pi.set_servo_pulsewidth( servo_pin, servo_derecha) ;
	pi.set_servo_pulsewidth( motor_pin, motor_girando) ;
	pi.set_PWM_dutycycle(led_pin,  0)
	time.sleep( 5 )
	pi.set_servo_pulsewidth( servo_pin, servo_izquierda ) ;
	pi.set_PWM_dutycycle(led_pin,  64)
	time.sleep( 5 )
	pi.set_servo_pulsewidth( servo_pin, servo_derecha) ;
	pi.set_servo_pulsewidth( motor_pin, motor_frenado) ;
	pi.set_PWM_dutycycle(led_pin,  128)
	time.sleep( 5 )
	pi.set_servo_pulsewidth( servo_pin, servo_izquierda ) ;
	pi.set_PWM_dutycycle(led_pin,  255)
	time.sleep( 5 )
"""

# El promedio fue de 1.26 - 1.27 segundos entre cada cubito

esperando = False
pi.set_PWM_dutycycle(led_pin,  32)
pi.set_servo_pulsewidth(motor_pin, motor_girando)
start_time = time.time()
primer_med = True

prom = 0.0
cont = 0.0

i = 0
while i < 200:
	
	distance = tof.get_distance()
	print("Distancia [mm]:" + str(distance))

	if not esperando and distance >= 49 :
		pi.set_servo_pulsewidth(motor_pin, motor_frenado)
		print("Freno! a " + str(distance) + " mm")

		if not primer_med:
			rotation_duration = time.time() - start_time
			prom = (prom * cont + rotation_duration) / (cont + 1)
			cont += 1
			print(f"Duracion: {(rotation_duration):.2f}")
			print(f"Duracion promedio: {(prom):.2f}")
			time.sleep(0.1)
			picam2.capture_file(f"./images/img{i}.jpg")
			i += 1
		else:
			primer_med = False

		
		time.sleep(3)
		start_time = time.time()
		pi.set_servo_pulsewidth(motor_pin, motor_girando)
		time.sleep(0.8)
		esperando = True
		
	if esperando and distance < 40 :
		esperando = False


pi.set_servo_pulsewidth(motor_pin, motor_frenado)
pi.set_PWM_dutycycle(led_pin,  0)