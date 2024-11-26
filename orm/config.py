#El engine permite configurar la conexion a la BD
from sqlalchemy import create_engine
#El session maker permite crear sesiones para hacer consultas
#Por cada consulta se abre y cierra una sesion
from sqlalchemy.orm import sessionmaker, declarative_base

#1. Configurar la conexion BD
# servidor://usuario:password@url:puerto/nombreBD
URL_BASE_DATOS = "postgresql://usuario-ejemplo:12345@localhost:5432/base-ejemplo"
# Conectamos mediante el esquema app
engine = create_engine(URL_BASE_DATOS,
                       connect_args={
                            "options": "-csearch_path=app"    
                       })

# 2. Obtener la clase que nos permite crear objetos de tipo sesion
SessionClass = sessionmaker(engine)
# Crear una funcion para obtener objetos de la clase SessionClass
def generador_sesion():
    sesion = SessionClass()
    try:
        # Equivalente a return sesion pero de manera segura
        yield sesion
    finally:
        sesion.close()
        
# 3.Obtener la clase base para mapear tablas
BaseClass = declarative_base()