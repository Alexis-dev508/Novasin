from distutils.log import error
import email
from encodings import normalize_encoding
from flask import Flask, request, session, flash
from flask import render_template, redirect
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import os
import errno

app = Flask(__name__) #Le asigna el mismo nombre que el archivo

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="alexisdev508",
    password="123456guessanovasin",
    hostname="alexisdev508.mysql.pythonanywhere-services.com",
    databasename="alexisdev508$novasin",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'H%23^2FY6673HN'

db = SQLAlchemy(app)

class Carrusel(db.Model):

    __tablename__ = "carruseles"
    pk_carrusel = db.Column(db.Integer, primary_key = True, autoincrement=True)
    titulo1=db.Column(db.String(300), nullable=False)
    titulo2=db.Column(db.String(300), nullable=False)
    titulo3=db.Column(db.String(300), nullable=False)
    titulo4=db.Column(db.String(300), nullable=False)
    titulo5=db.Column(db.String(300), nullable=False)
    imagen1= db.Column(db.String(300), nullable=False)
    imagen2= db.Column(db.String(300), nullable=False)
    imagen3= db.Column(db.String(300), nullable=False)
    imagen4= db.Column(db.String(300), nullable=False)
    imagen5= db.Column(db.String(300), nullable=False)

class Categoria(db.Model):
    __tablename__ = "categorias"
    pk_categoria= db.Column(db.Integer, primary_key = True, autoincrement=True) 
    nombreCategoria= db.Column(db.String(300), nullable=False) 
    descripcionCategoria= db.Column(db.String(300), nullable=False) 
    imagenCaratula= db.Column(db.String(300), nullable=False) 
    imagen1= db.Column(db.String(300), nullable=False) 
    imagen2= db.Column(db.String(300), nullable=False) 
    imagen3= db.Column(db.String(300), nullable=False) 
    imagen4= db.Column(db.String(300), nullable=False) 
    imagen5= db.Column(db.String(300), nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    pk_usuario = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    nombre = db.Column(db.String(300), nullable=False) 
    password = db.Column(db.String(300), nullable=False)
    email_usuario = db.Column(db.String(300), nullable=False)
    telefono = db.Column(db.String(300), nullable=False) 
    ciudad = db.Column(db.String(300), nullable=False)
    tipo_usuario = db.Column(db.String(300), nullable=False) 

class Producto(db.Model):
    __tablename__: "productos"
    pk_producto = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    nombre_producto = db.Column(db.String(300))
    descripcion_producto = db.Column(db.String(1000))
    precio_producto = db.Column(db.String(300), nullable=False)
    estatus = db.Column(db.String(300), nullable=False)
    imagen1 = db.Column(db.String(300), nullable=False) 
    imagen2 = db.Column(db.String(300), nullable=False) 
    imagen3 = db.Column(db.String(300), nullable=False) 
    imagen4 = db.Column(db.String(300), nullable=False) 
    imagen5 = db.Column(db.String(300), nullable=False) 
    imagen6 = db.Column(db.String(300), nullable=False) 
    imagen7 = db.Column(db.String(300), nullable=False) 
    imagen8 = db.Column(db.String(300), nullable=False) 
    imagen9 = db.Column(db.String(300), nullable=False) 
    imagen10 = db.Column(db.String(300), nullable=False) 
    fk_categoria = db.Column(db.Integer, db.ForeignKey(db.categorias.pk_categoria), nullable=False)

@app.route('/') #Sirve para señalar que cuando busque la diagonal, Flask cargue automaticamente el index
def index(): #Funcion para cargar el index
    consulta_categorias = 'SELECT * FROM categorias'
    consulta_carrusel = 'SELECT * FROM carruseles LIMIT 1'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta_categorias) 
    categorias = cur.fetchall() 
    cur.execute(consulta_carrusel) 
    carrusel = cur.fetchone() 
    con.commit() 
    return render_template('index.html', categorias = categorias, carruseles = carrusel) #Devuelve la vista del index y le manda variables


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/401')
def page_401():
    return render_template('_html/401.html')


