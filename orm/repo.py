import orm.modelos as modelos
import orm.esquemas as esquemas
from sqlalchemy.orm import Session
from sqlalchemy import and_

# ------------ Peticiones a usuarios ---------------------
# Esta función es llamada por api.py
# para atender GET '/usuarios/{id}'
# select * from app.usuarios where id = id_usuario
def usuario_por_id(sesion:Session,id_usuario:int):
    print("select * from app.usuarios where id = ", id_usuario)
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first()

# Buscar fotos por id de usuario
# GET '/usuarios/{id}/fotos'
# select * from app.fotos where id_usuario=id
def fotos_por_id_usuario(sesion:Session,id_usuario:int):
    print("select * from app.fotos where id_usuario=", id_usuario)
    return sesion.query(modelos.Foto).filter(modelos.Foto.id_usuario==id_usuario).all() 

# select * from app.compras where id_usuario=id
def compras_por_id_usuario(sesion:Session,id_usuario:int):
    print("select * from app.compras where id_usuario=", id_usuario)
    return sesion.query(modelos.Compra).filter(modelos.Compra.id_usuario==id_usuario).all() 

# Borra fotos por id de usuario
# DELETE '/usuarios/{id}/fotos'
# delete from app.fotos where id_usuario=id
def borrar_fotos_por_id_usuario(sesion:Session,id_usuario:int):
    print("delete from app.fotos where id_usuario=",id_usuario)
    fotos_usr = fotos_por_id_usuario(sesion, id_usuario)
    if fotos_usr is not None:
        for foto_usuario in fotos_usr:
            sesion.delete(foto_usuario)
        sesion.commit()

# Borra compras por id de usuario
# DELETE '/usuarios/{id}/compras'
# delete from app.compras where id_usuario=id
def borrar_compras_por_id_usuario(sesion:Session,id_usuario:int):
    print("delete from app.compras where id_usuario=",id_usuario)
    compras_usr = compras_por_id_usuario(sesion, id_usuario)
    if compras_usr is not None:
        for compra_usuario in compras_usr:
            sesion.delete(compra_usuario)
        sesion.commit()

# GET '/usuarios'
# select * from app.usuarios
def devuelve_usuarios(sesion:Session):
    print("select * from app.usuarios")
    return sesion.query(modelos.Usuario).all()

#PUT '/usuarios/{id}'
def actualiza_usuario(sesion:Session,id_usuario:int,usr_esquema:esquemas.UsuarioBase):
    #1.-Verificar que el usuario existe
    usr_bd = usuario_por_id(sesion,id_usuario)
    if usr_bd is not None:
        #2.- Actualizamos los datos del usuaurio en la BD
        usr_bd.nombre = usr_esquema.nombre
        usr_bd.edad = usr_esquema.edad
        usr_bd.domicilio = usr_esquema.domicilio
        usr_bd.email = usr_esquema.email
        usr_bd.password = usr_esquema.password
        #3.-Confirmamos los cambios
        sesion.commit()
        #4.-Refrescar la BD
        sesion.refresh(usr_bd)
        #5.-Imprimir los datos nuevos
        print(usr_esquema)
        return usr_esquema
    else:
        respuesta = {"mensaje":"No existe el usuario"}
        return respuesta
    
# POST '/usuarios/'
def guardar_usuario(sesion:Session, usr_nuevo:esquemas.UsuarioBase):
    #1.Crear un nuevo objeto de la clase modelo Usuario
    usr_bd = modelos.Usuario()
    #2.Llenamos el nuevo objeto con los parametros que nos paso el usuario
    usr_bd.nombre = usr_nuevo.nombre
    usr_bd.edad = usr_nuevo.edad
    usr_bd.domicilio = usr_nuevo.domicilio
    usr_bd.email = usr_nuevo.email
    usr_bd.password = usr_nuevo.password
    #3.Insertar el nuevo objeto a la BD
    sesion.add(usr_bd)
    #4.Confirmamos el cambio
    sesion.commit()
    #5.Hacemos un refresh
    sesion.refresh(usr_bd)
    return usr_bd
        
