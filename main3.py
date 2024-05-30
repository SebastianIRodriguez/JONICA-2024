#saca fotos 640×480 con una exposición de 10ms
import time
import fcntl
import os
import sys

import object_identification as NN
from object_identification import NeuralNetwork

import hardware_control as HC
from hardware_control import HardwareControl

# El promedio fue de 1.26 - 1.27 segundos entre cada cubito
nn = NeuralNetwork()
hw = HardwareControl()

hw.set_led_intensity(25)
hw.spin_wheel()

exiting_hole = False
absolute_start = time.time()
primer_med = True

i = 0

seleccion_hoyo = [HC.servo_izquierda, HC.servo_izquierda, HC.servo_izquierda, HC.servo_izquierda]
hole_index = 0

tiempo1 = time.time()
tiempo2 = time.time()

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

desired_object = NN.PELOTA_ROJA

while True:
    hole_detected = not hw.get_fototransistor_read()
    
    try: mensaje = sys.stdin.readline()
    except: continue
    if mensaje:
        mensaje = mensaje.strip()
        if mensaje.lower() == "pr":
            print("Se separaran las pelotitas rojas")
            desired_object = NN.PELOTA_ROJA
        elif mensaje.lower() == "pv":
            print("Se separaran las pelotitas verdes")
            desired_object = NN.PELOTA_VERDE
        elif mensaje.lower() == "cr":
            print("Se separaran los cubos rojos")
            desired_object = NN.CUBO_ROJO
        elif mensaje.lower() == "cv":
            print("Se separaran los cubos verdes")
            desired_object = NN.CUBO_VERDE
        else :
            print(f"Se recibio algo no valido {mensaje.lower()}")
    

    if not exiting_hole and hole_detected :
        #time.sleep(0.245)
        time.sleep(0.020)
        hw.stop_wheel()
    
        if not primer_med:
            #print(f"Tomando foto numero: {i}")
            time.sleep(0.3)
            
            tiempo1 = time.time()
            hw.take_picture()
            #print(f"La foto tardo {time.time() - tiempo1} segundos")
            
            tiempo2 = time.time()
            object_id = nn.process_image()
            #print(f"La red tardo {time.time() - tiempo2} segundos")

            if object_id == desired_object:
                servo_state = HC.servo_derecha
            else:
                servo_state = HC.servo_izquierda

            seleccion_hoyo[hole_index] = servo_state
            i += 1
        else:
            primer_med = False
        
        # Esperamos un cachin para poner más cosas en la tolva
        #time.sleep(1.5)
            
        # Arrancamos el motor
        hw.spin_wheel()
        
        # Acomodamos el estado de los servos
        hole_index += 1
        if hole_index == 4:
            hole_index = 0
            
        hw.servo_write(seleccion_hoyo[hole_index - 2])
        time.sleep(0.1)
        exiting_hole = True
        
    if exiting_hole and not hole_detected :
        exiting_hole = False

print(f"Duracion total del proceso: {(time.time() - absolute_start):.2f}")
hw.stop_wheel()
hw.set_led_intensity(0)
