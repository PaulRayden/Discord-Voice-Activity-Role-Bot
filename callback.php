<?php
    session_start();
    require_once 'config.php';

    if (isset($_GET['code'])) {
        $code = $_GET['code'];

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
        curl_close($ch);

        $tokenData = json_decode($response, true);

        if (isset($tokenData['access_token'])) {
            $accessToken = $tokenData['access_token'];

            // Obtener la información del usuario de Discord
            $ch = curl_init($userUrl);
            curl_setopt($ch, CURLOPT_HTTPHEADER, ['Authorization: Bearer ' . $accessToken]);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response = curl_exec($ch);
            curl_close($ch);

            $userData = json_decode($response, true);

            if (isset($userData['id']) && $userData['id'] == $adminUserId) {
                // El usuario es el administrador, guardar información en la sesión e ir al panel
                $_SESSION['admin_logged_in'] = true;                
                header('Location: php/panel/panel.php');
                die();
            } else {
                // El usuario no es el administrador, mostrar mensaje de error
                echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">No tienes permiso para acceder a este panel.</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
            }
        } else {
            // Error al obtener el token de acceso
            echo '<div class="container mt-5"><div class="alert alert-danger" role="alert">Error al iniciar sesión con Discord.</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
        }
    } else {
        // No se recibió el código de autorización
        echo '<div class="container mt-5"><div class="alert alert-warning" role="alert">Se produjo un error durante la autenticación.</div><p><a href="../index.php">Volver a la página de inicio</a></p></div>';
    }
?>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
