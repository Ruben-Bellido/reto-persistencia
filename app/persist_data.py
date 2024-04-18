from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Definir parámetros de la conexión a base de datos
url = "http://localhost:8086"
token = "3z8VGBowMDvIJ6A_q0AlS8x6IPodIYppdp78SLchb-sk3L3eZfWD1pTZ9rsGjY66-p3wnphgdeoszMtKT0E7VQ=="
org = "iot"

# Crear la conexión a la base de datos
client = InfluxDBClient(url=url, token=token, org=org)

# Crear el objeto para escribir en la base de datos
write_api = client.write_api(write_options=SYNCHRONOUS)

query_api = client.query_api()

def persist_data(bucket, measure):
    # Recorrer el contenido de la medida enviada
    for key, val in measure.items():
        # Crear un punto para cada fila
        if key == 'point':
            p = Point(val)
        # Añadir el origen de la medida como tag
        elif key == 'source':
            p.tag(key, val)
        # Fijar clave temporal
        elif key == 'datetime':
            p.time(val, WritePrecision.NS)
        # Añadir campo con su respectiva medida
        else:
            p.field(key, val)
    # Escribir punto en base de datos
    write_api.write(bucket=bucket, org=org, record=p)

    # Recuperar última medición
    query = f"""from(bucket: "{bucket}")
    |> range(start: -1s)
    |> filter(fn: (r) => r._measurement == "wind_turbine")
    |> filter(fn: (r) => r["source"] == "{measure['source']}")
    |> yield(name: "last")"""
    tables = query_api.query(query, org="iot")

    # Contar los valores registrados en la última medición
    count = 0
    for table in tables:
        count += len(table.records)
    return count
    