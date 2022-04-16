CREATE TABLE IF NOT EXISTS usuarios (
    pk_usuario SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    password VARCHAR(25) NOT NULL,
    email_usuario VARCHAR(150) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    tipo_usuario VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    pk_categoria SMALLINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombreCategoria VARCHAR(300) NOT NULL,
    descripcionCategoria TEXT NOT NULL,
    imagenCaratula VARCHAR(350) NOT NULL,
    imagen1 VARCHAR(350) NOT NULL,
    imagen2 VARCHAR(350) NOT NULL,
    imagen3 VARCHAR(350) NOT NULL,
    imagen4 VARCHAR(350) NOT NULL,
    imagen5 VARCHAR(350) NOT NULL
);
CREATE TABLE IF NOT EXISTS productos(
    pk_producto SMALLINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre_producto VARCHAR(150) NOT NULL,
    descripcion_producto TEXT NOT NULL,
    precio_producto FLOAT(6,2),
    estatus VARCHAR(25),
    imagen1 VARCHAR(300),
    imagen2 VARCHAR(300),
    imagen3 VARCHAR(300),
    imagen4 VARCHAR(300),
    imagen5 VARCHAR(300),
    imagen6 VARCHAR(300),
    imagen7 VARCHAR(300),
    imagen8 VARCHAR(300),
    imagen9 VARCHAR(300),
    imagen10 VARCHAR(300),
    fk_categoria SMALLINT NOT NULL,
    FOREIGN KEY (fk_categoria) REFERENCES categorias(pk_categoria)
);