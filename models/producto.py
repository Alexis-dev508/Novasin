from utils.db import db


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
    fk_categoria = db.Column(db.Integer, db.ForeignKey('categorias.pk_categoria'))
    categoria = db.relationship("Categoria")

    def __init__(self, nombre_producto, descripcion_producto, precio_producto, estatus, imagen1, imagen2,imagen3,imagen4,imagen5,imagen6,imagen7,imagen8,imagen9,imagen10, fk_categoria, categoria):
        self.nombre_producto = nombre_producto
        self.descripcion_producto = descripcion_producto
        self.precio_producto = precio_producto
        self.estatus = estatus
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.imagen3 = imagen3
        self.imagen4 = imagen4
        self.imagen5 = imagen5
        self.imagen6 = imagen6
        self.imagen7 = imagen7
        self.imagen8 = imagen8
        self.imagen9 = imagen9
        self.imagen10 = imagen10

        
