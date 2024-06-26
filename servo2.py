import RPi.GPIO as GPIO
import pigpio
import time

servo = 25

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
# La excursión va de 500 para 0 grados a 2500 para 180
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

print( "0 deg" )
pwm.set_servo_pulsewidth( servo, 1200 ) ;
time.sleep( 3 )

print( "90 deg" )
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 3 )

print( "180 deg" )
pwm.set_servo_pulsewidth( servo, 1800 ) ;
time.sleep( 3 )

# turning off servo
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )
