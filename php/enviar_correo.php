<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require '../vendor/autoload.php'; // Asegúrate de que la ruta sea correcta

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = htmlspecialchars($_POST['nombre']);
    $email = htmlspecialchars($_POST['email']);
    $mensaje = htmlspecialchars($_POST['mensaje']);

    $mail = new PHPMailer(true);

    try {
        // Configuración del servidor
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com'; // Cambiado a smtp.gmail.com
        $mail->SMTPAuth = true;
        $mail->Username = 'vanepotter19@gmail.com'; // Nombre de usuario SMTP
        $mail->Password = 'dbjq aojm vnfn vhpf'; // Contraseña SMTP (o contraseña de aplicación)
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; // Usa STARTTLS
        $mail->Port = 587; // Puerto para STARTTLS

        // Configuración del contenido
        $mail->setFrom($email, $nombre);
        $mail->addAddress('vanepotter19@gmail.com');
        $mail->isHTML(true);
        $mail->Subject = "Nuevo mensaje de contacto de $nombre";
        $mail->Body = "Nombre: $nombre<br>Email: $email<br><br>Mensaje:<br>$mensaje";

        // Habilitar depuración para ayudar a diagnosticar problemas
        $mail->SMTPDebug = 0; // Cambiar a 0 para desactivar la depuración
        $mail->Debugoutput = 'html';

        $mail->send();
        header("Location: ../contactanos.html?success=1");
        exit();

    } catch (Exception $e) {
        echo "Error al enviar el mensaje: {$mail->ErrorInfo}";
    }
} else {
    echo "Método no permitido.";
}
?>
