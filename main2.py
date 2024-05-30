#saca fotos 640×480 con una exposición de 10ms

import asyncio
import time
import object_identification as NN
from object_identification import NeuralNetwork

import hardware_control as HC
from hardware_control import HardwareControl

async def leer_mensajes():
    while True:
        mensaje = input("¿Cómo te llamas? ")
        print(f"Mensaje ingresado: {mensaje}")

        if mensaje.lower() == "suma":
            resultado = 2 + 2
            print(f"Resultado de la suma 2 + 2: {resultado}")

async def hacer_cosas():

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
    while True:
        hole_detected = not hw.get_fototransistor_read()

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

                if object_id == NN.PELOTA_ROJA:
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

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tareas = asyncio.gather(leer_mensajes(), hacer_cosas())
    try:
        loop.run_until_complete(tareas)
    except KeyboardInterrupt:
        import hardware_control as HC
        from hardware_control import HardwareControl
        print("\n[*] Cerrando el programa")
        hw = HardwareControl()
        hw.stop_wheel()
        hw.set_led_intensity(0)
        
