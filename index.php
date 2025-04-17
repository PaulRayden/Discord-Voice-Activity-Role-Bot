<?php
session_start();

// Verificar si se rechazaron los términos
if (isset($_GET['rejected']) && $_GET['rejected'] == 1) {
    $error_message = "Para continuar, debes aceptar los términos y condiciones y la licencia.";
}

if (file_exists('config.php')) {
    header('Location: install/index.php');
    exit;
} else {
    header('Location: install/terms.php'); // Redirigir a la página de términos
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <?php include 'theme/header.php'; ?>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <?php if (isset($error_message)): ?>
                    <div class="alert alert-danger" role="alert"><?php echo $error_message; ?></div>
                <?php endif; ?>
                <div class="card">
                    <div class="card-header">
                        Iniciar Sesión con Discord
                    </div>
                    <div class="card-body">
                        <p>Para acceder al panel de control del bot, por favor inicia sesión con tu cuenta de Discord.</p>
                        <a href="php/auth/login.php" class="btn btn-primary btn-block">Iniciar Sesión con Discord</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php include 'theme/footer.php'; ?>    
</body>
</html>
