<?php
    // --- Configuración del Dominio ---
    $baseDomain = ''; // Reemplaza con tu dominio base (ej., 'tu-dominio.com')
                      // Déjalo vacío si quieres que se detecte automáticamente (menos robusto para CLI).

    // --- Configuración de la Aplicación de Discord ---
    $clientId = 'TU_CLIENT_ID_DE_DISCORD';
    $clientSecret = 'TU_CLIENT_SECRET_DE_DISCORD';
    // La redirectUri se construirá dinámicamente en callback.php y login.php
    $tokenUrl = 'https://discord.com/api/oauth2/token';
    $userUrl = 'https://discord.com/api/users/@me';
    $scopes = 'identify';

    // --- Configuración del Administrador ---
    $adminUserId = 'TU_ID_DE_USUARIO_ADMINISTRADOR';

    // --- Rutas de Archivos ---
    $logFilePath = '../discord/logs/discord_bot.log';

    // --- Configuración de la Base de Datos ---
    $dbType = 'sqlite';
    $mysqlHost = 'localhost';
    $mysqlUser = 'tu_usuario_mysql';
    $mysqlPassword = 'tu_contraseña_mysql';
    $mysqlDatabase = 'tu_base_de_datos_mysql';

    // --- Configuración del Servidor para Comandos del Bot ---
    $botControlUrl = 'http://localhost:8000/';

    // --- Función para obtener la URL base dinámicamente ---
    function getBaseURL() {
        global $baseDomain;
        if (!empty($baseDomain)) {
            $protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http';
            return $protocol . '://' . $baseDomain;
        } else {
            $protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http';
            $host = $_SERVER['HTTP_HOST'] ?? '';
            $uri = rtrim(dirname($_SERVER['PHP_SELF']), '/\\');
            return $protocol . '://' . $host . $uri;
        }
    }
?>
