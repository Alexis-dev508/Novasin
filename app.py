# from ast import Try
# from crypt import methods
import email
from encodings import normalize_encoding
from flask import Flask, request
from flask import render_template, redirect
from flaskext.mysql import MySQL
import os
import errno


app = Flask(__name__) #Le asigna el mismo nombre que el archivo

db = MySQL() #Instancia Mysql

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'novasin'
db.init_app(app)


@app.route('/') #Sirve para señalar que cuando busque la diagonal, Flask cargue automaticamente el index
def index(): #Funcion para cargar el index
    return render_template('index.html') #Devuelve la vista del index y le manda variables


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
        return "Guardado" #Retorna el mensaje de guardado
    else:
        return 'Las contraseñas no coinciden'

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
def eliminar_persona(idcategoria):
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


@app.route('/admin')
def admin():
    consulta = 'SELECT * FROM categorias'
    con = db.connect()
    cur = con.cursor()
    cur.execute(consulta)
    categorias = cur.fetchall() #Envia todos los datos de la consulta y los guarda en la variable persona
    con.commit()
    return render_template('admin.html', categorias = categorias) #Le mandamos el array a la vista para poder usar los datos
    


@app.route('/guardar', methods=['POST']) #Ruta para hacer una insercion o POST
def guardar_persona():
    nombre = request.form['nombre'] #Recibiendo los datos del formulario, es importante poner el mismo nombre del input
    apaterno = request.form['apaterno']
    amaterno = request.form['amaterno']
    image = request.files['image'] #Tomamos el archivo
    nombre_foto= image.filename #Obtenemos el nombre del archivo
    image.save('static/img/' + nombre_foto) #Guardar la imagen en local
    consulta = 'INSERT INTO personas (pk_persona, nombre, apaterno, amaterno, image) VALUES(NULL, %s, %s, %s, %s)' 
    con = db.connect() #Abre una conexion con MySQL
    cur = con.cursor()
    cur.execute(consulta,(nombre, apaterno, amaterno, nombre_foto)) #Le enviamos parametros a la consulta
    con.commit() #Guarda los cambios en la base de datos
    return redirect('/personas')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=80,debug=True)