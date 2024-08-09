<?php
$servername = "localhost";  // Cambia esto por tu host, ej. 'localhost'
$username = "root";  // Tu nombre de usuario
$password = "mysql123";  // Tu contraseña
$dbname = "fruteriavictoria";  // Nombre de tu base de datos

// Crear la conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
echo "Conexión exitosa a la base de datos fruteriavictoria";

// Aquí puedes realizar operaciones con la base de datos

// Cerrar la conexión
$conn->close();
?>