@app.route('/404')
def page_404():
    return render_template('_html/404.html')


@app.route('/503')
def page_503():
    return render_template('_html/503.html')


@app.route('/acerca')
def acerca():
    return render_template('acerca.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')


@app.route('/admin')
def admin():
    try:
        if session['tipo_usuario'] != 'admin':
            return redirect('/401')
        else:
            consulta_categorias = 'SELECT * FROM categorias'
            consulta_productos = 'SELECT * FROM productos'
            consulta_usuarios = 'SELECT * FROM usuarios'
            con = db.connect()
            cur = con.cursor()
            cur.execute(consulta_categorias)
            categorias = cur.fetchall() 

            cur.execute(consulta_productos)
            productos = cur.fetchall() 
            
            cur.execute(consulta_usuarios)
            usuarios = cur.fetchall() 
            con.commit()
            return render_template('admin.html', categorias = categorias, productos = productos, usuarios = usuarios) #Le mandamos el array a la vista para poder usar los datos
    except:
        return redirect('/401')


# /////////////////////USUARIOS//////////////////////
@app.route('/guardar-usuario', methods=['POST']) #Ruta para hacer una insercion o POST
def guardar_usuario():
    nombre = request.form['name'] #Recibiendo los datos del formulario, es importante poner el mismo nombre del input
    contrasena = request.form['new-password']
    confirmarContrasena = request.form['new-password2']
    telefono = request.form['phone']
    email = request.form['email']
    ciudad = request.form['ciudad']
    if contrasena == confirmarContrasena:
        consulta = 'INSERT INTO usuarios (pk_usuario, nombre,password, email_usuario, telefono, ciudad, tipo_usuario) VALUES(NULL, %s,%s, %s, %s, %s, %s)' 
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombre,contrasena, email, telefono, ciudad, 'cliente')) #Le enviamos parametros a la consulta
        con.commit() #Guarda los cambios en la base de datos
        return redirect('/registro') #Retorna el mensaje de guardado
    else:
        return 'Las contraseñas no coinciden'


# /////////////////////////////CATEGORIAS///////////////////////////////////////
@app.route('/guardar-categoria', methods=['POST'])
def guardarCategoria():
    nombreCategoria = request.form['nombreCategoria']
    descripcionCategoria = request.form['descripcionCategoria']
    imagenCaratula = request.files['imagenCaratula']
    imagenCaratulaNombre = 'caratula-' + imagenCaratula.filename
    imagen1 = request.files['imagen1']
    imagen1Nombre = 'imagen1-'+ imagen1.filename
    imagen2 = request.files['imagen2']
    imagen2Nombre = 'imagen2-'+ imagen2.filename
    imagen3 = request.files['imagen3']
    imagen3Nombre = 'imagen3-'+ imagen3.filename
    imagen4 = request.files['imagen4']
    imagen4Nombre = 'imagen4-'+ imagen4.filename
    imagen5 = request.files['imagen5']
    imagen5Nombre = 'imagen5-'+ imagen5.filename
    try:
        os.mkdir(f'./static/images/categorias/{nombreCategoria}')
        imagenCaratula.save(f'./static/images/categorias/{nombreCategoria}/' + imagenCaratulaNombre)
        imagen1.save(f'./static/images/categorias/{nombreCategoria}/' + imagen1Nombre)
        imagen2.save(f'./static/images/categorias/{nombreCategoria}/' + imagen2Nombre)
        imagen3.save(f'./static/images/categorias/{nombreCategoria}/' + imagen3Nombre)
        imagen4.save(f'./static/images/categorias/{nombreCategoria}/' + imagen4Nombre)
        imagen5.save(f'./static/images/categorias/{nombreCategoria}/' + imagen5Nombre)
        consulta = 'INSERT INTO categorias (pk_categoria, nombreCategoria, descripcionCategoria, imagenCaratula, imagen1, imagen2, imagen3, imagen4, imagen5)  VALUES(NULL, %s, %s, %s, %s, %s,%s,%s,%s)' 
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombreCategoria, descripcionCategoria, imagenCaratulaNombre, imagen1Nombre, imagen2Nombre, imagen3Nombre, imagen4Nombre, imagen5Nombre)) #Le enviamos parametros a la consulta
        con.commit() #Guarda los cambios en la base de datos
        return redirect('/admin')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@app.route('/editar-categoria/<int:idcategoria>')
