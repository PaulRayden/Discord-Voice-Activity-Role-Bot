<?php
session_start();

if (isset($_POST['accept_terms']) && isset($_POST['terms_accepted_checkbox'])) {
    $_SESSION['terms_accepted'] = true;
    header('Location: index.php');
    exit;
}

if (isset($_POST['reject_terms'])) {
    $_SESSION['terms_rejected'] = true;
    header('Location: ../index.php?rejected=1'); // Redirigir a la página principal con un mensaje
    exit;
}

if (isset($_SESSION['terms_accepted']) && $_SESSION['terms_accepted'] === true) {
    header('Location: index.php');
    exit;
}

// --- Textos de Términos y Condiciones y Licencia ---
$terms_and_conditions = <<<EOT
Estos Términos y Condiciones rigen el uso de este bot de Discord y su panel de control web asociado (en adelante, el "Servicio"). Al instalar, acceder o utilizar el Servicio, usted acepta estar sujeto a estos términos.

1. **Uso del Servicio:** El Servicio se proporciona para la gestión y administración de un bot de Discord. Usted se compromete a utilizar el Servicio de acuerdo con todas las leyes y regulaciones aplicables, así como con las directrices de Discord.

2. **Responsabilidad del Usuario:** Usted es responsable de todas las acciones realizadas a través de su cuenta de administrador. Debe mantener la confidencialidad de sus credenciales de acceso.

3. **Limitación de Responsabilidad:** El desarrollador de este Servicio no será responsable de ningún daño directo, indirecto, incidental, especial, consecuente o punitivo que surja del uso o la imposibilidad de usar el Servicio.

4. **Recopilación de Datos:** El Servicio puede recopilar ciertos datos de uso para mejorar su funcionalidad. Estos datos se manejarán de acuerdo con la política de privacidad (que podría proporcionarse por separado).

5. **Terminación:** El acceso al Servicio puede ser terminado en cualquier momento, con o sin causa, y sin previo aviso.

6. **Modificaciones:** Estos Términos y Condiciones pueden ser modificados en cualquier momento sin previo aviso. El uso continuado del Servicio después de dichas modificaciones constituye su aceptación de los nuevos términos.

7. **Ley Aplicable:** Estos Términos y Condiciones se regirán e interpretarán de acuerdo con las leyes de [Tu Jurisdicción], sin dar efecto a ningún principio de conflicto de leyes.
EOT;

// Asumimos que ya tienes el texto de tu licencia
// --- Leer el contenido del archivo de licencia ---
$licensePath = '../LICENSE'; // Asegúrate de que la ruta al archivo sea correcta
$license = '';

if (file_exists($licensePath)) {
    $license = file_get_contents($licensePath);
} else {
    $license = 'No se pudo encontrar el archivo de licencia.';
    // O podrías manejar este error de otra manera, como mostrar un mensaje al usuario.
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones / Licencia</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <?php include '../theme/header.php'; ?>
    <div class="container mt-5">
        <h2>Términos y Condiciones</h2>
        <div class="scrollable-box">
            <?php echo nl2br(htmlspecialchars($terms_and_conditions)); ?>
        </div>

        <h2>Licencia</h2>
        <div class="scrollable-box">
            <?php echo nl2br(htmlspecialchars($license)); ?>
        </div>

        <?php if (isset($error_message)): ?>
            <div class="alert alert-danger"><?php echo $error_message; ?></div>
        <?php endif; ?>

        <form method="post" class="mt-3" id="termsForm">
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="accept_terms" name="terms_accepted_checkbox" value="1" required>
                <label class="form-check-label" for="accept_terms">Acepto los términos y condiciones y la licencia.</label>
            </div>
            <button type="submit" class="btn btn-primary mt-3" name="accept_terms">Aceptar y Continuar con la Instalación</button>
            <button type="button" class="btn btn-danger mt-3" id="rejectTermsBtn">Rechazar y Salir</button>
        </form>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const rejectBtn = document.getElementById('rejectTermsBtn');
                rejectBtn.addEventListener('click', function() {
                    window.location.href = '../index.php?rejected=1';
                });
            });
        </script>
    </div>
    <?php include '../theme/footer.php'; ?>
</body>
</html>
