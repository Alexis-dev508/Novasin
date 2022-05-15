from utils.db import db


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


    def __init__ (self, titulo1,titulo2,titulo3,titulo4,titulo5, imagen1,imagen2, imagen3, imagen4, imagen5):
        self.titulo1 = titulo1
        self.titulo2 = titulo2
        self.titulo3 = titulo3
        self.titulo4 = titulo4
        self.titulo5 = titulo5
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.imagen3 = imagen3
        self.imagen4 = imagen4
        self.imagen5 = imagen5

        