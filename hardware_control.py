#saca fotos 640×480 con una exposición de 10ms
import pigpio
from picamera2 import Picamera2

# Utils
servo_derecha = 1050 #derecha
servo_izquierda = 2000 #izquierda
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
     
class HardwareControl():
    def __init__(self) -> None:
        self.pi = pigpio.pi()
        # Damos la funcionalidad adecuada a los GPIOs
        self.pi.set_mode(servo_pin, pigpio.OUTPUT)
        self.pi.set_mode(motor_pin, pigpio.OUTPUT)
        self.pi.set_mode(led_pin, pigpio.OUTPUT)
        self.pi.set_mode(sensor_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(sensor_pin, pigpio.PUD_UP)

        self.pi.set_PWM_frequency( servo_pin, servo_freq )
        self.pi.set_PWM_frequency( motor_pin, servo_freq )
        self.pi.set_PWM_frequency( led_pin, led_freq )

        self.picam2 = Picamera2()
        self.picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
        self.picam2.start()

    def spin_wheel(self):
        self.pi.set_servo_pulsewidth(motor_pin, motor_girando)

    def stop_wheel(self):
        self.pi.set_servo_pulsewidth(motor_pin, motor_frenado)

    def servo_write(self, angle):
        self.pi.set_servo_pulsewidth(servo_pin, angle)

    def take_picture(self) -> None:
        self.picam2.capture_file("/var/www/html/img.jpg")
    
    def set_led_intensity(self, dc) -> None:
        self.pi.set_PWM_dutycycle(led_pin,  dc)

    def get_fototransistor_read(self) -> bool:
        return self.pi.read(sensor_pin)


