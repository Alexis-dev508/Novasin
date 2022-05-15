from utils.db import db


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
    productos = db.relationship('productos', lazy='dynamic')


    def __init__(self, nombreCategoria, descripcionCategoria,imagenCaratula,imagen1,imagen2,imagen3,imagen4,imagen5):
        self.nombreCategoria = nombreCategoria
        self.descripcionCategoria = descripcionCategoria
        self.imagenCaratula = imagenCaratula
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.imagen3 = imagen3
        self.imagen4 = imagen4
        self.imagen5 = imagen5
        # self.productos = productos