# DELETE '/usuarios/{id}'
# delete from app.usuarios where id=id_usuario
def borra_usuario_por_id(sesion:Session,id_usuario:int):
    print("delete from app.usuarios where id=", id_usuario)
    #1.- borro compras del usuario
    borrar_compras_por_id_usuario(sesion, id_usuario)
    #2.-borro foto del usuario
    borrar_fotos_por_id_usuario(sesion, id_usuario)
    #3.- select para ver si existe el usuario a borrar
    usr = usuario_por_id(sesion, id_usuario)
    #4.- Borramos
    if usr is not None:
        #Borramos usuario
        sesion.delete(usr)
        #Confirmar los cambios
        sesion.commit()
    respuesta = {
        "mensaje": "usuario eliminado"
    }
    return respuesta

# ------------ Peticiones a fotos ---------------------
# GET '/fotos/{id}'
# select * from app.fotos where id = id_foto
def foto_por_id(sesion:Session,id_foto:int):
    print("select * from fotos where id = id_foto")
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first()

# GET '/fotos'
# select * from app.fotos
def devuelve_fotos(sesion:Session):
    print("select * from app.fotos")
    return sesion.query(modelos.Foto).all()

# PUT '/fotos/{id}'
def actualiza_foto(sesion:Session, id_foto:int, foto_esquema:esquemas.FotoBase):
    foto_bd = foto_por_id(sesion, id_foto)
    if foto_bd is not None:
        foto_bd.titulo = foto_esquema.titulo
        foto_bd.descripcion = foto_esquema.descripcion
        foto_bd.ruta = foto_esquema.ruta
        
        sesion.commit()
        sesion.refresh(foto_bd)
        print(foto_esquema)
        return(foto_esquema)
    else:
        respuesta = {"mensaje":"No existe la foto"}
        return respuesta

# ------------ Peticiones a compras ---------------------
# GET '/compras/{id}'
# select * from app.compras where id = id_compra
def compra_por_id(sesion:Session,id_compra:int):
    print("select * from compras where id = id_compra")
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first()

# GET '/compras'
# select * from app.compras
def devuelve_compras(sesion:Session):
    print("select * from app.compras")
    return sesion.query(modelos.Compra).all()

# GET '/compras?id_usuario={id_usr}&precio={p}'
# select * from app.compras where id_usuario=id_usr and precio>=p
def devuelve_compras_por_usuario_precio(sesion:Session, id_usr:int, p:float):
    print("select * from app.compras where id_usuario=id_usr and precio>=p")
    return sesion.query(modelos.Compra).filter(and_(modelos.Compra.id_usuario==id_usr, modelos.Compra.precio>=p)).all()

#PUT '/compras/{id}'
def actualiza_compras(sesion:Session, id_comp:int, comp_esquema:esquemas.CompraBase):
    compra_bd = compra_por_id(sesion, id_comp)
    if compra_bd is not None:
        compra_bd.producto = comp_esquema.producto
        compra_bd.precio = comp_esquema.precio
        
        sesion.commit()
        sesion.refresh(compra_bd)
        print(comp_esquema)
        return(comp_esquema)
    else:
        respuesta = {"mensaje":"No existe la compra"}
        return respuesta
    
# POST '/usuario/{id}/compras'
def guardar_compra_usuario(sesion:Session, id_usr:int, compra_nueva:esquemas.CompraBase):
    usr = usuario_por_id(sesion, id_usr)
    if usr is not None:
        #1.Crear un nuevo objeto de la clase modelo Compra
        compra_bd = modelos.Compra()
        #2.Llenamos el nuevo objeto con los parametros que nos paso el usuario
        compra_bd.id_usuario = id_usr
        compra_bd.producto = compra_nueva.producto
        compra_bd.precio = compra_nueva.precio
        #3.Insertar el nuevo objeto a la BD
        sesion.add(compra_bd)
        #4.Confirmamos el cambio
        sesion.commit()
        #5.Hacemos un refresh
        sesion.refresh(compra_bd)
        return compra_bd
    else:
        respuesta = {"mensaje":"El usuario no existe"}
        return respuesta