def editar_categoria(idcategoria):
    consulta = 'SELECT * FROM categorias WHERE pk_categoria = %s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta, (idcategoria))
    registro = cur.fetchall()
    con.commit()
    return render_template('editar-categoria.html', registro=registro) #Le mandamos el array a la vista para poder usar los datos




@app.route('/actualizar-categoria', methods=['POST']) #Ruta para hacer una insercion o POST
def actualizar_categoria():
    idCategoria = request.form['pk_categoria']
    nombreCategoria = request.form['nombreCategoria']
    nombreCategoriaRespaldo = request.form['nombreCategoriaRespaldo']
    descripcionCategoria = request.form['descripcionCategoria']
    imagenCaratula = request.files['imagenCaratula']
    imagenCaratulaNombre = imagenCaratula.filename
    imagen1 = request.files['imagen1']
    imagen1Nombre = imagen1.filename
    imagen2 = request.files['imagen2']
    imagen2Nombre = imagen2.filename
    imagen3 = request.files['imagen3']
    imagen3Nombre = imagen3.filename
    imagen4 = request.files['imagen4']
    imagen4Nombre = imagen4.filename
    imagen5 = request.files['imagen5']
    imagen5Nombre = imagen5.filename
    try:
        listaArchivos = os.listdir(f'./static/images/categorias/{nombreCategoria}/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
        for archivo in listaArchivos:
             os.remove(f'./static/images/categorias/{nombreCategoria}/{archivo}')#Borra el directorio junto con los archivos contenidos
        consulta = "UPDATE categorias SET nombreCategoria = %s, descripcionCategoria = %s, imagenCaratula = %s, imagen1 = %s, imagen2 = %s, imagen3 = %s, imagen4 = %s, imagen5 = %s  WHERE pk_categoria = %s"  
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombreCategoria, descripcionCategoria, imagenCaratulaNombre, imagen1Nombre, imagen2Nombre, imagen3Nombre, imagen4Nombre, imagen5Nombre, idCategoria )) #Le enviamos parametros a la consulta
        imagenCaratula.save(f'./static/images/categorias/{nombreCategoria}/' +'caratula-'+ imagenCaratulaNombre)
        imagen1.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen1-' + imagen1Nombre)
        imagen2.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen2-' + imagen2Nombre)
        imagen3.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen3-' + imagen3Nombre)
        imagen4.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen4-' + imagen4Nombre)
        imagen5.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen5-' + imagen5Nombre)
        con.commit() #Guarda los cambios en la base de datos
        return redirect('/admin')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@app.route('/eliminar-categoria/<int:idcategoria>')
