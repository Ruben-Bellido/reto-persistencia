from datetime import datetime, timezone
import logging
import csv
import time
from persist_data import persist_data

# Establecer logger
logging.basicConfig(format='%(asctime)s %(levelname)s   %(name)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('csv.client')

# Establecer bucket en el cual almacenar los datos
bucket = 'wind_farm'

# Abrir el archivo CSV
with open('./reto-persistencia/app/T1.csv', 'r') as file:
    reader = csv.DictReader(file)
    # Recorrer el CSV e insertar los datos en la base de datos
    for row in reader:
        # Inicializar medida
        measure = {}
        # Añadir información de la medida al diccionario utilizando los nombres de las columnas del CSV
        measure['point'] = 'wind_turbine'
        for column in row:
            if 'Date/Time' not in column:
                measure[column] = float(row[column])
        measure['source'] = 'csv'
        measure['datetime'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Registrar medida en base de datos y verificar
        if (persist_data(bucket, measure) == 4):
            logger.info('Medida registrada correctamente')
        else:
            logger.warning('La medida no se ha registrado correctamente')
        
        # Esperar 1 segundo antes de insertar la siguiente línea
        time.sleep(1)
