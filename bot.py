# Importamos las librerías necesarias
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import sqlite3
import mysql.connector

# --- CONFIGURACIÓN DEL BOT ---
# Token de tu bot de Discord (reemplaza con el tuyo)
TOKEN = 'TU_TOKEN_AQUI'
# ID del servidor de Discord donde quieres que funcione el bot
GUILD_ID = TU_ID_DE_SERVIDOR
# ID del rol de MIEMBRO ACTIVO
ACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_ACTIVO
# ID del rol de MIEMBRO INACTIVO
INACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_INACTIVO
# Nombre del canal de voz que el bot debe monitorear (opcional)
VOICE_CHANNEL_NAME_TO_MONITOR = None

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DATABASE_TYPE = 'sqlite'  # Por defecto usar SQLite. Cambiar a 'mysql' para usar MySQL

# Configuración para SQLite
SQLITE_DATABASE_FILE = 'voice_activity.db'

# Configuración para MySQL (reemplaza con tus credenciales)
MYSQL_HOST = 'localhost'
MYSQL_USER = 'tu_usuario_mysql'
MYSQL_PASSWORD = 'tu_contraseña_mysql'
MYSQL_DATABASE = 'tu_base_de_datos_mysql'

# --- INTENTS DEL BOT ---
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
db_connection = None
db_cursor = None

# --- FUNCIONES DE CONEXIÓN A LA BASE DE DATOS ---

def conectar_sqlite():
    """Conecta a la base de datos SQLite."""
    global db_connection, db_cursor
    db_connection = sqlite3.connect(SQLITE_DATABASE_FILE)
    db_cursor = db_connection.cursor()
    print("Conectado a SQLite.")

def conectar_mysql():
    """Conecta a la base de datos MySQL."""
    global db_connection, db_cursor
    try:
        db_connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        db_cursor = db_connection.cursor()
        print("Conectado a MySQL.")
    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        return False
    return True

def desconectar_db():
    """Desconecta de la base de datos."""
    global db_connection, db_cursor
    if db_connection:
        db_connection.close()
        print("Desconectado de la base de datos.")
        db_connection = None
        db_cursor = None

def crear_tabla():
    """Crea la tabla para almacenar la actividad de voz si no existe."""
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
    """Registra una conexión de voz para un usuario."""
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
    """Obtiene las conexiones de voz de un usuario dentro de un período."""
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
    """Se ejecuta cuando el bot está conectado y listo."""
    print(f'Bot conectado como {bot.user.name} ({bot.user.id})')

    global DATABASE_TYPE
    while DATABASE_TYPE.lower() not in ['sqlite', 'mysql']:
        DATABASE_TYPE = input("Elige el tipo de base de datos a usar ('sqlite' o 'mysql'): ").lower()

    if DATABASE_TYPE == 'sqlite':
        conectar_sqlite()
    elif DATABASE_TYPE == 'mysql':
        if not conectar_mysql():
            print("No se pudo conectar a MySQL. Saliendo.")
            await bot.close()
            return

    crear_tabla()
    check_activity.start()

@bot.event
async def on_voice_state_update(member, before, after):
    """Se ejecuta cuando un miembro cambia su estado de voz."""
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
    """Se ejecuta cuando el bot se va a cerrar."""
    desconectar_db()

# --- TAREAS PROGRAMADAS ---

@tasks.loop(seconds=60)
async def check_activity():
    """Verifica la actividad de voz de los miembros y asigna/remueve roles."""
    now = datetime.datetime.utcnow()
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"No se encontró el servidor con ID: {GUILD_ID}")
        return

    active_role = guild.get_role(ACTIVE_MEMBER_ROLE_ID)
    inactive_role = guild.get_role(INACTIVE_MEMBER_ROLE_ID)

    if not active_role or not inactive_role:
        print("No se encontraron los roles de MIEMBRO ACTIVO o MIEMBRO INACTIVO.")
        return

    for member in guild.members:
        if member.bot:
            continue

        # --- Cálculo de actividad en 24 horas ---
        connections_24h = obtener_conexiones(member.id, '24h')
        twenty_four_hours_ago = now - datetime.timedelta(hours=24)
        recent_connections_24h = [dt for dt in connections_24h if dt > twenty_four_hours_ago]
        connected_time_24h_minutes = len(recent_connections_24h)

        if connected_time_24h_minutes >= 60 and active_role not in member.roles:
            try:
                await member.add_roles(active_role, reason="Cumplió con el tiempo de conexión en las últimas 24 horas.")
                print(f"Asignado rol '{active_role.name}' a {member.name}")
            except discord.Forbidden:
                print(f"No tengo permisos para asignar el rol '{active_role.name}' a {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al asignar el rol '{active_role.name}' a {member.name}: {e}")
        elif connected_time_24h_minutes < 60 and active_role in member.roles:
            try:
                await member.remove_roles(active_role, reason="No cumplió con el tiempo de conexión en las últimas 24 horas.")
                print(f"Removido rol '{active_role.name}' de {member.name}")
            except discord.Forbidden:
                print(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

        # --- Cálculo de actividad en 7 días ---
        connections_7d = obtener_conexiones(member.id, '7d')
        seven_days_ago = now - datetime.timedelta(days=7)
        recent_connections_7d = [dt for dt in connections_7d if dt > seven_days_ago]
        connected_time_7d_minutes = len(recent_connections_7d)

        if connected_time_7d_minutes == 0 and inactive_role not in member.roles:
            try:
                await member.add_roles(inactive_role, reason="No ha estado activo en los últimos 7 días.")
                print(f"Asignado rol '{inactive_role.name}' a {member.name}")
            except discord.Forbidden:
                print(f"No tengo permisos para asignar el rol '{inactive_role.name}' a {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al asignar el rol '{inactive_role.name}' a {member.name}: {e}")
        elif connected_time_7d_minutes > 0 and inactive_role in member.roles:
            try:
                await member.remove_roles(inactive_role, reason="Ha estado activo en los últimos 7 días.")
                print(f"Removido rol '{inactive_role.name}' de {member.name}")
            except discord.Forbidden:
                print(f"No tengo permisos para remover el rol '{inactive_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al remover el rol '{inactive_role.name}' de {member.name}: {e}")
        elif connected_time_7d_minutes == 0 and active_role in member.roles:
            try:
                await member.remove_roles(active_role, reason="No ha estado activo en los últimos 7 días.")
                print(f"Removido rol '{active_role.name}' de {member.name} (inactivo 7 días).")
            except discord.Forbidden:
                print(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

# Iniciamos el bot
bot.run(TOKEN)
