# Discord Voice Activity Role Bot

## Descripción

Este es un bot de Discord en Python diseñado para gestionar roles basados en la actividad de los miembros en canales de voz. El bot rastrea el tiempo que los usuarios pasan conectados en los canales de voz durante las últimas 24 horas y los últimos 7 días, asignando automáticamente los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO" según los criterios definidos. Además, incluye una interfaz web básica para la administración y el monitoreo del bot por parte del administrador del servidor.

**Características:**

* **Rol de Miembro Activo/Inactivo:** Asignación automática de roles basada en la actividad de voz.
* **Persistencia de Datos:** Soporte para SQLite y MySQL para almacenar la actividad de los usuarios.
* **Selección de Base de Datos:** Opción para elegir entre SQLite y MySQL al iniciar el bot.
* **Interfaz Web de Administración:** Panel de control web protegido por inicio de sesión con Discord para el administrador.
    * **Visualización de Logs:** Muestra las últimas líneas del archivo de log del bot.
    * **Monitorización de Recursos:** Información básica sobre el uso de CPU, memoria y subida del servidor.
    * **Control del Bot:** Botones para (intentar) iniciar, reiniciar y apagar el bot.
* **Configuración Centralizada:** La mayoría de la configuración específica de la web se encuentra en el archivo `config.php`.
* **Detección Dinámica de URL:** La URL de retorno para la autenticación de Discord se genera dinámicamente, facilitando la instalación en diferentes dominios y subdirectorios.

## Cómo Empezar

### Prerrequisitos

* Python 3.6 o superior instalado.
* pip (el gestor de paquetes de Python).
* Librerías de Python: `discord.py`, `mysql-connector-python` (si se usa MySQL).
* Una cuenta de Discord y una **aplicación** creada en el Portal de Desarrolladores de Discord ([https://discord.com/developers/applications](https://discord.com/developers/applications)).
* Los IDs del servidor de Discord y los roles de "MIEMBRO ACTIVO" y "MIEMBRO INACTIVO".
* **Para la interfaz web:**
    * Un servidor web (como Apache o Nginx) con PHP habilitado.
    * **Configuración de la Aplicación de Discord en el Portal de Desarrolladores:** Deberás configurar una **URL de retorno (Redirect URI)** para tu aplicación en la sección "OAuth2". Esta URL debe ser la ruta completa a `callback.php` en tu servidor web (ej., `https://tu-dominio.com/callback.php`).

### Instalación

1.  **Clona este repositorio (opcional):**
    ```bash
    git clone https://github.com/PaulRayden/Discord-Voice-Activity-Role-Bot.git
    cd Discord-Voice-Activity-Role-Bot
    ```

2.  **Instala las dependencias de Python:**
    ```bash
    pip install discord.py mysql-connector-python
    ```

### Configuración

1.  **Configura el Bot de Discord (archivo `/discord/bot.py`):**
    * Reemplaza los marcadores de posición de `TOKEN`, `GUILD_ID`, `ACTIVE_MEMBER_ROLE_ID`, `INACTIVE_MEMBER_ROLE_ID` y `ADMIN_USER_ID` con tus valores reales.
    * Si planeas usar MySQL, configura las credenciales en las variables `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE`.
    * El archivo de log se guardará en `/discord/logs/discord_bot.log`.

2.  **Configura la Interfaz Web (archivo `config.php`):**
    * **Crea un archivo llamado `config.php`** en el directorio raíz de tu sitio web.
    * **Obtén el Client ID y el Client Secret de tu aplicación de Discord** desde el Portal de Desarrolladores (sección "OAuth2").
    * **Reemplaza los marcadores de posición** con la información de tu aplicación de Discord y tu servidor web:
        * `$baseDomain`: (Opcional) Define tu dominio base (ej., `tu-dominio.com`). Déjalo vacío para detección automática.
        * `$clientId`: El **Client ID** de tu aplicación de Discord.
        * `$clientSecret`: El **Client Secret** de tu aplicación de Discord. **¡Mantén este secreto seguro!**
        * `$adminUserId`: El ID del usuario administrador del bot (debe coincidir con el configurado en `/discord/bot.py`).
        * `$logFilePath`: La ruta al archivo de log del bot (por defecto: `'../discord/logs/discord_bot.log'`).
        * `$botControlUrl`: (Opcional) La URL base para enviar comandos al bot (si implementas un servidor web separado para esto).

3.  **Configuración Inicial (carpeta `/install/`):**
    * Accede a la carpeta `/install/` a través de tu navegador web (ej., `https://tu-dominio.com/install/`).
    * Completa el formulario con la información requerida. **Asegúrate de que la "Redirect URI" que ingreses aquí coincida exactamente con la que configuraste en el Portal de Desarrolladores de Discord.**
    * Esto creará automáticamente el archivo `config.php` en la raíz de tu sitio web.
    * Si eliges MySQL durante la instalación, intentará crear la tabla `voice_activity` en la base de datos proporcionada.
    * **Importante:** Después de la instalación, **elimina o protege fuertemente la carpeta `/install/`** para evitar que se vuelva a ejecutar la instalación accidentalmente. Puedes hacerlo mediante la configuración de tu servidor web o utilizando un archivo `.htaccess` (como se mencionó anteriormente).

### Ejecución

#### Ejecución del Bot de Discord

1.  Abre una terminal o símbolo del sistema.
2.  Navega al directorio `/discord/` dentro de tu repositorio.
3.  Ejecuta el bot con:
    ```bash
    python bot.py
    ```
    El bot te preguntará en la consola si deseas usar `sqlite` o `mysql`.

#### Acceso a la Interfaz Web

1.  Asegúrate de que todos los archivos PHP y la carpeta `css` estén subidos a la raíz de tu servidor web.
2.  Accede a la página de inicio de sesión (`index.php`) a través de tu navegador web (ej., `https://tu-dominio.com/index.php`).
3.  Sigue el proceso de inicio de sesión con tu cuenta de Discord. Solo el usuario con el ID configurado como administrador podrá acceder al panel de control.

### Notas Importantes sobre la Interfaz Web

* **Seguridad:** La funcionalidad de control del bot (iniciar, reiniciar, apagar) en el panel de control es un ejemplo básico y puede ser insegura en un entorno de producción. Considera implementar mecanismos de seguridad más robustos para controlar el bot desde la web.
* **Protección de Directorios:** Asegúrate de proteger los directorios `/discord/` y `/install/` para evitar accesos no autorizados (se recomienda usar la configuración de tu servidor web o archivos como `.htaccess` para Apache y la configuración equivalente para Nginx).
* **Uso de Recursos:** La información sobre el uso de recursos del servidor es básica y puede variar según el sistema operativo.
* **Servidor Web:** Asegúrate de que tu servidor web esté configurado correctamente para PHP y tenga los módulos necesarios (como `curl` para las peticiones a la API de Discord).

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request.

## Créditos

Desarrollado por Paul Rayden para PREL - Agency.
