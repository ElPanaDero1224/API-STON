from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends

#modelos de la API

#modelos para agregar un nuevo usuario
class usuario(BaseModel):
    usuario: str = Field(..., min_length=1, max_length=50, description="Nombre de usuario, mínimo 1 caracter, máximo 50")
    name: str = Field(..., min_length=1, max_length=85, description="Nombre, mínimo 1 caracter, máximo 85")
    lastname: str = Field(..., min_length=1, max_length=85, description="Apellido, mínimo 1 caracter, máximo 85")
    password: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña de al menos 8 caracteres")

#modelo para validar credenciales
class credenciales(BaseModel):
    usuario: str = Field(..., min_length=1, max_length=50, description="Nombre de usuario, mínimo 1 caracter, máximo 50")
    contraseña: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña de al menos 8 caracteres")

# modelo para productos
class productos(BaseModel):
    id: int = Field(..., gt=0, description="ID del producto, debe ser un número positivo")
    producto: str = Field(..., min_length=1, max_length=100, description="Nombre del producto, mínimo 1 caracter, máximo 100")
    codigo: int = Field(..., gt=0, description="Código de barras, debe ser un número positivo")
    expiración: Optional[List[str]] = Field(None, description="Fechas de vencimiento (opcional)")
    cantidad: int = Field(..., ge=0, description="Cantidad del producto, debe ser un número positivo o cero")

#modelo para estadísticas de un producto
class estadísticas(BaseModel):
    producto: str = Field(..., min_length=1, max_length=100, description="Nombre del producto, mínimo 1 caracter, máximo 100")
    codigo: int = Field(..., gt=0, description="Código de barras, debe ser un número positivo")
    expiración: Optional[List[str]] = Field(None, description="Fechas de vencimiento (opcional)")
    entrada: List[str] = Field(..., description="Fechas de entrada del producto")
    salida: List[str] = Field(..., description="Fechas de salida del producto")

# ISe inicia la api
app = FastAPI(
    title="stockon API",
    description="API para la gestión de usuarios y productos en stockon",
    version="1.0.0"
)

# bd en memoria
usuariosbd = []
inventariobd = []

# endpoint para agregar un nuevo usuario
@app.post("/agregarUsuario/", tags=["Usuarios"])
def agregarus(user: usuario):
    for u in usuariosbd:
        if u.usuario == user.usuario:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
    usuariosbd.append(user)
    return {"message": "Usuario agregado correctamente"}

# endpoint para validar credenciales
@app.post("/validarcredencial/", tags=["Autenticación"])
def validar(credentials: credenciales):
    for u in usuariosbd:
        if u.usuario == credentials.usuario and u.password == credentials.contraseña:
            return {"message": "credenciales válidas"}
    raise HTTPException(status_code=401, detail="credenciales inválidas")

# endpoint para eliminar un usuario
@app.delete("/eliminarusuario/{usuario}", tags=["Usuarios"])
def eliminarus(usuario: str):
    for i, u in enumerate(usuariosbd):
        if u.usuario == usuario:
            del usuariosbd[i]
            return {"message": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# endpoint para obtener el inventario
@app.get("/inventario/", response_model=List[productos], tags=["Inventario"])
def obtenerinventario():
    return inventariobd

# endpoint para obtener los detalles de un producto
@app.get("/detallesProducto/{idproducto}", response_model=productos, tags=["Inventario"])
def obtenerdetalles(idproducto: int):
    for producto in inventariobd:
        if producto.id == idproducto:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# endpoint para agregar un producto
@app.post("/agregarProducto/", tags=["Inventario"])
def añadirprod(producto: productos, existent: bool = False):
    if existent:
        for p in inventariobd:
            if p.codigo == producto.codigo:
                p.cantidad += producto.cantidad
                return {"message": "Cantidad del producto actualizada"}
    inventariobd.append(producto)
    return {"message": "Producto agregado correctamente"}

# endpoint para eliminar un producto
@app.delete("/eliminarProducto/{idproducto}", tags=["Inventario"])
def eliminarprod(idproducto: int):
    for i, producto in enumerate(inventariobd):
        if producto.id == idproducto:
            del inventariobd[i]
            return {"message": "Producto eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# endpoint para obtener estadísticas de un producto
@app.get("/Estadísticas/{idproducto}", response_model=estadísticas, tags=["Estadisticas"])
def estadisticas(idproducto: int):
    for producto in inventariobd:
        if producto.id == idproducto:
            return estadísticas(
                producto=producto.producto,
                codigo=producto.codigo,
                expiración=producto.expiración,
                entrada=["2025-03-05", "2025-03-15"],  # ejemplo de entradas
                salida=["2025-03-21"]  # ejemplo de salidas
            )
    raise HTTPException(status_code=404, detail="Producto no encontrado")