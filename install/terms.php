<?php
session_start();

if (isset($_POST['accept_terms'])) {
    $_SESSION['terms_accepted'] = true;
    header('Location: install/index.php');
    exit;
}

if (isset($_POST['reject_terms'])) {
    $error_message = "Para continuar con la instalación, debes aceptar los términos y condiciones y la licencia.";
}

if (isset($_SESSION['terms_accepted']) && $_SESSION['terms_accepted'] === true) {
    header('Location: install/index.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones / Licencia</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <?php include 'theme/header.php'; ?>
    <div class="container mt-5">
        <h2>Términos y Condiciones</h2>
        <p>Aquí irán los términos y condiciones...</p>

        <h2>Licencia</h2>
        <p>Aquí irá la información de la licencia...</p>

        <?php if (isset($error_message)): ?>
            <div class="alert alert-danger"><?php echo $error_message; ?></div>
        <?php endif; ?>

        <form method="post" class="mt-3">
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="accept_terms" name="accept_terms" required>
                <label class="form-check-label" for="accept_terms">Acepto los términos y condiciones y la licencia.</label>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Aceptar y Continuar con la Instalación</button>
            <button type="submit" class="btn btn-danger mt-3" name="reject_terms">Rechazar y Salir</button>
        </form>
    </div>
    <?php include 'theme/footer.php'; ?>
</body>
</html>
