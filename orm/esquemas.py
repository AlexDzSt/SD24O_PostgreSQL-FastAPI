from pydantic import BaseModel

#Definir el esquema usuario
class UsuarioBase(BaseModel):
    nombre:str
    edad:int
    domicilio:str
    email:str
    password:str
    
class CompraBase(BaseModel):
    producto: str
    precio: float
    
class FotoBase(BaseModel):
    titulo: str
    descripcion: str
    ruta: str