def eliminar_categoria(idcategoria):
    consultaTraerDatos = 'SELECT * FROM categorias WHERE pk_categoria = %s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consultaTraerDatos,(idcategoria))
    registro = cur.fetchone()
    con.commit()
    print(registro)
    listaArchivos = os.listdir(f'./static/images/categorias/{registro[1]}/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
    for archivo in listaArchivos:
        os.remove(f'./static/images/categorias/{registro[1]}/{archivo}')#Borra el directorio junto con los archivos contenidos
    os.rmdir(f'./static/images/categorias/{registro[1]}')
    consulta = 'DELETE FROM categorias WHERE pk_categoria=%s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta,(idcategoria))
    con.commit()
    return redirect('/admin')

# ///////////////////////////// PRODUCTOS //////////////////////////////////
@app.route('/mostrar-productos-categoria/<int:pk_categoria>')
def mostrar_productos_categoria(pk_categoria):
    consulta_productos = 'SELECT * FROM productos WHERE fk_categoria = %s'
    consulta_categoria = 'SELECT * FROM categorias WHERE pk_categoria = %s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta_productos,(pk_categoria))
    productos = cur.fetchall()
    cur.execute(consulta_categoria,(pk_categoria))
    categoria = cur.fetchone()
    con.commit()
    return render_template('productos.html', productos = productos, categoria = categoria)


@app.route('/editar-producto/<int:pk_producto>')
def editar_producto(pk_producto):
    consulta = 'SELECT * FROM productos WHERE pk_producto = %s'
    consulta_categoria = 'SELECT * FROM categorias'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta, (pk_producto))
    producto = cur.fetchall()

    cur.execute(consulta_categoria)
    categorias = cur.fetchall()
    con.commit()
    return render_template('editar-producto.html', producto=producto, categorias = categorias) #Le mandamos el array a la vista para poder usar los datos


@app.route('/guardar-producto', methods = ['POST'])
def guardar_producto():
    nombre_producto = request.form['nombreProducto']
    descripcion_producto = request.form['descripcionProducto']
    precio_producto = request.form['precioProducto']
    status = 'v'
    categoria = request.form['select-categoria']
    imagen1p = request.files['imagen1']
    imagen2p = request.files['imagen2']
    imagen3p = request.files['imagen3']
    imagen4p = request.files['imagen4']
    imagen5p = request.files['imagen5']
    imagen6p = request.files['imagen6']
    imagen7p = request.files['imagen7']
    imagen8p = request.files['imagen8']
    imagen9p = request.files['imagen9']
    imagen10p = request.files['imagen10']
    imagen1pNombre = 'imagen1p-' + imagen1p.filename
    imagen2pNombre = 'imagen2p-' + imagen2p.filename
    imagen3pNombre = 'imagen3p-' + imagen3p.filename
    imagen4pNombre = 'imagen4p-' + imagen4p.filename
    imagen5pNombre = 'imagen5p-' + imagen5p.filename
    imagen6pNombre = 'imagen6p-' + imagen6p.filename
    imagen7pNombre = 'imagen7p-' + imagen7p.filename
    imagen8pNombre = 'imagen8p-' + imagen8p.filename
    imagen9pNombre = 'imagen9p-' + imagen9p.filename
    imagen10pNombre = 'imagen10-' + imagen10p.filename
    try:
        os.mkdir(f'./static/images/productos/{nombre_producto}') 
        imagen1p.save(f'./static/images/productos/{nombre_producto}/' + imagen1pNombre)
        imagen2p.save(f'./static/images/productos/{nombre_producto}/' + imagen2pNombre)
        imagen3p.save(f'./static/images/productos/{nombre_producto}/' + imagen3pNombre)
        imagen4p.save(f'./static/images/productos/{nombre_producto}/' + imagen4pNombre)
        imagen5p.save(f'./static/images/productos/{nombre_producto}/' + imagen5pNombre)
        imagen6p.save(f'./static/images/productos/{nombre_producto}/' + imagen6pNombre)
        imagen7p.save(f'./static/images/productos/{nombre_producto}/' + imagen7pNombre)
        imagen8p.save(f'./static/images/productos/{nombre_producto}/' + imagen8pNombre)
        imagen9p.save(f'./static/images/productos/{nombre_producto}/' + imagen9pNombre)
        imagen10p.save(f'./static/images/productos/{nombre_producto}/' + imagen10pNombre) 
        consulta = 'INSERT INTO productos  VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombre_producto, descripcion_producto, precio_producto, status, imagen1pNombre, imagen2pNombre,imagen3pNombre,imagen4pNombre,imagen5pNombre,imagen6pNombre,imagen7pNombre,imagen8pNombre,imagen9pNombre,imagen10pNombre, categoria)) #Le enviamos parametros a la consulta
        con.commit() #Guarda los cambios en la base de datos
        return redirect('/admin')
    except OSError as e:
        if e.errno != errno.EEXIST:
            return ''


