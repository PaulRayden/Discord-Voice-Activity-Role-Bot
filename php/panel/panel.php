<?php
    session_start();
    require_once 'config.php';

    if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
        header('Location: index.php');
        die();
    }

    // Función para leer las últimas líneas del archivo de log
    function tailFile($filepath, $lines = 20) {
        $f = @fopen($filepath, "r");
        if ($f === false) return false;
        $buffer = '';
        $fsize = filesize($filepath);
        $pos = $fsize;
        $linecount = 0;
        while ($linecount < $lines && $pos > 0) {
            $offset = min($pos, 4096);
            $pos -= $offset;
            fseek($f, $pos);
            $buffer = fread($f, $offset) . $buffer;
        }
        fclose($f);
        $lines = explode("\n", trim($buffer));
        $lines = array_slice($lines, - $lines);
        return array_reverse($lines);
    }

    $logs = tailFile($logFilePath);

    // Función para obtener el uso de recursos (solo Linux)
    function getResourceUsage() {
        $cpu = shell_exec("top -bn1 | grep 'Cpu(s)' | sed 's/.*: *\\([0-9.]*\\).*/\\1/'");
        $memTotal = trim(shell_exec("free -m | grep Mem | awk '{print $2}'"));
        $memUsed = trim(shell_exec("free -m | grep Mem | awk '{print $3}'"));
        $uploadSpeed = trim(shell_exec("ifconfig | grep 'TX bytes' | awk '{print $5}'")); // Simplificado, puede variar
        return [
            'cpu' => round($cpu, 2) . '%',
            'memory' => $memUsed . 'MB / ' . $memTotal . 'MB',
            'upload' => $uploadSpeed
        ];
    }

    $resources = getResourceUsage();

    // Función para ejecutar comandos del bot (necesitarás un mecanismo más robusto en producción)
    function sendBotCommand($command) {
        global $botControlUrl;
        if ($command === 'shutdown') {
            file_get_contents($botControlUrl . 'shutdown'); // Asumiendo un pequeño servidor web para comandos
        } elseif ($command === 'restart') {
            file_get_contents($botControlUrl . 'restart'); // Asumiendo un pequeño servidor web para comandos
        }
    }

    if (isset($_POST['bot_action'])) {
        $action = $_POST['bot_action'];
        sendBotCommand($action);
        // Redirigir para evitar el reenvío del formulario
        header("Location: panel.php");
        exit();
    }
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Control del Bot</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="../../css/style.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Panel de Control del Bot</h2>
        <div class="mb-3">
            <h3>Control del Bot</h3>
            <form method="post" class="form-inline">
                <button type="submit" name="bot_action" value="start" class="btn btn-success mr-2" disabled>Iniciar (No implementado)</button>
                <button type="submit" name="bot_action" value="restart" class="btn btn-warning mr-2">Reiniciar (Requiere configuración externa)</button>
                <button type="submit" name="bot_action" value="shutdown" class="btn btn-danger">Apagar</button>
            </form>
            <small class="form-text text-muted">Los botones de Iniciar y Reiniciar requieren una configuración adicional en el servidor.</small>
        </div>
        <div>
            <h3>Logs del Bot</h3>
            <div class="log-console">
                <?php if ($logs): ?>
                    <?php foreach ($logs as $line): ?>
                        <p><?php echo htmlspecialchars($line); ?></p>
                    <?php endforeach; ?>
                <?php else: ?>
                    <p>No se encontraron logs o el archivo no es accesible.</p>
                <?php endif; ?>
            </div>
        </div>
        <div class="mt-3">
            <h3>Uso de Recursos del Servidor</h3>
            <ul>
                <li><strong>CPU:</strong> <?php echo $resources['cpu']; ?></li>
                <li><strong>Memoria:</strong> <?php echo $resources['memory']; ?></li>
                <li><strong>Subida (TX):</strong> <?php echo $resources['upload']; ?></li>
            </ul>
            <small class="form-text text-muted">La información del uso de recursos puede variar según el sistema operativo y la configuración del servidor.</small>
        </div>
        <p class="mt-3"><a href="logout.php" class="btn btn-secondary">Cerrar Sesión</a></p>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
