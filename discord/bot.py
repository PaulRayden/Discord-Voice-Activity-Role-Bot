# Importamos las librerías necesarias
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import sqlite3
import mysql.connector
import logging
import os
import subprocess  # Para ejecutar comandos del sistema

# --- CONFIGURACIÓN DEL BOT ---
TOKEN = 'TU_TOKEN_AQUI'
GUILD_ID = TU_ID_DE_SERVIDOR
ACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_ACTIVO
INACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_INACTIVO
VOICE_CHANNEL_NAME_TO_MONITOR = None

# --- CONFIGURACIÓN DEL ADMINISTRADOR ---
ADMIN_USER_ID = TU_ID_DE_USUARIO_ADMINISTRADOR  # Reemplaza con el ID del dueño del servidor

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DATABASE_TYPE = 'sqlite'
SQLITE_DATABASE_FILE = 'voice_activity.db'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'tu_usuario_mysql'
MYSQL_PASSWORD = 'tu_contraseña_mysql'
MYSQL_DATABASE = 'tu_base_de_datos_mysql'

# --- CONFIGURACIÓN DE LOGGING ---
LOG_DIR = 'logs'  # Nombre de la carpeta de logs dentro de /discord/
LOG_FILE = os.path.join(LOG_DIR, 'discord_bot.log')
os.makedirs(LOG_DIR, exist_ok=True)  # Crear la carpeta de logs si no existe
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- INTENTS DEL BOT ---
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
db_connection = None
db_cursor = None

# --- FUNCIONES DE CONEXIÓN A LA BASE DE DATOS ---
def conectar_sqlite():
    global db_connection, db_cursor
    db_connection = sqlite3.connect(SQLITE_DATABASE_FILE)
    db_cursor = db_connection.cursor()
    logging.info("Conectado a SQLite.")

def conectar_mysql():
    global db_connection, db_cursor
    try:
        db_connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        db_cursor = db_connection.cursor()
        logging.info("Conectado a MySQL.")
    except mysql.connector.Error as err:
        logging.error(f"Error al conectar a MySQL: {err}")
        return False
    return True

def desconectar_db():
    global db_connection, db_cursor
    if db_connection:
        db_connection.close()
        logging.info("Desconectado de la base de datos.")
        db_connection = None
        db_cursor = None

def crear_tabla():
    if DATABASE_TYPE == 'sqlite':
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_activity (
                user_id INTEGER PRIMARY KEY,
                last_connection_24h TEXT,
                last_connection_7d TEXT
            )
        ''')
    elif DATABASE_TYPE == 'mysql':
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_activity (
                user_id BIGINT PRIMARY KEY,
                last_connection_24h TEXT,
                last_connection_7d TEXT
            )
        ''')
    db_connection.commit()

def registrar_conexion(user_id, timestamp, period):
    db_cursor.execute(f'''
        SELECT last_connection_{period} FROM voice_activity WHERE user_id = %s
    ''', (user_id,))
    result = db_cursor.fetchone()
    if result:
        connections = result[0] if result[0] else ""
        connections += timestamp.isoformat() + ","
        db_cursor.execute(f'''
            UPDATE voice_activity SET last_connection_{period} = %s WHERE user_id = %s
        ''', (connections, user_id))
    else:
        db_cursor.execute('''
            INSERT INTO voice_activity (user_id, last_connection_24h, last_connection_7d)
            VALUES (%s, %s, %s)
        ''', (user_id, timestamp.isoformat() if period == '24h' else None, timestamp.isoformat() if period == '7d' else None))
        if period == '24h' and period != '7d':
            db_cursor.execute('''
                UPDATE voice_activity SET last_connection_7d = %s WHERE user_id = %s
            ''', (timestamp.isoformat(), user_id))
        elif period == '7d' and period != '24h':
            db_cursor.execute('''
                UPDATE voice_activity SET last_connection_24h = %s WHERE user_id = %s
            ''', (timestamp.isoformat(), user_id))
    db_connection.commit()

def obtener_conexiones(user_id, period):
    db_cursor.execute(f'''
        SELECT last_connection_{period} FROM voice_activity WHERE user_id = %s
    ''', (user_id,))
    result = db_cursor.fetchone()
    if result and result[0]:
        return [datetime.datetime.fromisoformat(dt) for dt in result[0].strip(',').split(',')]
    return []

# --- EVENTOS DEL BOT ---
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} ({bot.user.id})')
    logging.info(f'Bot conectado como {bot.user.name} ({bot.user.id})')

    global DATABASE_TYPE
    while DATABASE_TYPE.lower() not in ['sqlite', 'mysql']:
        DATABASE_TYPE = input("Elige el tipo de base de datos a usar ('sqlite' o 'mysql'): ").lower()

    if DATABASE_TYPE == 'sqlite':
        conectar_sqlite()
    elif DATABASE_TYPE == 'mysql':
        if not conectar_mysql():
            print("No se pudo conectar a MySQL. Saliendo.")
            logging.error("No se pudo conectar a MySQL. Saliendo.")
            await bot.close()
            return

    crear_tabla()
    check_activity.start()