@app.route('/eliminar-producto/<int:pk_producto>')
def eliminar_producto(pk_producto):
    consultaTraerDatos = 'SELECT * FROM productos WHERE pk_producto = %s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consultaTraerDatos,(pk_producto))
    registro = cur.fetchone()
    con.commit()
    listaArchivos = os.listdir(f'./static/images/productos/{registro[1]}/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
    for archivo in listaArchivos:
        os.remove(f'./static/images/productos/{registro[1]}/{archivo}')#Borra el directorio junto con los archivos contenidos
    os.rmdir(f'./static/images/productos/{registro[1]}')
    consulta = 'DELETE FROM productos WHERE pk_producto=%s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta,(pk_producto))
    con.commit()
    return redirect('/admin')


@app.route('/actualizar-producto', methods=['POST']) #Ruta para hacer una insercion o POST
def actualizar_producto():
    nombre_producto = request.form['nombreProducto']
    descripcion_producto = request.form['descripcionProducto']
    precio_producto = request.form['precioProducto']
    status = 'v'
    categoria = request.form['select-categoria']
    imagen1p = request.files['imagen1']
    imagen2p = request.files['imagen2']
    imagen3p = request.files['imagen3']
    imagen4p = request.files['imagen4']
    imagen5p = request.files['imagen5']
    imagen6p = request.files['imagen6']
    imagen7p = request.files['imagen7']
    imagen8p = request.files['imagen8']
    imagen9p = request.files['imagen9']
    imagen10p = request.files['imagen10']
    imagen1pNombre = 'imagen1p-' +imagen1p.filename
    imagen2pNombre = 'imagen2p-' +imagen2p.filename
    imagen3pNombre = 'imagen3p-' +imagen3p.filename
    imagen4pNombre = 'imagen4p-' +imagen4p.filename
    imagen5pNombre = 'imagen5p-' +imagen5p.filename
    imagen6pNombre = 'imagen6p-' +imagen6p.filename
    imagen7pNombre = 'imagen7p-' +imagen7p.filename
    imagen8pNombre = 'imagen8p-' +imagen8p.filename
    imagen9pNombre = 'imagen9p-' +imagen9p.filename
    imagen10pNombre =  'imagen10p-'+imagen10p.filename
    try:
        listaArchivos = os.listdir(f'./static/images/productos/{nombre_producto}/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
        for archivo in listaArchivos:
            os.remove(f'./static/images/productos/{nombre_producto}/{archivo}')#Borra el directorio junto con los archivos contenidos
        imagen1p.save(f'./static/images/productos/{nombre_producto}/' +  imagen1pNombre)
        imagen2p.save(f'./static/images/productos/{nombre_producto}/' +  imagen2pNombre)
        imagen3p.save(f'./static/images/productos/{nombre_producto}/' +  imagen3pNombre)
        imagen4p.save(f'./static/images/productos/{nombre_producto}/' +  imagen4pNombre)
        imagen5p.save(f'./static/images/productos/{nombre_producto}/' +  imagen5pNombre)
        imagen6p.save(f'./static/images/productos/{nombre_producto}/' +  imagen6pNombre)
        imagen7p.save(f'./static/images/productos/{nombre_producto}/' +  imagen7pNombre)
        imagen8p.save(f'./static/images/productos/{nombre_producto}/' +  imagen8pNombre)
        imagen9p.save(f'./static/images/productos/{nombre_producto}/' +  imagen9pNombre)
        imagen10p.save(f'./static/images/productos/{nombre_producto}/' +  imagen10pNombre) 
        consulta = 'UPDATE productos SET nombre_producto=%s, descripcion_producto = %s, precio_producto = %s, imagen1 = %s, imagen2=%s,imagen3=%s,imagen4=%s,imagen5=%s,imagen6=%s,imagen7=%s,imagen8=%s,imagen9=%s,imagen10=%s, fk_categoria=%s'
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombre_producto, descripcion_producto, precio_producto, imagen1pNombre, imagen2pNombre,imagen3pNombre,imagen4pNombre,imagen5pNombre,imagen6pNombre,imagen7pNombre,imagen8pNombre,imagen9pNombre,imagen10pNombre, categoria)) #Le enviamos parametros a la consulta
        con.commit() #Guarda los cambios en la base de datos
        return redirect('/admin')
    except OSError as e:
        if e.errno != errno.EEXIST:
            return 'Algo salio mal'


