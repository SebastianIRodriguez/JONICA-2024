#saca fotos 640×480 con una exposición de 10ms
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import pigpio
import time

# Utils
servo_derecha = 1050
servo_izquierda = 2000
servo_estable = 1530
motor_frenado = 1500
motor_girando = 1600

# GPIO
sensor_pin = 17
servo_pin = 23
motor_pin = 24
led_pin = 25

# Frecuencias
led_freq = 1000
servo_freq = 50

# Instanciamos los objetos
pi = pigpio.pi()
picam2 = Picamera2()
picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.start()

# Damos la funcionalidad adecuada a los GPIOs
pi.set_mode(servo_pin, pigpio.OUTPUT)
pi.set_mode(motor_pin, pigpio.OUTPUT)
pi.set_mode(led_pin, pigpio.OUTPUT)
pi.set_mode(sensor_pin, pigpio.INPUT)
pi.set_pull_up_down(sensor_pin, pigpio.PUD_UP)

pi.set_PWM_frequency( servo_pin, servo_freq )
pi.set_PWM_frequency( motor_pin, servo_freq )
pi.set_PWM_frequency( led_pin, led_freq )

# El promedio fue de 1.26 - 1.27 segundos entre cada cubito

esperando = False
pi.set_PWM_dutycycle(led_pin,  25)
pi.set_servo_pulsewidth(motor_pin, motor_girando)
absolute_start = time.time()
start_time = time.time()
primer_med = True

prom = 0.0
cont = 0.0

i = 0
while i < 332:
	
	hole_detected = not pi.read(sensor_pin)

	if not esperando and hole_detected :
		time.sleep(0.245)
		pi.set_servo_pulsewidth(motor_pin, motor_frenado)
		print(f"Freno! - Iteracion {i}")

		if not primer_med:
			rotation_duration = time.time() - start_time
			prom = (prom * cont + rotation_duration) / (cont + 1)
			cont += 1
			print(f"Duracion: {(rotation_duration):.2f}, promedio: {(prom):.2f}")
			time.sleep(0.3)
			picam2.capture_file(f"./images/img{i}.jpg")
			i += 1
		else:
			primer_med = False

		
		time.sleep(1.5)
		start_time = time.time()
		pi.set_servo_pulsewidth(motor_pin, motor_girando)
		time.sleep(0.8)
		esperando = True
		
	if esperando and not hole_detected :
		esperando = False

print(f"Duracion total del proceso: {(time.time() - absolute_start):.2f}")
pi.set_servo_pulsewidth(motor_pin, motor_frenado)
pi.set_PWM_dutycycle(led_pin,  0)
