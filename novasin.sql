CREATE DATABASE novasin;

CREATE TABLE IF NOT EXISTS tipos_usuarios(
    pk_tipo_usuario SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    tipo_usuario VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS categorias(
    pk_categoria SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_categoria VARCHAR(150),
    descripcion_categoria TEXT,
    imagen_caratula TEXT,
    imagen_carusel_1 TEXT,
    imagen_carusel_2 TEXT,
    imagen_carusel_3 TEXT,
    imagen_carusel_4 TEXT,
    imagen_carusel_5 TEXT
);
CREATE TABLE usuarios (
    pk_usuario, nombre, email_usuario, telefono, ciudad, fk_tipo_usuario
    pk_usuario SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(250) NOT NULL,
    email_usuario VARCHAR(150),
    telefono VARCHAR(10),
    ciudad VARCHAR(10),
    tipo_usuario VARCHAR(10),
    
);

CREATE TABLE IF NOT EXISTS productos(
    fk_producto SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombre_producto VARCHAR(150),
    descripcion_producto TEXT,
    precio_unidad FLOAT(6,3),
    imagen_1 TEXT,
    imagen_2 TEXT,
    imagen_3 TEXT,
    imagen_4 TEXT,
    imagen_5 TEXT,
    fk_categoria SMALLINT,
    FOREIGN KEY (fk_categoria) REFERENCES categorias(pk_categoria)
);