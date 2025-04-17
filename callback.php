<?php
session_start();
require_once 'config.php';

if (isset($_GET['code']) && isset($_GET['state'])) {
    $code = $_GET['code'];
    $state = $_GET['state'];

    // Verificar el estado para protección CSRF
    if (!isset($_SESSION['auth_state']) || $_SESSION['auth_state'] !== $state) {
        echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">Error: Solicitud no válida. Posible ataque CSRF.</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
        die();
    }

    unset($_SESSION['auth_state']); // Limpiar el estado después de la verificación

    // Construir la URL de retorno dinámicamente (debería ser la misma que en login.php)
    $redirectUri = getBaseURL() . '/callback.php';

    // Intercambiar el código de autorización por un token de acceso
    $params = [
        'client_id' => $clientId,
        'client_secret' => $clientSecret,
        'grant_type' => 'authorization_code',
        'code' => $code,
        'redirect_uri' => $redirectUri,
        'scope' => $scopes
    ];

    $ch = curl_init($tokenUrl);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    $error = curl_error($ch);
    curl_close($ch);

    if ($response === false) {
        echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">Error de cURL al obtener el token: ' . htmlspecialchars($error) . '</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
        die();
    }

    $tokenData = json_decode($response, true);

    if (isset($tokenData['access_token'])) {
        $accessToken = $tokenData['access_token'];

        // Obtener la información del usuario de Discord
        $ch = curl_init($userUrl);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Authorization: Bearer ' . $accessToken]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $error = curl_error($ch);
        curl_close($ch);

        if ($response === false) {
            echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">Error de cURL al obtener la información del usuario: ' . htmlspecialchars($error) . '</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
            die();
        }

        $userData = json_decode($response, true);

        if (isset($userData['id']) && $userData['id'] == $adminUserId) {
            // El usuario es el administrador, guardar información en la sesión e ir al panel
            $_SESSION['admin_logged_in'] = true;
            $_SESSION['admin_id'] = $userData['id'];
            $_SESSION['admin_username'] = $userData['username']; // Guardar nombre de usuario (opcional)
            // Puedes guardar más información del usuario si lo deseas

            header('Location: ../panel/panel.php');
            die();
        } else {
            // El usuario no es el administrador, mostrar mensaje de error
            echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">No tienes permiso para acceder a este panel. ID de Discord: ' . htmlspecialchars($userData['id'] ?? 'No encontrado') . '</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
        }
    } else {
        // Error al obtener el token de acceso
        echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">Error al iniciar sesión con Discord: ' . htmlspecialchars($tokenData['error_description'] ?? 'Error desconocido al obtener el token') . '</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
    }
} else {
    // No se recibieron el código de autorización o el estado
    echo '<div class="container mt-5"><div class="alert alert-warning" role="alert">Se produjo un error durante la autenticación. Faltan parámetros.</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
}
?>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" href="../assets/css/style.css">
