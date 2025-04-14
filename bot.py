# Importamos las librerías necesarias de discord.py
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import sqlite3

# --- CONFIGURACIÓN DEL BOT ---
# Token de tu bot de Discord (reemplaza con el tuyo)
TOKEN = 'TU_TOKEN_AQUI'
# ID del servidor de Discord donde quieres que funcione el bot
GUILD_ID = TU_ID_DE_SERVIDOR
# ID del rol de MIEMBRO ACTIVO
ACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_ACTIVO
# ID del rol de MIEMBRO INACTIVO
INACTIVE_MEMBER_ROLE_ID = TU_ID_DE_ROL_INACTIVO
# Nombre del canal de voz que el bot debe monitorear (opcional, si quieres un canal específico)
VOICE_CHANNEL_NAME_TO_MONITOR = None  # Si es None, se considerarán todos los canales de voz

# Nombre del archivo de la base de datos SQLite
DATABASE_FILE = 'voice_activity.db'

# Definimos los intents (intenciones) que nuestro bot necesitará
# Necesitamos intents para miembros y presencia para rastrear el estado de voz
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# Creamos una instancia del bot con un prefijo para los comandos (aunque no usaremos comandos aquí)
bot = commands.Bot(command_prefix='!', intents=intents)

# --- FUNCIONES DE LA BASE DE DATOS ---

def crear_tabla():
    """Crea la tabla para almacenar la actividad de voz si no existe."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voice_activity (
            user_id INTEGER PRIMARY KEY,
            last_connection_24h TEXT,
            last_connection_7d TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_conexion(user_id, timestamp, period):
    """Registra una conexión de voz para un usuario."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT last_connection_{period} FROM voice_activity WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    if result:
        connections = result[0] if result[0] else ""
        connections += timestamp.isoformat() + ","
        cursor.execute(f'''
            UPDATE voice_activity SET last_connection_{period} = ? WHERE user_id = ?
        ''', (connections, user_id))
    else:
        cursor.execute('''
            INSERT INTO voice_activity (user_id, last_connection_24h, last_connection_7d)
            VALUES (?, ?, ?)
        ''', (user_id, timestamp.isoformat() if period == '24h' else None, timestamp.isoformat() if period == '7d' else None))
        if period == '24h' and period != '7d':
            cursor.execute('''
                UPDATE voice_activity SET last_connection_7d = ? WHERE user_id = ?
            ''', (timestamp.isoformat(), user_id))
        elif period == '7d' and period != '24h':
            cursor.execute('''
                UPDATE voice_activity SET last_connection_24h = ? WHERE user_id = ?
            ''', (timestamp.isoformat(), user_id))
        elif period == '24h' and period == '7d': # Esto nunca debería pasar en la lógica actual
            pass
    conn.commit()
    conn.close()

def obtener_conexiones(user_id, period):
    """Obtiene las conexiones de voz de un usuario dentro de un período."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT last_connection_{period} FROM voice_activity WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
        return [datetime.datetime.fromisoformat(dt) for dt in result[0].strip(',').split(',')]
    return []

# --- EVENTOS DEL BOT ---

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y listo."""
    print(f'Bot conectado como {bot.user.name} ({bot.user.id})')
    crear_tabla()
    # Iniciamos la tarea de verificación de actividad al iniciar el bot
    check_activity.start()

@bot.event
async def on_voice_state_update(member, before, after):
    """Se ejecuta cuando un miembro cambia su estado de voz (se une, se va, se silencia, etc.)."""
    now = datetime.datetime.utcnow()

    # Si el miembro se conecta a un canal de voz
    if before.channel is None and after.channel is not None:
        # Si estamos monitoreando un canal específico y no es ese canal, ignoramos
        if VOICE_CHANNEL_NAME_TO_MONITOR is not None and after.channel.name != VOICE_CHANNEL_NAME_TO_MONITOR:
            return

        # Registramos la hora de conexión
        registrar_conexion(member.id, now, '24h')
        registrar_conexion(member.id, now, '7d')

    # Si el miembro se desconecta de un canal de voz
    elif before.channel is not None and after.channel is None:
        # No necesitamos hacer nada especial al desconectarse para el conteo de tiempo
        pass

# --- TAREAS PROGRAMADAS ---

@tasks.loop(seconds=60)  # Verificamos la actividad cada 60 segundos (1 minuto)
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
        if member.bot:  # Ignoramos a otros bots
            continue

        # --- Cálculo del tiempo de conexión en las últimas 24 horas ---
        connections_24h = obtener_conexiones(member.id, '24h')
        twenty_four_hours_ago = now - datetime.timedelta(hours=24)
        recent_connections_24h = [dt for dt in connections_24h if dt > twenty_four_hours_ago]
        connected_time_24h_minutes = len(recent_connections_24h)

        # Asignar o remover rol de MIEMBRO ACTIVO
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

        # --- Cálculo del tiempo de conexión en los últimos 7 días ---
        connections_7d = obtener_conexiones(member.id, '7d')
        seven_days_ago = now - datetime.timedelta(days=7)
        recent_connections_7d = [dt for dt in connections_7d if dt > seven_days_ago]
        connected_time_7d_minutes = len(recent_connections_7d)

        # Asignar o remover rol de MIEMBRO INACTIVO
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
            # Si no estuvo activo en 7 días y tiene el rol activo, también removerlo
            try:
                await member.remove_roles(active_role, reason="No ha estado activo en los últimos 7 días.")
                print(f"Removido rol '{active_role.name}' de {member.name} (inactivo 7 días).")
            except discord.Forbidden:
                print(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

# Iniciamos el bot con nuestro token
bot.run(TOKEN)
