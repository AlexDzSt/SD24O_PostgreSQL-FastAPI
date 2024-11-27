import orm.modelos as modelos
from sqlalchemy.orm import Session
from sqlalchemy import and_

# Esta funcion es llamada por api.py para atender GET '/usuarios/(id)'
# select * from app.usuarios where id = id_usuario

#### USUARIOS ####
def usuario(sesion: Session):
    print("select * from app.usuarios")
    return sesion.query(modelos.Usuario).all()

def usuario_por_id(sesion: Session, id_usuario: int):
    print("select * from app.usuarios where id =",  id_usuario)
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first()

def usuario_por_rango_edad(sesion: Session, edadMin: int, edadMax: int):
    print("select * from usuarios where edad > ", edadMin, "y edad < ", edadMax)
    return sesion.query(modelos.Usuario).filter(and_(modelos.Usuario.edad>edadMin, modelos.Usuario.edad<edadMax)).all()

#### COMPRAS ####
def compra(sesion: Session):
    print("select * from app.compras")
    return sesion.query(modelos.Compra).all()

def compra_por_id(sesion: Session, id_compra: int):
    print("select * from app.compras where id = ", id_compra)
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first()

def devuelve_compras_por_usuario_precio(sesion: Session, id_usr: int, p: float):
    print("select * from app.compras where id_usuario = ", id_usr, "y precio =", p)
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario==id_usr, modelos.Compra.precio>=p)).all()

#### FOTOS ####
def foto(sesion: Session):
    print("select * from app.fotos")
    return sesion.query(modelos.Foto).all()

def foto_por_id(sesion: Session, id_foto: int):
    print("select * from app.fotos where id = ", id_foto)
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first()



