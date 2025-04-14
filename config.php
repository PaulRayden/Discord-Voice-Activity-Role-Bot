<?php
    // --- Configuración de la Aplicación de Discord ---
    $clientId = 'TU_CLIENT_ID_DE_DISCORD'; // Reemplaza con el Client ID de tu aplicación de Discord
    $clientSecret = 'TU_CLIENT_SECRET_DE_DISCORD'; // Reemplaza con el Client Secret de tu aplicación de Discord
    $redirectUri = 'URL_DE_RETORNO_DE_TU_WEB/callback.php'; // Reemplaza con la URL de retorno de tu web
    $tokenUrl = 'https://discord.com/api/oauth2/token';
    $userUrl = 'https://discord.com/api/users/@me';
    $scopes = 'identify'; // Permisos solicitados

    // --- Configuración del Administrador ---
    $adminUserId = 'TU_ID_DE_USUARIO_ADMINISTRADOR'; // Reemplaza con el ID del usuario administrador

    // --- Rutas de Archivos ---
    $logFilePath = 'discord_bot.log'; // Ruta al archivo de log del bot

    // --- Configuración del Servidor para Comandos del Bot (Ejemplo básico e inseguro) ---
    $botControlUrl = 'http://localhost:8000/'; // URL base para enviar comandos al bot (ejemplo)
?>
