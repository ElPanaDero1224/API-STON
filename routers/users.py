from models.pydantic import  EmpresaModel, credentials
""" user"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.db import Empresa, Users 
from db.connection import Session
from passlib.context import CryptContext



usersRouter = APIRouter()

# Endpoint para agregar un nuevo usuario

""" @usersRouter.post("/addUser/", tags=["Usuarios"])
def add_user(user: user):
    db=Session()
    try:
        db.add(Users(**user.model_dump()))
        db.commit()
        return JSONResponse(content={"message": "Usuario agregado con exito", "user": jsonable_encoder(user)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al agregar el usuario", "exception": str(e)})
    finally:
        db.close()
 """

#enpoint para agregarlo a la empresa

@usersRouter.post("/addEmpresa/", tags=["Empresas"])
def add_empresa(empresa: EmpresaModel):
    db = Session()
    try:
        db_empresa = Empresa(
            numeroRegistro=empresa.numeroRegistro,
            nombre=empresa.nombre,
            tipo=empresa.tipo,
            correo=empresa.correo,
            contrasenia=empresa.contrasenia,  # Contraseña en texto plano
            numTelefono=empresa.numTelefono,
            pais=empresa.pais,
            region=empresa.region,
            direccion=empresa.direccion
        )
        
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Empresa registrada con éxito",
                "data": jsonable_encoder(db_empresa)
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "message": "Error al registrar la empresa",
                "error": str(e)
            }
        )
    finally:
        db.close()



@usersRouter.post("/validateEmpresa/", tags=["Autenticación"])
def validate_empresa(credenciales: credentials):  # Ahora usa el nuevo modelo
    db = Session()
    try:
        empresa = db.query(Empresa).filter(
            Empresa.correo == credenciales.correo,  # Usa el campo correo
            Empresa.contrasenia == credenciales.contrasenia  # Usa contrasenia
        ).first()
        
        if empresa:
            return JSONResponse(
                status_code=200,
                content={"message": "Autenticación exitosa"}
            )
        return JSONResponse(
            status_code=401,
            content={"message": "Correo o contraseña incorrectos"}
        )
    finally:
        db.close()

""" 
# Endpoint para validar credenciales
@usersRouter.post("/credentialValidator/", tags=["Autenticación"])
def validate(credentials: credentials):
    db=Session()
    try:
        user = db.query(Users).filter(Users.username == credentials.username, Users.password == credentials.password).first()
        if user:
            return JSONResponse(content={"message": "Credenciales validas"})
        else:
            return JSONResponse(status_code=503, content={"message": "Usuario o contraseña incorrecta"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al validar las credenciales", "exception": str(e)})
    finally:
        db.close()

# endpoint para eliminar un usuario
@usersRouter.delete("/delUser/{username}", tags=["Usuarios"])
def delete_user(username: str):
    db=Session()
    try:
        user = db.query(Users).filter(Users.username == username).first()
        if user:
            db.delete(user)
            db.commit()
            return JSONResponse(content={"message": "Usuario eliminado correctamente"})
        else:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar el usuario", "exception": str(e)})
    finally:
        db.close() """