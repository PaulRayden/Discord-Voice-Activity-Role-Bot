<?php
    require_once 'config.php';

    // Construir la URL de autorización de Discord
    $authorizeUrl = 'https://discord.com/oauth2/authorize';
    $authorizeUrl .= '?client_id=' . urlencode($clientId);
    $authorizeUrl .= '&redirect_uri=' . urlencode($redirectUri);
    $authorizeUrl .= '&response_type=code';
    $authorizeUrl .= '&scope=' . urlencode($scopes);

    // Redirigir al usuario a la página de autorización de Discord
    header('Location: ' . $authorizeUrl);
    die();
?>
