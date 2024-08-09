from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(UserMixin):

    def __init__(self, correo, contraseña, num_usuario, nombre="", apellido="", num_tel="") -> None:
        self.nombre = nombre
        self.apellido = apellido
        self.num_tel = num_tel
        self.correo = correo
        self.contraseña = contraseña
        self.num_usuario = num_usuario

    def get_id(self):
        return str(self.num_usuario)

    @staticmethod
    def check_password(hashed_contraseña, contraseña):
        return check_password_hash(hashed_contraseña, contraseña)

    @staticmethod
    def generate_password(contraseña):
        return generate_password_hash(contraseña)
    
    
        