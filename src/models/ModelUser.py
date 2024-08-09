from .entities.User import User
class ModelUser():
    @classmethod
    def login(self, db, usuarios):
        try:
            cursor = db.connection.cursor()
            sql = """ SELECT nombre, apellido, num_tel, correo, contraseña, num_usuario FROM usuarios
                WHERE correo = '{}'""".format(usuarios.correo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                is_valid_password = User.check_password(row[4], usuarios.contraseña)
                usuarios = User(row[3], User.check_password(row[4], usuarios.contraseña), row[5])
                return usuarios
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, num_usuario):
        try:
            cursor = db.connection.cursor()
            sql = " SELECT nombre, apellido, num_tel, correo, num_usuario FROM usuarios WHERE num_usuario = {} ".format(num_usuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[3], None, row[4], row[0], row[1], row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
