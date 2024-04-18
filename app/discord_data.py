from datetime import datetime, timezone
import logging
import discord
from discord.ext import commands
from persist_data import persist_data


# Establecer logger
logger = logging.getLogger('discord.client')

# Establecer bucket en el cual almacenar los datos
bucket = 'wind_farm'

# Declarar bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento del bot una vez esté listo
@bot.event
async def on_ready():
    logger.info(f'{bot.user} bot logged in')

# Evento del bot al recibir un mensaje
@bot.event
async def on_message(message):
    # Ignora los mensajes del propio bot
    if message.author == bot.user:
        return

    # Comando de ayuda
    if message.content.startswith('!help'):
        # Respuesta
        await message.channel.send(f'Este es el bot {bot.user}, el funcionamiento es el siguiente:\n'+
                                   'Has de introducir los siguientes datos para persistirlos en InfluxDB:\n'+
                                   '1 - LV ActivePower (kW)\n'+
                                   '2 - Wind Speed (m/s)\n'+
                                   '3 - Theoretical_Power_Curve (KWh)\n'+
                                   '4 - Wind Direction (°)\n'+
                                   'El formato para enviar los datos ha de ser el siguiente: !measure 1,2,3,4\n'+
                                   'Advertencia: Las medidas han de estar en formato entero o coma flotante.')
    # Comando de envío de medida
    elif message.content.startswith('!measure '):
        msg = message.content.lstrip('!measure ')
        try:
            # Estructurar mensaje y parsear medidas
            measures = [float(m.strip()) for m in msg.split(',')]
            # Si la longitud no es la deseada se provoca una excepción
            if len(measures) != 4:
                raise Exception()
            # Estructurar información recibida
            measure = {
                'point': 'wind_turbine',
                'LV ActivePower (kW)': measures[0],
                'Wind Speed (m/s)': measures[1],
                'Theoretical_Power_Curve (KWh)': measures[2],
                'Wind Direction (°)': measures[3],
                'source': 'discord',
                'datetime': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            # Registrar medida en base de datos y verificar
            if (persist_data(bucket, measure) == 4):
                logger.info('Medida registrada correctamente')
                # Respuesta
                await message.channel.send('La siguiente medida se ha registrado correctamente:\n'+
                                        f'LV ActivePower (kW): {measures[0]}\n'+
                                        f'Wind Speed (m/s): {measures[1]}\n'+
                                        f'Theoretical_Power_Curve (KWh): {measures[2]}\n'+
                                        f'Wind Direction (°): {measures[3]}')
            else:
                logger.warning('La medida no se ha registrado correctamente')
                # Respuesta
                await message.channel.send('La medida no se ha registrado correctamente')
        except Exception:
            # Respuesta
            await message.channel.send('Revisa el formato de la medida: !measure 1,2,3,4\n'+
                                       'Advertencia: Las medidas han de estar en formato entero o coma flotante.')
    # Mensaje predeterminado
    else:
        # Respuesta
        await message.channel.send('Introduce !help para obtener ayuda acerca del funcionamiento de este bot.')

# Ejecutar bot
bot.run('MTIyODM0NDEyMDUyNzgxODc5Mw.Gj27Tm.7A9QnXQ-0gw-QTEIO_2e4skdXOGjeepfBMu2DM')
