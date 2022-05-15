
from utils.db import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    pk_usuario = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    nombre = db.Column(db.String(300), nullable=False) 
    password = db.Column(db.String(300), nullable=False)
    email_usuario = db.Column(db.String(300), nullable=False)
    telefono = db.Column(db.String(300), nullable=False) 
    ciudad = db.Column(db.String(300), nullable=False)
    tipo_usuario = db.Column(db.String(300), nullable=False) 


    def __init__(self, nombre, password, email_usuario, telefono, ciudad, tipo_usuario):
        self.nombre = nombre
        self.password = password
        self.email_usuario = email_usuario
        self.telefono = telefono
        self.ciudad = ciudad
        self.tipo_usuario = tipo_usuario