@bot.event
async def on_voice_state_update(member, before, after):
    now = datetime.datetime.utcnow()

    if before.channel is None and after.channel is not None:
        if VOICE_CHANNEL_NAME_TO_MONITOR is not None and after.channel.name != VOICE_CHANNEL_NAME_TO_MONITOR:
            return
        registrar_conexion(member.id, now, '24h')
        registrar_conexion(member.id, now, '7d')

    elif before.channel is not None and after.channel is None:
        pass

@bot.event
async def on_close():
    desconectar_db()

# --- COMANDOS DE ADMINISTRACIÓN (Solo para el dueño del servidor) ---
@bot.command()
async def shutdown_bot(ctx):
    """Apaga el bot (solo para el administrador)."""
    if ctx.author.id == ADMIN_USER_ID:
        logging.info("Comando de apagado recibido por el administrador.")
        await ctx.send("Apagando el bot...")
        await bot.close()
    else:
        await ctx.send("No tienes permiso para ejecutar este comando.")

@bot.command()
async def restart_bot(ctx):
    """Reinicia el bot (solo para el administrador)."""
    if ctx.author.id == ADMIN_USER_ID:
        logging.info("Comando de reinicio recibido por el administrador.")
        await ctx.send("Reiniciando el bot...")
        # Aquí necesitarías una forma externa de reiniciar el script
        # como un script bash que mate el proceso y lo vuelva a ejecutar.
        # Esto no se puede hacer directamente desde el bot de forma fiable.
        await ctx.send("El reinicio debe ser gestionado externamente.")
    else:
        await ctx.send("No tienes permiso para ejecutar este comando.")

# --- TAREAS PROGRAMADAS ---
@tasks.loop(seconds=60)
async def check_activity():
    now = datetime.datetime.utcnow()
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        logging.error(f"No se encontró el servidor con ID: {GUILD_ID}")
        return

    active_role = guild.get_role(ACTIVE_MEMBER_ROLE_ID)
    inactive_role = guild.get_role(INACTIVE_MEMBER_ROLE_ID)

    if not active_role or not inactive_role:
        logging.error("No se encontraron los roles de MIEMBRO ACTIVO o MIEMBRO INACTIVO.")
        return

    for member in guild.members:
        if member.bot:
            continue

        connections_24h = obtener_conexiones(member.id, '24h')
        twenty_four_hours_ago = now - datetime.timedelta(hours=24)
        recent_connections_24h = [dt for dt in connections_24h if dt > twenty_four_hours_ago]
        connected_time_24h_minutes = len(recent_connections_24h)

        if connected_time_24h_minutes >= 60 and active_role not in member.roles:
            try:
                await member.add_roles(active_role, reason="Cumplió con el tiempo de conexión en las últimas 24 horas.")
                logging.info(f"Asignado rol '{active_role.name}' a {member.name}")
            except discord.Forbidden:
                logging.warning(f"No tengo permisos para asignar el rol '{active_role.name}' a {member.name}.")
            except discord.HTTPException as e:
                logging.error(f"Error al asignar el rol '{active_role.name}' a {member.name}: {e}")
        elif connected_time_24h_minutes < 60 and active_role in member.roles:
            try:
                await member.remove_roles(active_role, reason="No cumplió con el tiempo de conexión en las últimas 24 horas.")
                logging.info(f"Removido rol '{active_role.name}' de {member.name}")
            except discord.Forbidden:
                logging.warning(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                logging.error(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

        connections_7d = obtener_conexiones(member.id, '7d')
        seven_days_ago = now - datetime.timedelta(days=7)
        recent_connections_7d = [dt for dt in connections_7d if dt > seven_days_ago]
        connected_time_7d_minutes = len(recent_connections_7d)

        if connected_time_7d_minutes == 0 and inactive_role not in member.roles:
            try:
                await member.add_roles(inactive_role, reason="No ha estado activo en los últimos 7 días.")
                logging.info(f"Asignado rol '{inactive_role.name}' a {member.name}")
            except discord.Forbidden:
                logging.warning(f"No tengo permisos para asignar el rol '{inactive_role.name}' a {member.name}.")
            except discord.HTTPException as e:
                logging.error(f"Error al asignar el rol '{inactive_role.name}' a {member.name}: {e}")
        elif connected_time_7d_minutes > 0 and inactive_role in member.roles:
            try:
                await member.remove_roles(inactive_role, reason="Ha estado activo en los últimos 7 días.")
                logging.info(f"Removido rol '{inactive_role.name}' de {member.name}")
            except discord.Forbidden:
                logging.warning(f"No tengo permisos para remover el rol '{inactive_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                logging.error(f"Error al remover el rol '{inactive_role.name}' de {member.name}: {e}")
        elif connected_time_7d_minutes == 0 and active_role in member.roles:
            try:
                await member.remove_roles(active_role, reason="No ha estado activo en los últimos 7 días.")
                logging.info(f"Removido rol '{active_role.name}' de {member.name} (inactivo 7 días).")
            except discord.Forbidden:
                logging.warning(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                logging.error(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

# Iniciamos el bot
bot.run(TOKEN)
