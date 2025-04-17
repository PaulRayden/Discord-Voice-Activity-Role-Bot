<?php
session_start();
require_once '../../config.php';

$state = bin2hex(random_bytes(16));
$_SESSION['auth_state'] = $state;

// Construir la URL de retorno dinámicamente
$redirectUri = getBaseURL() . '/callback.php';

// Construir la URL de autorización de Discord
$params = [
    'client_id' => $clientId,
    'redirect_uri' => $redirectUri,
    'response_type' => 'code',
    'scope' => $scopes,
    'state' => $state
];

$authUrl = 'https://discord.com/oauth2/authorize?' . http_build_query($params);

// Redirigir al usuario a la página de autorización de Discord
header('Location: ' . $authUrl);
die();
?>
