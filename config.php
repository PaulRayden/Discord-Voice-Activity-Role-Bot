<?php
    // --- Configuración de la Aplicación de Discord ---
    $clientId = 'TU_CLIENT_ID_DE_DISCORD';
    $clientSecret = 'TU_CLIENT_SECRET_DE_DISCORD';
    $redirectUri = 'URL_DE_RETORNO_DE_TU_WEB/callback.php';
    $tokenUrl = 'https://discord.com/api/oauth2/token';
    $userUrl = 'https://discord.com/api/users/@me';
    $scopes = 'identify';

    // --- Configuración del Administrador ---
    $adminUserId = 'TU_ID_DE_USUARIO_ADMINISTRADOR';

    // --- Rutas de Archivos ---
    $logFilePath = '../discord/logs/discord_bot.log'; // Ruta al archivo de log del bot

    // --- Configuración de la Base de Datos ---
    $dbType = 'sqlite';
    $mysqlHost = 'localhost';
    $mysqlUser = 'tu_usuario_mysql';
    $mysqlPassword = 'tu_contraseña_mysql';
    $mysqlDatabase = 'tu_base_de_datos_mysql';

    // --- Configuración del Servidor para Comandos del Bot ---
    $botControlUrl = 'http://localhost:8000/';
?>
