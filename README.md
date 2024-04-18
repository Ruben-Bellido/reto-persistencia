# reto-persistencia

## Pasos seguidos
- Investigación: Elección de base de datos apropiada
- Ivestigación: Instalación, configuración y uso de InfluxDB
- Desarrollo del script de inserción de datos del CSV a InfluxDB
- Desarrollo de un módulo que inserte puntos a un cubo de InfluxDB
- Configuración de un dashboard con gráficas y agregaciones de los datos recientes
- Investigación: Creación y configuración de un bot de Discord
- Desarrollo del script de configuración de un bot de Discord para hacer inserciones manuales a InfluxDB
- Desarrollo del shell script encargado de instalar las librerías de Python necesarias

## Instrucciones de uso
Todos los comandos se han de ejecutar desde la ruta /app
### Instalación de InfluxDB:
- $ curl -O https://dl.influxdata.com/influxdb/releases/influxdb2_2.7.5-1_amd64.deb
- $ sudo dpkg -i influxdb2_2.7.5-1_amd64.deb
- $ sudo service influxdb start
- Ir a http://localhost:8086, configurar InfluxDB y añadir un bucket de nombre wind_farm
### Instalación del bot de discord:
- Acceder al siguiente enlace: https://discord.com/oauth2/authorize?client_id=1228344120527818793
- Autorizar al bot y añadirlo a un servidor
- Inicializar el bot: $ python3 discord_data.py
### Módulos y componentes nesesarios:
- $ sh requirements.sh
### Ejecucción del programa:
- Introducir registros desde el CSV: $ python3 csv_data.py
- Introducir registros desde discord: Este nos ofrece instrucciones al chatear con él

## Posibles vías de mejora
- Añadir seguridad tanto para hacer inserciones como para recuperar registros de base de datos
- Mejorar la escalabilidad, ya que todos los registros se registran en la misma turbina
- Mejorar la verificación, ya que ocasionalmente se detectan inserciones válidas como fallidas

## Problemas / Retos encontrados
- Instalación de InfluxDB
- Comprensión del funcionamiento de una base de datos temporal frente a una relacional o NoSQL

## Alternativas posibles
- TimescaleDB en lugar de InfluxDB
- Telegram en lugar de Discord
