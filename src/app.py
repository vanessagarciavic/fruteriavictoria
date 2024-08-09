import dbm
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from config import config

#Models
from models.ModelUser import ModelUser

#Entities:
from models.entities.User import User
from models.entities.Pedido import Pedido
from models.entities.DetallePedido import DetallePedido

app = Flask(__name__)

app.config.from_object(config['development'])
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(num_usuario):
    return ModelUser.get_by_id(db, num_usuario)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vanepotter19@gmail.com'
app.config['MAIL_PASSWORD'] = 'dbjq aojm vnfn vhpf'  # Contraseña de aplicación (mejor usar variables de entorno)

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/productos/fruta')
def fruta():
    return render_template('categorias/frutas.html')

@app.route('/productos/verdura')
def verdura():
    return render_template('categorias/verduras.html')

@app.route('/productos/chiles')
def chiles():
    return render_template('categorias/chiles.html')

@app.route('/productos/otros')
def otros():
    return render_template('categorias/otros.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/contactanos', methods=['GET', 'POST'])
def contactanos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        msg = Message(f"Nuevo mensaje de contacto de {nombre}",
                      sender=email,
                      recipients=['vanepotter19@gmail.com'])
        msg.html = f"Nombre: {nombre}<br>Email: {email}<br><br>Mensaje:<br>{mensaje}"
        
        try:
            mail.send(msg)
            return redirect(url_for('contactanos', success=True))
        except Exception as e:
            return f"Error al enviar el mensaje: {str(e)}"

    return render_template('contactanos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       # correo = request.form['correo']
        # contraseña = request.form['contraseña']
        usuarios = User(request.form['correo'], request.form['contraseña'], 0)
        logged_usuarios = ModelUser.login(db, usuarios)
        if logged_usuarios is not None:
            if logged_usuarios.contraseña:
                login_user(logged_usuarios)
                return redirect(url_for('menuu'))
            else:
                flash("Contraseña incorrecta")
                return render_template('login/login.html')
        else:
            flash("Usuario no encontrado")
        return render_template('login/login.html')
    else:
        return render_template('login/login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        num_tel = request.form['numtel']
        correo = request.form['correo']
        contraseña = generate_password_hash(request.form['contraseña'])

        # Código para insertar el nuevo usuario en la base de datos
        cursor = db.connection.cursor()
        sql = """INSERT INTO usuarios (nombre, apellido, num_tel, correo, contraseña) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nombre, apellido, num_tel, correo, contraseña))
        db.connection.commit()

        flash("Usuario registrado")
        return redirect(url_for('login'))
    else:
        return render_template('login/registro.html')
    

@app.route('/inicio')
@login_required
def index2():
    return render_template('usuario_comprador/index.html')

@app.route('/productos-usuario')
@login_required
def productos2():
    return render_template('usuario_comprador/productos.html')

@app.route('/productos/fruta-usuario')
@login_required
def fruta2():
    return render_template('usuario_comprador/categorias/frutas.html')

@app.route('/productos/verdura-usuario')
@login_required
def verdura2():
    return render_template('usuario_comprador/categorias/verduras.html')

@app.route('/productos/chiles-usuario')
@login_required
def chiles2():
    return render_template('usuario_comprador/categorias/chiles.html')

@app.route('/productos/otros-usuario')
@login_required
def otros2():
    return render_template('usuario_comprador/categorias/otros.html')

@app.route('/historia-usuario')
@login_required
def historia2():
    return render_template('usuario_comprador/historia.html')

@app.route('/contactanos-usuario', methods=['GET', 'POST'])
@login_required
def contactanos2():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        msg = Message(f"Nuevo mensaje de contacto de {nombre}",
                      sender=email,
                      recipients=['vanepotter19@gmail.com'])
        msg.html = f"Nombre: {nombre}<br>Email: {email}<br><br>Mensaje:<br>{mensaje}"
        
        try:
            mail.send(msg)
            return redirect(url_for('contactanos', success=True))
        except Exception as e:
            return f"Error al enviar el mensaje: {str(e)}"

    return render_template('usuario_comprador/contactanos.html')

    
@app.route('/menu-usuario')
@login_required
def menuu():
    print(f"Current User: {current_user.__dict__}")
    return render_template('usuario_comprador/menu.html')

@app.route('/carrito')
@login_required
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    carrito = session['carrito']
    productos = []
    total = 0
    
    cursor = db.connection.cursor()
    for item in carrito:
        cursor.execute("SELECT id, nombre, precio FROM productos WHERE id = %s", (item,))
        producto = cursor.fetchone()
        productos.append(producto)
        total += producto[2]

    return render_template('carrito1.html', productos=productos, total=total)

@app.route('/carrito-usuario')
@login_required
def carrito2():
    if 'carrito' not in session:
        session['carrito'] = []
    carrito = session.get('carrito', [])
    productos = {}
    total = 0
    gramos_totales = 0
    
    cursor = db.connection.cursor()
    for item in carrito:
        cursor.execute("SELECT id, nombre, cont, precio FROM productos WHERE id = %s", (item,))
        producto = cursor.fetchone()

        if producto:
            producto_id = producto[0]
            nombre = producto[1]
            gramos = producto[2]
            precio = producto[3]

            if producto_id in productos:
                productos[producto_id]['gramos'] += gramos
                productos[producto_id]['total_precio'] += precio
            else:
                productos[producto_id] = {
                    'id': producto_id,
                    'nombre': nombre,
                    'gramos': gramos,
                    'total_precio': precio
                }
            
            total += precio
            gramos_totales += gramos
    productos_lista = list(productos.values())

    return render_template('usuario_comprador/carrito.html', productos=productos_lista, total=total, gramos=gramos_totales)

@app.route('/agregar_carrito/<int:producto_id>')
@login_required
def agregar_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(producto_id)
    session.modified = True
    return redirect(url_for('carrito2'))

@app.route('/realizar-compra', methods=['POST'])
@login_required
def realizar_compra():
    print('funciona')
    if 'carrito' in session and 'id_direccion' in session and 'id_metodo' in session:
        carrito = session['carrito']
        id_direccion = session['id_direccion']
        id_metodo = session['id_metodo']
        total = 0
        cursor = db.connection.cursor()
        print('funciona')
        # Calcular el total del pedido
        for item in carrito:
            cursor.execute("SELECT precio FROM productos WHERE id = %s", (item,))
            precio = cursor.fetchone()[0]
            total += precio
        print('funciona')
        # Crear el pedido
        cursor.execute("INSERT INTO pedidos (usuario_id, direccion_id, metodo_id, total) VALUES (%s, %s, %s, %s)", (current_user.num_usuario, id_direccion, id_metodo, total))
        pedido_id = cursor.lastrowid
        print('funciona')
        # Insertar los detalles del pedido
        for item in carrito:
            cursor.execute("SELECT precio FROM productos WHERE id = %s", (item,))
            precio = cursor.fetchone()[0]
            cursor.execute("INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                           (pedido_id, item, 1, precio))
        print('funciona')
        db.connection.commit()
        session.pop('carrito', None)
        session.pop('id_direccion', None)
        session.pop('id_metodo', None)
        return redirect(url_for('pedido_exitoso'))
    
    print('funciona')
    return redirect(url_for('carrito2'))
                         
@app.route('/elegir-dir')
@login_required
def elegir_dir():
    if 'direccion' not in session:
        session['direccion'] = []
    direcciones = []
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, calle, num, colonia, ciudad, num_usuario FROM direcciones WHERE num_usuario = %s", (current_user.num_usuario,))
    rows = cursor.fetchall()
    num_direccion = 1
    for row in rows:
            direccion = (row[0], row[1], row[2], row[3], row[4])
            direcciones.append(direccion)
            num_direccion += 1


    return render_template('usuario_comprador/menu/elegir_dir.html', direcciones=direcciones)


@app.route('/elegir-met')
@login_required
def elegir_met():
    if 'direccion' not in session:
        session['direccion'] = []
    metodos = []
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, num_tarjeta FROM metodos_pago WHERE num_usuario = %s", (current_user.num_usuario,))
    rows = cursor.fetchall()
    num_tarjeta = 1
    for row in rows:
            metodo = (row[0], row[1])
            metodos.append(metodo)
            num_tarjeta += 1

    return render_template('usuario_comprador/menu/elegir_met.html', metodos=metodos)

@app.route('/set_direccion', methods=['POST'])
@login_required
def set_direccion():
    id_direccion = request.form.get('id_direccion')
    session['id_direccion'] = id_direccion
    return redirect(url_for('elegir_met'))

@app.route('/set_metodo', methods=['POST'])
@login_required
def set_metodo():
    id_metodo = request.form.get('id_metodo')
    session['id_metodo'] = id_metodo
    print('funciona')
    return redirect(url_for('realizar_compra'))

@app.route('/pedido_exitoso')
@login_required
def pedido_exitoso():
    return render_template('usuario_comprador/menu/pedidos.html')


@app.route('/mis_pedidos')
@login_required
def mis_pedidos():
    pedidos = []
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, fecha, total FROM pedidos WHERE usuario_id = %s", (current_user.num_usuario,))
    rows = cursor.fetchall()
    num_pedido = 1
    for row in rows:
            pedido = (num_pedido, row[1], row[2])
            pedidos.append(pedido)
            num_pedido += 1
    usuario = (current_user.num_usuario)
    print(usuario)
    return render_template('usuario_comprador/menu/pedidos.html', pedidos=pedidos)

@app.route('/delete-ped/<string:id_ped>')
@login_required
def delete_ped(id_ped):
    id_pedidos = []
    cursor = db.connection.cursor()
    cursor.execute('SELECT id FROM pedidos WHERE usuario_id = %s', (current_user.num_usuario,))
    resultados = cursor.fetchall()

    for resultado in resultados:
            id_ped = (resultado[0])

    cursor.execute('DELETE FROM pedidos WHERE id = %s', (id_ped,))
    db.connection.commit()
    flash('Pedido eliminado')
    return redirect(url_for('mis_pedidos'))
    


@app.route('/mis_datos', methods=['GET', 'POST'])
@login_required
def mis_datos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        num_tel = request.form['numtel']
        correo = request.form['correo']
        contraseña = generate_password_hash(request.form['contraseña'])

        cursor = db.connection.cursor()
        sql = """UPDATE usuarios 
                 SET nombre = %s, apellido = %s, num_tel = %s, correo = %s, contraseña = %s
                 WHERE num_usuario = %s"""
        cursor.execute(sql, (nombre, apellido, num_tel, correo, contraseña, current_user.num_usuario))
        db.connection.commit()

        flash("Datos actualizados correctamente")
        return redirect(url_for('menuu'))
    else:
        return render_template('usuario_comprador/menu/datos.html', usuario=current_user)

@app.route('/direcciones')
@login_required
def direcciones():
    direcciones = []
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, calle, num, colonia, ciudad, num_usuario FROM direcciones WHERE num_usuario = %s", (current_user.num_usuario,))
    rows = cursor.fetchall()
    num_direccion = 1
    for row in rows:
            direccion = (num_direccion, row[1], row[2], row[3], row[4], row[5])
            direcciones.append(direccion)
            num_direccion += 1
    usuario = (current_user.num_usuario)
    print(usuario)
    return render_template('usuario_comprador/menu/direcciones.html', direcciones=direcciones)


@app.route('/agregar-direccion', methods=['GET', 'POST'])
@login_required
def agregar_direccion():
    if request.method == 'POST':
        calle = request.form['calle']
        num = request.form['num']
        colonia = request.form['colonia']
        ciudad = request.form['ciudad']

        # Código para insertar el nuevo usuario en la base de datos
        cursor = db.connection.cursor()
        sql = """INSERT INTO direcciones (calle, num, colonia, ciudad, num_usuario) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (calle, num, colonia, ciudad, current_user.num_usuario))
        db.connection.commit()

        flash("Direccion registrada")
        return redirect(url_for('direcciones'))
    
    return render_template('usuario_comprador/menu/agregar_direcciones.html')


@app.route('/delete-dir/<string:id_dir>')
def delete_dir(id_dir):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id FROM direcciones WHERE num_usuario = %s', (current_user.num_usuario,))
    resultados = cursor.fetchall()

    for resultado in resultados:
            id_dir = (resultado[0])

    cursor.execute('DELETE FROM direcciones WHERE id = %s', (id_dir,))
    db.connection.commit()
    flash('Direccion eliminada')
    return redirect(url_for('direcciones'))

@app.route('/editar-dir/<string:id>', methods=['GET', 'POST'])
def editar_dir(id):
    cursor = db.connection.cursor()
    
    # Obtener la dirección actual
    cursor.execute('SELECT * FROM direcciones WHERE num_usuario = %s', (current_user.num_usuario,))    
    direcciones = cursor.fetchall()
    
    for direccion in direcciones:
            id = (direccion[0])

    if request.method == 'POST':
        nueva_calle = request.form['calle']
        nuevo_num = request.form['num']
        nueva_colonia = request.form['colonia']
        nueva_ciudad = request.form['ciudad']

        sql = """UPDATE direcciones 
                 SET calle = %s, num = %s, colonia = %s, ciudad = %s 
                 WHERE id = %s AND num_usuario = %s"""
        cursor.execute(sql, (nueva_calle, nuevo_num, nueva_colonia, nueva_ciudad, id, current_user.num_usuario))
        db.connection.commit()

        flash("Dirección actualizada correctamente")
        return redirect(url_for('direcciones'))
    
    return render_template('usuario_comprador/menu/editar_direccion.html', direccion=direccion)

@app.route('/metodos-pago')
@login_required
def metodos_pago():
    metodos = []
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, num_tarjeta, nombre, apellido, fecha_exp, cvv, num_usuario FROM metodos_pago WHERE num_usuario = %s", (current_user.num_usuario,))
    rows = cursor.fetchall()
    num_metodo = 1
    for row in rows:
            metodo = (num_metodo, row[1], row[2], row[3], row[4], row[5], row[6])
            metodos.append(metodo)
            num_metodo+= 1
    usuario = (current_user.num_usuario)
    print(usuario)
    return render_template('usuario_comprador/menu/metodos.html', metodos=metodos)


@app.route('/agregar-metodo', methods=['GET', 'POST'])
def agregar_metodo():
    if request.method == 'POST':
        num_tarjeta = request.form['num_tarjeta']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_exp = request.form['fecha_exp']
        cvv = request.form['cvv']

        cursor = db.connection.cursor()
        sql = """INSERT INTO metodos_pago (num_tarjeta, nombre, apellido, fecha_exp, cvv, num_usuario) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (num_tarjeta, nombre, apellido, fecha_exp, cvv, current_user.num_usuario))
        db.connection.commit()

        flash("Tarjeta registrada")
        return redirect(url_for('metodos_pago'))
    
    return render_template('usuario_comprador/menu/agregar_metodos.html')

@app.route('/delete-metodo/<string:id_met>')
def delete_metodo(id_met):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id FROM metodos_pago WHERE num_usuario = %s', (current_user.num_usuario,))
    resultados = cursor.fetchall()

    for resultado in resultados:
            id_met = (resultado[0])

    cursor.execute('DELETE FROM metodos_pago WHERE id = %s', (id_met,))
    db.connection.commit()
    flash('Tarjeta eliminada')
    return redirect(url_for('metodos_pago'))

@app.route('/editar-metodo/<string:id>', methods=['GET', 'POST'])
def editar_metodo(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM metodos_pago WHERE num_usuario = %s', (current_user.num_usuario,))    
    metodos = cursor.fetchall()
    
    for metodo in metodos:
            id = (metodo[0])

    if request.method == 'POST':
        nueva_num_tarjeta = request.form['num_tarjeta']
        nueva_nombre = request.form['nombre']
        nueva_apellido = request.form['apellido']
        nueva_fecha_exp = request.form['fecha_exp']
        nueva_cvv = request.form['cvv']

        sql = """UPDATE metodos_pago
                 SET num_tarjeta = %s, nombre = %s, apellido = %s, fecha_exp = %s, cvv = %s
                 WHERE id = %s AND num_usuario = %s"""
        cursor.execute(sql, (nueva_num_tarjeta, nueva_nombre, nueva_apellido, nueva_fecha_exp, nueva_cvv, id, current_user.num_usuario))
        db.connection.commit()

        flash("Tarjeta actualizada correctamente")
        return redirect(url_for('metodos_pago'))
    
    return render_template('usuario_comprador/menu/editar_metodo.html', metodo=metodo)

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.cart = session.get('carrito', [])
    db.connection.commit()
    session.pop('carrito', None)
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

