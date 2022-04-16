import email
from encodings import normalize_encoding
from flask import Flask, request, session, flash
from flask import render_template, redirect
from flaskext.mysql import MySQL
import os
import errno


app = Flask(__name__) #Le asigna el mismo nombre que el archivo

db = MySQL()

# app.config['MYSQL_DATABASE_HOST'] = '35.238.174.237'
# app.config['MYSQL_DATABASE_USER'] = 'admin'
# app.config['MYSQL_DATABASE_PASSWORD'] = '123456guessa'
# app.config['MYSQL_DATABASE_DB'] = 'novasin'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'novasin'
app.secret_key = 'H%23^2FY6673HN'


db.init_app(app)


@app.route('/') #Sirve para señalar que cuando busque la diagonal, Flask cargue automaticamente el index
def index(): #Funcion para cargar el index
    consulta = 'SELECT * FROM categorias'
    con = db.connect() #Abre una conexion con MySQL
    cur = con.cursor()
    cur.execute(consulta) #Le enviamos parametros a la consulta
    categorias = cur.fetchall() 
    con.commit() #Guarda los cambios en la base de datos
    return render_template('index.html', categorias = categorias) #Devuelve la vista del index y le manda variables


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
    consulta_categorias = 'SELECT * FROM categorias'
    consulta_productos = 'SELECT * FROM productos'
    consulta_usuarios = 'SELECT * FROM usuarios'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta_categorias)
    categorias = cur.fetchall() #Envia todos los datos de la consulta y los guarda en la variable persona

    cur.execute(consulta_productos)
    productos = cur.fetchall() #Envia todos los datos de la consulta y los guarda en la variable persona
    
    cur.execute(consulta_usuarios)
    usuarios = cur.fetchall() #Envia todos los datos de la consulta y los guarda en la variable persona
    
    con.commit()
    return render_template('admin.html', categorias = categorias, productos = productos, usuarios = usuarios) #Le mandamos el array a la vista para poder usar los datos

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
        os.mkdir(f'./static/images/categorias/{nombreCategoria}')
        imagenCaratula.save(f'./static/images/categorias/{nombreCategoria}/' +'caratula-'+ imagenCaratulaNombre)
        imagen1.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen1-' + imagen1Nombre)
        imagen2.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen2-' + imagen2Nombre)
        imagen3.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen3-' + imagen3Nombre)
        imagen4.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen4-' + imagen4Nombre)
        imagen5.save(f'./static/images/categorias/{nombreCategoria}/' + 'imagen5-' + imagen5Nombre)
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


@app.route('/editar-producto/<int:pk_producto>')
def editar_producto(pk_producto):
    consulta_productos = 'SELECT * FROM productos WHERE pk_producto = %s'
    consulta_categorias = 'SELECT * FROM categorias'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta_productos, (pk_producto))
    registro = cur.fetchall()
    con.commit()
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta_categorias)
    categorias = cur.fetchall()
    con.commit()
    return render_template('editar-producto.html', registro=registro, categorias = categorias) #Le mandamos el array a la vista para poder usar los datos


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
    imagen1pNombre = imagen1p.filename
    imagen2pNombre = imagen2p.filename
    imagen3pNombre = imagen3p.filename
    imagen4pNombre = imagen4p.filename
    imagen5pNombre = imagen5p.filename
    imagen6pNombre = imagen6p.filename
    imagen7pNombre = imagen7p.filename
    imagen8pNombre = imagen8p.filename
    imagen9pNombre = imagen9p.filename
    imagen10pNombre = imagen10p.filename
    try:
        os.mkdir(f'./static/images/productos/{nombre_producto}') 
        imagen1p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen1p-' + imagen1pNombre)
        imagen2p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen2p-' + imagen2pNombre)
        imagen3p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen3p-' + imagen3pNombre)
        imagen4p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen4p-' + imagen4pNombre)
        imagen5p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen5p-' + imagen5pNombre)
        imagen6p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen6p-' + imagen6pNombre)
        imagen7p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen7p-' + imagen7pNombre)
        imagen8p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen8p-' + imagen8pNombre)
        imagen9p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen9p-' + imagen9pNombre)
        imagen10p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen10p-' + imagen10pNombre) 
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
    imagen1pNombre = imagen1p.filename
    imagen2pNombre = imagen2p.filename
    imagen3pNombre = imagen3p.filename
    imagen4pNombre = imagen4p.filename
    imagen5pNombre = imagen5p.filename
    imagen6pNombre = imagen6p.filename
    imagen7pNombre = imagen7p.filename
    imagen8pNombre = imagen8p.filename
    imagen9pNombre = imagen9p.filename
    imagen10pNombre = imagen10p.filename
    try:
        listaArchivos = os.listdir(f'./static/images/productos/{nombre_producto}/') #Obtiene una lista de los nombres de archivos contenidos en la carpeta
        for archivo in listaArchivos:
            os.remove(f'./static/images/productos/{nombre_producto}/{archivo}')#Borra el directorio junto con los archivos contenidos
        imagen1p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen1p-' + imagen1pNombre)
        imagen2p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen2p-' + imagen2pNombre)
        imagen3p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen3p-' + imagen3pNombre)
        imagen4p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen4p-' + imagen4pNombre)
        imagen5p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen5p-' + imagen5pNombre)
        imagen6p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen6p-' + imagen6pNombre)
        imagen7p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen7p-' + imagen7pNombre)
        imagen8p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen8p-' + imagen8pNombre)
        imagen9p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen9p-' + imagen9pNombre)
        imagen10p.save(f'./static/images/productos/{nombre_producto}/' + 'imagen10p-' + imagen10pNombre) 
        consulta = 'UPDATE productos SET nombre_producto=%s, descripcion_producto = %s, precio_producto = %s, imagen1 = %s, imagen2=%s,imagen3=%s,imagen4=%s,imagen5=%s,imagen6=%s,imagen7=%s,imagen8=%s,imagen9=%s,imagen10=%s, fk_categoria=%s'
        con = db.connect() #Abre una conexion con MySQL
        cur = con.cursor()
        cur.execute(consulta,(nombre_producto, descripcion_producto, precio_producto, imagen1pNombre, imagen2pNombre,imagen3pNombre,imagen4pNombre,imagen5pNombre,imagen6pNombre,imagen7pNombre,imagen8pNombre,imagen9pNombre,imagen10pNombre, categoria)) #Le enviamos parametros a la consulta
        con.commit() #Guarda los cambios en la base de datos
        return 'Editado'
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
        return redirect('/')
    else:
        flash('El usuario o la contraseña son incorrectos')
        return render_template('./registro.html')

@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)