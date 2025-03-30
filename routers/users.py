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


@usersRouter.delete("/deleteEmpresa", tags=["Empresas"])
def delete_empresa(credenciales: credentials):
    db = Session()
    try:
        # 1. Validación estricta de credenciales (case-sensitive)
        empresa = db.query(Empresa).filter(
            Empresa.correo == credenciales.correo,  # Comparación exacta de mayúsculas/minúsculas
            Empresa.contrasenia == credenciales.contrasenia  # Comparación exacta
        ).first()

        if not empresa:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Credenciales inválidas",
                    "hint": "Verifique mayúsculas/minúsculas y caracteres especiales"
                }
            )

        # 2. Eliminación de la empresa
        db.delete(empresa)
        db.commit()

        # 3. Verificación de eliminación
        empresa_eliminada = db.query(Empresa).filter(
            Empresa.correo == credenciales.correo
        ).first()

        if empresa_eliminada:
            db.rollback()
            return JSONResponse(
                status_code=500,
                content={"message": "No se pudo completar la eliminación"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "message": "Empresa eliminada correctamente",
                "empresa": {
                    "nombre": empresa.nombre,
                    "correo": empresa.correo,
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al eliminar la empresa",
                "error": str(e),
                "suggestion": "Contacte al administrador si el problema persiste"
            }
        )
    finally:
        db.close()
