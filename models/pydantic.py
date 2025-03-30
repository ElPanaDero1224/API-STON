from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

#modelos de la API

#modelos para agregar un nuevo usuario
class user(BaseModel):
    name: str = Field(..., min_length=1, max_length=85, description="Nombre, mínimo 1 caracter, máximo 85")
    lastname: str = Field(..., min_length=1, max_length=85, description="Apellido, mínimo 1 caracter, máximo 85")
    username: str = Field(..., min_length=1, max_length=50, description="Nombre de usuario, mínimo 1 caracter, máximo 50")
    password: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña de al menos 8 caracteres")
    
class EmpresaModel(BaseModel):
    numeroRegistro: str = Field(..., min_length=1, max_length=14)
    nombre: str = Field(..., min_length=1, max_length=255)
    tipo: str = Field(..., min_length=1, max_length=255)
    correo: EmailStr
    contrasenia: str = Field(..., min_length=8)
    numTelefono: str = Field(..., min_length=1, max_length=20)
    pais: str = Field(..., min_length=1, max_length=50)
    region: str = Field(..., min_length=1, max_length=50)
    direccion: str = Field(..., min_length=1, max_length=300)
    
    class Config:
        from_attributes = True
#modelo para validar credenciales
class credentials(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Nombre de usuario, mínimo 1 caracter, máximo 50")
    password: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña de al menos 8 caracteres")

# modelo para productos
class products(BaseModel):
    id: int = Field(..., gt=0, description="ID del producto, debe ser un número positivo")
    producto: str = Field(..., min_length=1, max_length=100, description="Nombre del producto, mínimo 1 caracter, máximo 100")
    codigo: int = Field(..., gt=0, description="Código de barras, debe ser un número positivo")
    expiración: Optional[List[str]] = Field(None, description="Fechas de vencimiento (opcional)")
    cantidad: int = Field(..., ge=0, description="Cantidad del producto, debe ser un número positivo o cero")

#modelo para estadísticas de un producto
class statistics(BaseModel):
    producto: str = Field(..., min_length=1, max_length=100, description="Nombre del producto, mínimo 1 caracter, máximo 100")
    codigo: int = Field(..., gt=0, description="Código de barras, debe ser un número positivo")
    expiración: Optional[List[str]] = Field(None, description="Fechas de vencimiento (opcional)")
    entrada: List[str] = Field(..., description="Fechas de entrada del producto")
    salida: List[str] = Field(..., description="Fechas de salida del producto")