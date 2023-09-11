import random
from datetime import datetime, timedelta

def generar_horas(horarios_probabilidades, num_transacciones):
    horas_generadas = []
    
    for _ in range(num_transacciones):
        r = random.uniform(0, 1)
        acumulado = 0
        for horario, probabilidad in horarios_probabilidades:
            acumulado += probabilidad
            if r <= acumulado:
                hora_inicio, hora_fin = map(int, horario.split('-'))
                hora_random = random.randint(hora_inicio, hora_fin-1)
                minutos_random = random.randint(0, 59)
                segundos_random = random.randint(0, 59) # Generando segundos aleatoriamente
                horas_generadas.append((hora_random, minutos_random, segundos_random))
                break
                
    return sorted(horas_generadas)

horarios_probabilidades = [
    #... (tu lista de horarios y probabilidades)
    ("0-1", 0.01),
    ("1-2", 0.01),
    ("2-3", 0.01),
    ("3-4", 0.01),
    ("4-5", 0.01),
    ("5-6", 0.02),
    ("6-7", 0.02),
    ("7-8", 0.10),
    ("8-9", 0.10),
    ("9-10", 0.06),
    ("10-11", 0.02),
    ("11-12", 0.02),
    ("12-13", 0.02),
    ("13-14", 0.10),
    ("14-15", 0.09),
    ("15-16", 0.07),
    ("16-17", 0.02),
    ("17-18", 0.02),
    ("18-19", 0.10),
    ("19-20", 0.09),
    ("20-21", 0.06),
    ("21-22", 0.02),
    ("22-23", 0.01),
    ("23-24", 0.01)
]


def call_generar_horas(data, fecha_inicio_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
    num_transacciones = len(data)
    horas_generadas = generar_horas(horarios_probabilidades, num_transacciones)
    transacciones_con_fecha = []

    for idx, (hora, minuto, segundo) in enumerate(horas_generadas):
        fecha_transaccion = fecha_inicio + timedelta(hours=hora, minutes=minuto, seconds=segundo)
        transaccion_actual = data[idx]  
        transaccion_actual['fechaYHoraTransaccionVenta'] = fecha_transaccion.strftime('%Y-%m-%dT%H:%M:%S')
        transacciones_con_fecha.append(transaccion_actual)

    i = 0
    while i < len(transacciones_con_fecha) - 1:
        trans1 = transacciones_con_fecha[i]
        trans2 = transacciones_con_fecha[i+1]
        fecha1 = datetime.strptime(trans1['fechaYHoraTransaccionVenta'], '%Y-%m-%dT%H:%M:%S')
        fecha2 = datetime.strptime(trans2['fechaYHoraTransaccionVenta'], '%Y-%m-%dT%H:%M:%S')
        diff = fecha2 - fecha1

        if diff.seconds < 120 and trans1['numeroDispensario'] == trans2['numeroDispensario'] and trans1['identificadorManguera'] == trans2['identificadorManguera']:
            if i + 2 < len(transacciones_con_fecha):  # Si existe una tercera transacción
                trans3 = transacciones_con_fecha[i+2]

                # Intercambiar el número de transacción de trans2 y trans3
                num_trans2 = trans2['numeroUnicoTransaccionVenta']
                num_trans3 = trans3['numeroUnicoTransaccionVenta']
                trans2['numeroUnicoTransaccionVenta'], trans3['numeroUnicoTransaccionVenta'] = num_trans3, num_trans2

                # Intercambio de datos de trans2 y trans3, excepto el número de transacción
                fecha_trans2 = trans2['fechaYHoraTransaccionVenta']
                trans2, trans3 = trans3, trans2

                # Intercambiar fechas de transacción para mantener la lógica
                trans2['fechaYHoraTransaccionVenta'], trans3['fechaYHoraTransaccionVenta'] = fecha_trans2, trans2['fechaYHoraTransaccionVenta']

                transacciones_con_fecha[i+1], transacciones_con_fecha[i+2] = trans2, trans3
            i += 2  # Saltar la siguiente transacción para evitar doble revisión
        else:
            i += 1  # Pasar a la siguiente transacción

    return transacciones_con_fecha



def call_generar_horas_OLD(data, fecha_inicio_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
    num_transacciones = len(data)
    horas_generadas = generar_horas(horarios_probabilidades, num_transacciones)
    transacciones_con_fecha = []
    
    for idx, (hora, minuto, segundo) in enumerate(horas_generadas):
        fecha_transaccion = fecha_inicio + timedelta(hours=hora, minutes=minuto, seconds=segundo)
        transaccion_actual = data[idx]  # Asumimos que data es una lista de diccionarios de transacciones
        transaccion_actual['fechaYHoraTransaccionVenta'] = fecha_transaccion.strftime('%Y-%m-%dT%H:%M:%S')
        transacciones_con_fecha.append(transaccion_actual)
        
    return transacciones_con_fecha

