import time
from pylsl import StreamInlet, resolve_stream
import numpy as np
import requests

api_key = 'ei_4d4c0c4aaab112133466a751d62eac320a6e11f98b2fdb56ca3f8bd98371b2e4'
project_id = "360326" 

url = 'https://ingestion.edgeimpulse.com/api/training/data'

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

emptySignature = ''.join(['0'] * 64)

def subir_datos(data, label, sample_num):
    newh = headers.copy()
    newh['x-file-name'] = f'emg{sample_num}_{label}.json'
    newh['x-label'] = label
    data_payload = {
        "protected": {
            "ver": "v1",
            "alg": "HS256",
            "iat": 0  # Timestamp de la creación del dato
        },
        "signature": emptySignature,  # La firma, si es necesaria; de lo contrario, dejar vacío
        "payload": {
            "device_name": "98:D3:71:FD:62:1F",  # Nombre de tu dispositivo
            "device_type": "Bitalino",
            "interval_ms": 1,  # Intervalo entre muestras en milisegundos
            "sensors": [
                { "name": "emg1", "units": "mV" }
            ],
            "values": [
                [value] for value in data  
            ]
        }
    }

    response = requests.post(url, headers=newh, json=data_payload)
    
    if response.status_code == 200:
        print(f'Datos de {label} enviados con éxito.')
    else:
        print(f'Error al enviar datos de {label}: {response.status_code}', response.text)


def iniciar_adquisicion(label, sample_num):
    print(f"Iniciando adquisición para {label}, muestra #{sample_num}...")
    
    # Cuenta regresiva de 3 segundos antes de iniciar la adquisición
    for i in range(3, 0, -1):
        print(f"Comenzando en {i}...")
        time.sleep(1)
    
    os_stream = resolve_stream("name", "OpenSignals")
    print("Adquiriendo datos...")
    inlet = StreamInlet(os_stream[0])

    buffer = []
    ts_buffer = []
    start_time = time.time()
    while (time.time() - start_time) < 5:  # Receive samples for 5 seconds
        samples, timestamps = inlet.pull_chunk()
        if samples:  # Verifica si la lista no está vacía
            samples_array = np.array(samples)  # Convierte samples a un array de NumPy
            last_values = samples_array[:, -1]  # Selecciona solo la última columna (último valor de cada muestra)
            buffer.extend(last_values.tolist())  # Añade los valores al buffer convirtiéndolos de nuevo a lista si es necesario
            ts_buffer.extend(timestamps)
            print(f"Añadido {len(last_values)} muestras al buffer. Total muestras en buffer: {len(buffer)}")

    print(f"Total muestras recibidas en 5 segundos: {len(buffer)}")
    print(len(ts_buffer))
    print("Adquisición completada.")

    # Preguntar al usuario si desea enviar los datos
    enviar = input("¿Desea enviar los datos? (y/n): ")
    if enviar.lower() == 'y':
        subir_datos(buffer, label, sample_num)
    else:
        print("Los datos no se enviarán.")


def menu_principal():
    while True:
        print("\nMenu Principal")
        print("1. Iniciar adquisición de datos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            label = input("Ingrese el label: ")
            sample_num = input("Ingrese el número de muestra: ")
            iniciar_adquisicion(label, sample_num)
        elif opcion == '2':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    menu_principal()