# /////////////////////////////////USUARIOS///////////////////////////////////
@app.route('/eliminar-usuario/<int:pk_usuario>')
def eliminar_usuario(pk_usuario):
    consulta = 'DELETE FROM usuarios WHERE pk_usuario=%s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta,(pk_usuario))
    con.commit()
    return redirect('/admin')


@app.route('/login', methods=['POST', 'GET'])
def validar_usuario():
    username = request.form['user']
    pass1 = request.form['password']
    consulta = 'SELECT * FROM usuarios WHERE nombre = %s AND password = %s'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta,(username, pass1))
    usuario = cur.fetchone() #Envia todos los datos de la consulta y los guarda en la variable persona
    con.commit()
    if usuario != None:
        session["nombre_usuario"]= usuario[1]
        session["tipo_usuario"]= usuario[6]
        session['pk_usuario'] = usuario[0]

        return redirect('/')
    else:
        flash('El usuario o la contraseña son incorrectos')
        return render_template('./registro.html')


@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')


# ////////////////////////////CARRUSEL PRINCIPAL////////////////////////////////
@app.route('/guardar-imagenes-carrusel', methods=['POST'])
def carrusel_principal():
    titulo_imagen_1 = request.form['titulo_imagen_1']
    titulo_imagen_2 = request.form['titulo_imagen_2']
    titulo_imagen_3 = request.form['titulo_imagen_3']
    titulo_imagen_4 = request.form['titulo_imagen_4']
    titulo_imagen_5 = request.form['titulo_imagen_5']
    imagen1c=request.files['imagen1c']
    imagen2c=request.files['imagen2c']
    imagen3c=request.files['imagen3c']
    imagen4c=request.files['imagen4c']
    imagen5c=request.files['imagen5c']
    imagen1cNombre = imagen1c.filename
    imagen2cNombre = imagen2c.filename
    imagen3cNombre = imagen3c.filename
    imagen4cNombre = imagen4c.filename
    imagen5cNombre = imagen5c.filename
    # try:
    listaArchivos = os.listdir(f'./static/images/carrusel/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
    for archivo in listaArchivos:
        os.remove(f'./static/images/carrusel/{archivo}')#Borra el directorio junto con los archivos contenidos
    imagen1c.save(f'./static/images/carrusel/' + 'imagen1c-' + imagen1cNombre)
    imagen2c.save(f'./static/images/carrusel/' + 'imagen2c-' + imagen2cNombre)
    imagen3c.save(f'./static/images/carrusel/' + 'imagen3c-' + imagen3cNombre)
    imagen4c.save(f'./static/images/carrusel/' + 'imagen4c-' + imagen4cNombre)
    imagen5c.save(f'./static/images/carrusel/' + 'imagen5c-' + imagen5cNombre)
    consulta = 'INSERT INTO carruseles VALUES(NULL, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)'
    borrar = 'DELETE FROM carruseles'
    con = db.connect()
    cur = con.cursor()
    cur.execute(borrar)
    cur.execute(consulta,(titulo_imagen_1,titulo_imagen_2,titulo_imagen_3,titulo_imagen_4,titulo_imagen_5,imagen1cNombre, imagen2cNombre, imagen3cNombre, imagen4cNombre,imagen5cNombre))
    con.commit()
    return redirect('/admin')
    # except OSError as e:
    #     if e.errno != errno.EEXIST:
    #         return 'Algo salio mal'


if __name__ == '__main__':
    app.run(debug=True)