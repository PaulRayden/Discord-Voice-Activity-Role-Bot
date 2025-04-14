## README.md

# Discord Voice Activity Role Bot

## Descripción

Este es un bot de Discord en Python diseñado para gestionar roles basados en la actividad de los miembros en canales de voz. El bot rastrea el tiempo que los usuarios pasan conectados en los canales de voz durante las últimas 24 horas y los últimos 7 días, asignando automáticamente los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO" según los criterios definidos. La información de la actividad se persiste utilizando una base de datos SQLite para que el bot pueda recordar el estado incluso después de reiniciarse.

**Funcionalidades:**

* **Rol de Miembro Activo:** Asigna el rol "MIEMBRO ACTIVO" a los usuarios que han estado conectados en un canal de voz durante al menos 60 minutos en las últimas 24 horas.
* **Rol de Miembro Inactivo:** Asigna el rol "MIEMBRO INACTIVO" a los usuarios que no han estado conectados en ningún canal de voz durante los últimos 7 días.
* **Persistencia de Datos:** Utiliza una base de datos SQLite (`voice_activity.db`) para almacenar la información de la actividad de los usuarios, lo que permite que el bot recuerde el estado incluso después de reiniciarse.
* **Configuración Sencilla:** Requiere la configuración de los IDs del token del bot, el ID del servidor y los IDs de los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO". Opcionalmente, se puede especificar un canal de voz específico para monitorear.
* **Funcionamiento en Segundo Plano:** Ideal para ejecutarse en un servidor Ubuntu utilizando `screen` o como un servicio systemd para un funcionamiento continuo.

## Cómo Empezar

### Prerrequisitos

* Python 3.6 o superior instalado.
* pip (el gestor de paquetes de Python).
* Una cuenta de Discord y un bot creado en el Portal de Desarrolladores de Discord ([https://discord.com/developers/applications](https://discord.com/developers/applications)).
* Los IDs del servidor de Discord y los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO".

### Instalación

1.  **Clona este repositorio (opcional si solo copias el código):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <nombre_del_repositorio>
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install discord.py
    ```

### Configuración

1.  **Copia el código de `bot.py`** en un archivo con ese nombre.
2.  **Reemplaza los marcadores de posición** en el archivo `bot.py` con tus valores reales:
    * `'TU_TOKEN_AQUI'`: El token de tu bot de Discord.
    * `TU_ID_DE_SERVIDOR`: El ID de tu servidor de Discord.
    * `TU_ID_DE_ROL_ACTIVO`: El ID del rol de "MIEMBRO ACTIVO".
    * `TU_ID_DE_ROL_INACTIVO`: El ID del rol de "MIEMBRO INACTIVO".
    * `VOICE_CHANNEL_NAME_TO_MONITOR`: Opcionalmente, el nombre del canal de voz a monitorear (dejar en `None` para todos).

### Ejecución

#### Ejecución Simple (para pruebas):

1.  Abre una terminal o símbolo del sistema.
2.  Navega al directorio donde guardaste `bot.py`.
3.  Ejecuta el bot con:
    ```bash
    python bot.py
    ```

#### Ejecución en Ubuntu con `screen` (para mantenerlo corriendo en segundo plano):

1.  Instala `screen` si no lo tienes:
    ```bash
    sudo apt update
    sudo apt install screen
    ```
2.  Ejecuta el bot en una sesión de `screen`:
    ```bash
    screen -S discord_bot
    python bot.py
    ```
3.  Desconéctate de la sesión (`Ctrl + a` luego `d`). El bot seguirá corriendo.
4.  Para volver a ver la sesión: `screen -r discord_bot`.

#### Ejecución como Servicio Systemd en Ubuntu (para inicio automático):

1.  Crea un archivo de servicio:
    ```bash
    sudo nano /etc/systemd/system/discord_bot.service
    ```
2.  Pega la siguiente configuración (ajusta las rutas y el usuario):
    ```ini
    [Unit]
    Description=Servicio del bot de Discord
    After=network.target

    [Service]
    User=$(whoami)
    WorkingDirectory=/ruta/donde/guardaste/bot.py
    ExecStart=/usr/bin/python3 bot.py
    Restart=on-failure
    StandardOutput=journal
    StandardError=journal

    [Install]
    WantedBy=multi-user.target
    ```
3.  Habilita e inicia el servicio:
    ```bash
    sudo systemctl enable discord_bot.service
    sudo systemctl start discord_bot.service
    ```
4.  Verifica el estado y los logs:
    ```bash
    sudo systemctl status discord_bot.service
    sudo journalctl -u discord_bot.service -f
    ```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request.

## Créditos

Desarrollado por Paul Rayden.
