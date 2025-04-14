# Importamos las librerías necesarias de discord.py
import discord
from discord.ext import commands, tasks
import datetime
import asyncio

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

# Diccionario para almacenar el tiempo de conexión de cada miembro en los últimos 24 horas
voice_activity_24h = {}
# Diccionario para almacenar el tiempo de conexión de cada miembro en los últimos 7 días
voice_activity_7d = {}

# Definimos los intents (intenciones) que nuestro bot necesitará
# Necesitamos intents para miembros y presencia para rastrear el estado de voz
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# Creamos una instancia del bot con un prefijo para los comandos (aunque no usaremos comandos aquí)
bot = commands.Bot(command_prefix='!', intents=intents)

# --- EVENTOS DEL BOT ---

@bot.event
async def on_ready():
    """Se ejecuta cuando el bot está conectado y listo."""
    print(f'Bot conectado como {bot.user.name} ({bot.user.id})')
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
        voice_activity_24h.setdefault(member.id, []).append(now)
        voice_activity_7d.setdefault(member.id, []).append(now)

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
        if member.id in voice_activity_24h:
            # Filtramos las horas de conexión que están dentro de las últimas 24 horas
            twenty_four_hours_ago = now - datetime.timedelta(hours=24)
            recent_connections_24h = [dt for dt in voice_activity_24h[member.id] if dt > twenty_four_hours_ago]
            # Estimamos el tiempo conectado (esto es una simplificación, no es exacto si se une y se va varias veces)
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
        else:
            # Si no hay actividad reciente en las últimas 24 horas y tiene el rol activo, lo removemos
            if active_role in member.roles:
                try:
                    await member.remove_roles(active_role, reason="No hay actividad reciente en las últimas 24 horas.")
                    print(f"Removido rol '{active_role.name}' de {member.name} (sin actividad reciente).")
                except discord.Forbidden:
                    print(f"No tengo permisos para remover el rol '{active_role.name}' de {member.name}.")
                except discord.HTTPException as e:
                    print(f"Error al remover el rol '{active_role.name}' de {member.name}: {e}")

        # --- Cálculo del tiempo de conexión en los últimos 7 días ---
        if member.id in voice_activity_7d:
            # Filtramos las horas de conexión que están dentro de los últimos 7 días
            seven_days_ago = now - datetime.timedelta(days=7)
            recent_connections_7d = [dt for dt in voice_activity_7d[member.id] if dt > seven_days_ago]
            # Estimamos el tiempo conectado en los últimos 7 días (simplificación)
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
        elif inactive_role not in member.roles:
            # Si no hay registro de actividad en 7 días y no tiene el rol inactivo, se lo asignamos
            try:
                await member.add_roles(inactive_role, reason="Sin registro de actividad en los últimos 7 días.")
                print(f"Asignado rol '{inactive_role.name}' a {member.name} (sin registro de actividad).")
            except discord.Forbidden:
                print(f"No tengo permisos para asignar el rol '{inactive_role.name}' a {member.name}.")
            except discord.HTTPException as e:
                print(f"Error al asignar el rol '{inactive_role.name}' a {member.name}: {e}")

    # --- Limpieza de los diccionarios de actividad (opcional, se mantiene por simplicidad) ---
    # Esto podría volverse grande con el tiempo en servidores muy activos.
    # Podrías implementar una lógica para eliminar entradas antiguas si es necesario.

# Iniciamos el bot con nuestro token
bot.run(TOKEN)
