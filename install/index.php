<?php
    $error = '';
    $success = '';

    if (file_exists('../config.php')) {
        header('Location: ../panel.php'); // Si config.php existe, redirigir al panel
        exit;
    }

    if (isset($_POST['submit'])) {
        $clientId = $_POST['client_id'] ?? '';
        $clientSecret = $_POST['client_secret'] ?? '';
        $redirectUri = $_POST['redirect_uri'] ?? '';
        $adminUserId = $_POST['admin_user_id'] ?? '';
        $logFilePath = $_POST['log_file_path'] ?? '../discord_bot.log';
        $dbType = $_POST['db_type'] ?? 'sqlite';
        $mysqlHost = $_POST['mysql_host'] ?? 'localhost';
        $mysqlUser = $_POST['mysql_user'] ?? '';
        $mysqlPassword = $_POST['mysql_password'] ?? '';
        $mysqlDatabase = $_POST['mysql_database'] ?? '';
        $botControlUrl = $_POST['bot_control_url'] ?? 'http://localhost:8000/';

        if (empty($clientId) || empty($clientSecret) || empty($redirectUri) || empty($adminUserId)) {
            $error = 'Por favor, completa todos los campos requeridos.';
        } else {
            $configContent = "<?php\n";
            $configContent .= "    // --- Configuración de la Aplicación de Discord ---\n";
            $configContent .= "    \$clientId = '" . addslashes($clientId) . "';\n";
            $configContent .= "    \$clientSecret = '" . addslashes($clientSecret) . "';\n";
            $configContent .= "    \$redirectUri = '" . addslashes($redirectUri) . "';\n";
            $configContent .= "    \$tokenUrl = 'https://discord.com/api/oauth2/token';\n";
            $configContent .= "    \$userUrl = 'https://discord.com/api/users/@me';\n";
            $configContent .= "    \$scopes = 'identify';\n";
            $configContent .= "\n";
            $configContent .= "    // --- Configuración del Administrador ---\n";
            $configContent .= "    \$adminUserId = '" . addslashes($adminUserId) . "';\n";
            $configContent .= "\n";
            $configContent .= "    // --- Rutas de Archivos ---\n";
            $configContent .= "    \$logFilePath = '" . addslashes($logFilePath) . "';\n";
            $configContent .= "\n";
            $configContent .= "    // --- Configuración de la Base de Datos ---\n";
            $configContent .= "    \$dbType = '" . addslashes($dbType) . "';\n";
            $configContent .= "    \$mysqlHost = '" . addslashes($mysqlHost) . "';\n";
            $configContent .= "    \$mysqlUser = '" . addslashes($mysqlUser) . "';\n";
            $configContent .= "    \$mysqlPassword = '" . addslashes($mysqlPassword) . "';\n";
            $configContent .= "    \$mysqlDatabase = '" . addslashes($mysqlDatabase) . "';\n";
            $configContent .= "\n";
            $configContent .= "    // --- Configuración del Servidor para Comandos del Bot ---\n";
            $configContent .= "    \$botControlUrl = '" . addslashes($botControlUrl) . "';\n";
            $configContent .= "?>\n";

            if (file_put_contents('../config.php', $configContent)) {
                $success = 'El archivo config.php ha sido creado exitosamente. Ahora puedes intentar acceder al <a href="../panel.php">Panel de Control</a>.';

                // Intentar conectar a MySQL y crear tablas si se eligió MySQL
                if ($dbType === 'mysql') {
                    require_once '../config.php'; // Incluir el recién creado config
                    $conn = new mysqli($mysqlHost, $mysqlUser, $mysqlPassword, $mysqlDatabase);
                    if ($conn->connect_error) {
                        $success .= '<div class="alert alert-warning mt-3" role="alert">Error al conectar a MySQL: ' . $conn->connect_error . '. Asegúrate de que la base de datos exista.</div>';
                    } else {
                        $sqlCreateTable = "
                            CREATE TABLE IF NOT EXISTS voice_activity (
                                user_id BIGINT PRIMARY KEY,
                                last_connection_24h TEXT,
                                last_connection_7d TEXT
                            )
                        ";
                        if ($conn->query($sqlCreateTable) === TRUE) {
                            $success .= '<div class="alert alert-success mt-3" role="alert">Tabla `voice_activity` creada en MySQL exitosamente.</div>';
                        } else {
                            $success .= '<div class="alert alert-danger mt-3" role="alert">Error al crear la tabla `voice_activity` en MySQL: ' . $conn->error . '</div>';
                        }
                        $conn->close();
                    }
                }
            } else {
                $error = 'Error al crear el archivo config.php. Asegúrate de que el servidor tenga permisos de escritura en el directorio raíz.';
            }
        }
    }
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instalación del Bot</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Instalación del Bot</h2>
        <?php if ($error): ?>
            <div class="alert alert-danger" role="alert"><?php echo $error; ?></div>
        <?php endif; ?>
        <?php if ($success): ?>
            <div class="alert alert-success" role="alert"><?php echo $success; ?></div>
            <p><a href="../panel.php" class="btn btn-primary">Ir al Panel de Control</a></p>
        <?php else: ?>
            <form method="post">
                <div class="form-group">
                    <label for="client_id">Client ID de Discord:</label>
                    <input type="text" class="form-control" id="client_id" name="client_id" required>
                    <small class="form-text text-muted">El ID de tu aplicación de Discord.</small>
                </div>
                <div class="form-group">
                    <label for="client_secret">Client Secret de Discord:</label>
                    <input type="text" class="form-control" id="client_secret" name="client_secret" required>
                    <small class="form-text text-muted">El secreto de tu aplicación de Discord.</small>
                </div>
                <div class="form-group">
                    <label for="redirect_uri">Redirect URI:</label>
                    <input type="url" class="form-control" id="redirect_uri" name="redirect_uri" required placeholder="https://tu-dominio.com/callback.php">
                    <small class="form-text text-muted">La URL de retorno configurada en tu aplicación de Discord.</small>
                </div>
                <div class="form-group">
                    <label for="admin_user_id">ID del Usuario Administrador:</label>
                    <input type="text" class="form-control" id="admin_user_id" name="admin_user_id" required>
                    <small class="form-text text-muted">El ID del usuario de Discord que será el administrador.</small>
                </div>
                <div class="form-group">
                    <label for="log_file_path">Ruta del Archivo de Log:</label>
                    <input type="text" class="form-control" id="log_file_path" name="log_file_path" value="../discord_bot.log">
                    <small class="form-text text-muted">La ruta donde el bot guarda el archivo de log.</small>
                </div>
                <hr class="my-4">
                <h5>Configuración de la Base de Datos</h5>
                <div class="form-group">
                    <label for="db_type">Tipo de Base de Datos:</label>
                    <select class="form-control" id="db_type" name="db_type">
                        <option value="sqlite" selected>SQLite</option>
                        <option value="mysql">MySQL</option>
                    </select>
                </div>
                <div id="mysql_config" style="display: none;">
                    <div class="form-group">
                        <label for="mysql_host">Host de MySQL:</label>
                        <input type="text" class="form-control" id="mysql_host" name="mysql_host" value="localhost">
                    </div>
                    <div class="form-group">
                        <label for="mysql_user">Usuario de MySQL:</label>
                        <input type="text" class="form-control" id="mysql_user" name="mysql_user">
                    </div>
                    <div class="form-group">
                        <label for="mysql_password">Contraseña de MySQL:</label>
                        <input type="password" class="form-control" id="mysql_password" name="mysql_password">
                    </div>
                    <div class="form-group">
                        <label for="mysql_database">Nombre de la Base de Datos MySQL:</label>
                        <input type="text" class="form-control" id="mysql_database" name="mysql_database">
                    </div>
                </div>
                <hr class="my-4">
                <h5>Configuración Opcional del Control del Bot</h5>
                <div class="form-group">
                    <label for="bot_control_url">URL de Control del Bot:</label>
                    <input type="url" class="form-control" id="bot_control_url" name="bot_control_url" value="http://localhost:8000/">
                    <small class="form-text text-muted">URL base para enviar comandos al bot (si implementas un servidor web separado).</small>
                </div>
                <button type="submit" name="submit" class="btn btn-primary">Guardar Configuración</button>
            </form>
        <?php endif; ?>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const dbTypeSelect = document.getElementById('db_type');
            const mysqlConfigDiv = document.getElementById('mysql_config');

            function toggleMysqlConfig() {
                if (dbTypeSelect.value === 'mysql') {
                    mysqlConfigDiv.style.display = 'block';
                } else {
                    mysqlConfigDiv.style.display = 'none';
                }
            }

            dbTypeSelect.addEventListener('change', toggleMysqlConfig);
            toggleMysqlConfig(); // Inicializar al cargar la página
        });
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
