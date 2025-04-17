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
$license = <<<EOT
MIT License

Copyright (c) 2025 PaulRayden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOT;
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones / Licencia</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
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

        <form method="post" class="mt-3">
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="accept_terms" name="accept_terms" required>
                <label class="form-check-label" for="accept_terms">Acepto los términos y condiciones y la licencia.</label>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Aceptar y Continuar con la Instalación</button>
            <button type="submit" class="btn btn-danger mt-3" name="reject_terms">Rechazar y Salir</button>
        </form>
    </div>
    <?php include '../theme/footer.php'; ?>
</body>
</html>
