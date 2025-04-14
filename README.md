# Discord Voice Activity Role Bot

## Descripción

Este es un bot de Discord en Python diseñado para gestionar roles basados en la actividad de los miembros en canales de voz. El bot rastrea el tiempo que los usuarios pasan conectados en los canales de voz durante las últimas 24 horas y los últimos 7 días, asignando automáticamente los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO" según los criterios definidos.

**Nuevas Características:**

* **Soporte para SQLite y MySQL:** Ahora el bot puede utilizar tanto una base de datos SQLite local (por defecto) como un servidor MySQL para la persistencia de datos.
* **Selección de Base de Datos al Inicio:** Al ejecutar el bot, se preguntará al usuario qué tipo de base de datos desea utilizar.

## Cómo Empezar

### Prerrequisitos

* Python 3.6 o superior instalado.
* pip (el gestor de paquetes de Python).
* Una cuenta de Discord y un bot creado en el Portal de Desarrolladores de Discord ([https://discord.com/developers/applications](https://discord.com/developers/applications)).
* Los IDs del servidor de Discord y los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO".
* **Para usar MySQL:** Un servidor MySQL en funcionamiento y las credenciales necesarias. También debes tener instalada la librería `mysql-connector-python` (`pip install mysql-connector-python`).

### Instalación

1.  **Clona este repositorio (opcional):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <nombre_del_repositorio>
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install discord.py mysql-connector-python  # Incluye el conector de MySQL
    ```

### Configuración

1.  **Copia el código de `bot.py`** en un archivo con ese nombre.
2.  **Reemplaza los marcadores de posición** en el archivo `bot.py` con tus valores reales:
    * `'TU_TOKEN_AQUI'`: El token de tu bot de Discord.
    * `TU_ID_DE_SERVIDOR`: El ID de tu servidor de Discord.
    * `TU_ID_DE_ROL_ACTIVO`: El ID del rol de "MIEMBRO ACTIVO".
    * `TU_ID_DE_ROL_INACTIVO`: El ID del rol de "MIEMBRO INACTIVO".
    * `VOICE_CHANNEL_NAME_TO_MONITOR`: Opcionalmente, el nombre del canal de voz a monitorear (dejar en `None` para todos).
3.  **Configura las credenciales de MySQL** en las variables `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, y `MYSQL_DATABASE` dentro del archivo `bot.py` si planeas usar MySQL.

### Ejecución

1.  Abre una terminal o símbolo del sistema.
2.  Navega al directorio donde guardaste `bot.py`.
3.  Ejecuta el bot con:
    ```bash
    python bot.py
    ```
    El bot te preguntará en la consola si deseas usar `sqlite` o `mysql`. Ingresa tu elección.

#### Ejecución en Segundo Plano (Ubuntu con `screen`)

(Esta sección puede permanecer igual, ya que la forma de ejecutar el bot no cambia)

#### Ejecución como Servicio Systemd en Ubuntu

(Esta sección también puede permanecer similar, recordando que el bot preguntará por la base de datos al inicio)

### Configuración de la Base de Datos

Al ejecutar el bot por primera vez, se te pedirá que elijas entre `sqlite` y `mysql`.

* **SQLite:** Si eliges `sqlite`, se creará un archivo de base de datos local llamado `voice_activity.db` en el mismo directorio del bot. No requiere configuración adicional más allá de la elección.
* **MySQL:** Si eliges `mysql`, el bot intentará conectarse al servidor MySQL utilizando las credenciales que configuraste en las variables `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, y `MYSQL_DATABASE` dentro del archivo `bot.py`. Asegúrate de que el servidor esté en funcionamiento y de que la base de datos exista con los permisos correctos para el usuario configurado.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request.

## Créditos

Desarrollado por Paul Rayden para PREL - Agency.
