from models.pydantic import statistics
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.db import Productos, Inventario
""" Statistics """
from db.connection import Session
from typing import List
from sqlalchemy import or_

productsRouter = APIRouter()

# endpoint para obtener productos de acuerdo a busquedas
@productsRouter.get("/inventory/", tags=["Inventario"])
def get_inventory(search: str = Query(None, description="Término para buscar en nombre o material")):
    db = Session()
    try:
        # Construimos la consulta base seleccionando solo los campos necesarios
        query = db.query(
            Productos.nombre,
            Productos.precioUnitario,
            Productos.material
        )
        
        # Aplicamos filtro si hay término de búsqueda
        if search:
            query = query.filter(
                or_(
                    Productos.nombre.ilike(f"%{search}%"),
                    Productos.material.ilike(f"%{search}%")
                )
            )
        
        # Ejecutamos la consulta
        resultados = query.all()
        
        # Formateamos la respuesta
        productos = [{
            "nombre": item.nombre,
            "precio": float(item.precioUnitario),  # Convertimos a float para JSON
            "material": item.material
        } for item in resultados]
        
        return JSONResponse(content=productos)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Error al obtener productos", "error": str(e)}
        )
    finally:
        db.close()



@productsRouter.get("/searchProducts/", tags=["Inventario"])
def search_products(
    nombre: str = Query(None, description="Nombre o parte del nombre del producto a buscar"),
    material: str = Query(None, description="Material o parte del material del producto a buscar")
):
    db = Session()
    try:
        # Consulta con JOIN a inventarios
        query = db.query(Productos, Inventario)\
            .join(Inventario, Productos.id_inventario == Inventario.id)
        
        # Aplicamos filtros
        if nombre:
            query = query.filter(Productos.nombre.ilike(f"%{nombre}%"))
        if material:
            query = query.filter(Productos.material.ilike(f"%{material}%"))
        
        resultados = query.all()

        if not resultados:
            return JSONResponse(
                status_code=404,
                content={"message": "No se encontraron productos con los criterios de búsqueda"}
            )

        # Construimos la respuesta con todo en un solo objeto por producto
        response_data = []
        for producto, inventario in resultados:
            item = {
                "nombre": producto.nombre,
                "precioUnitario": float(producto.precioUnitario),
                "cantidad": producto.cantidad,
                "material": producto.material,
                "codigoLote": producto.codigoLote,
                # Campos del inventario integrados directamente
                "inventario_nombre": inventario.nombre,
                # Agrega aquí cualquier otro campo del inventario que necesites
                # ...
                # Mantienes los demás campos del producto
                "dimensiones": producto.dimensiones,
                "precauciones": producto.precauciones,
                "caracteristicas": producto.caracteristicas
            }
            response_data.append(item)

        return JSONResponse(content=jsonable_encoder(response_data))

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Error al buscar productos", "error": str(e)}
        )
    finally:
        db.close()
""" 
# endpoint para obtener los detalles de un producto
@productsRouter.get("/productDetails/{productID}", response_model=products, tags=["Inventario"])
def get_details(productID: int):
    db=Session()
    try:
        producto = db.query(Products).filter(Products.id == productID).first()
        if producto:
            return JSONResponse(content=jsonable_encoder(producto))
        else:
            return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener los detalles del producto", "exception": str(e)})
    finally:
        db.close()

# endpoint para agregar un producto
@productsRouter.post("/addProduct/", tags=["Inventario"])
def add_product(producto: products, existent: bool = False):
    db=Session()
    try:
        if existent:
            db.query(Products).filter(Products.id == producto.id).update(producto.model_dump())
        else:
            db.add(Products(**producto.model_dump()))
        db.commit()
        return JSONResponse(content={"message": "Producto agregado con éxito", "product": jsonable_encoder(producto)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al agregar el producto", "exception": str(e)})
    finally:
        db.close()

# endpoint para modificar el producto
@productsRouter.put("/modProduct/{productID}", tags=["Inventario"])
def modify_product(productID: int, producto: products):
    db=Session()
    try:
        db.query(Products).filter(Products.id == productID).update(producto.model_dump())
        db.commit()
        return JSONResponse(content={"message": "Producto modificado con éxito", "product": jsonable_encoder(producto)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al modificar el producto", "exception": str(e)})
    finally:
        db.close()

# endpoint para eliminar un producto
@productsRouter.delete("/delProduct/{productID}", tags=["Inventario"])
def delete_product(productID: int):
    db=Session()
    try:
        db.query(Products).filter(Products.id == productID).delete()
        db.commit()
        return JSONResponse(content={"message": "Producto eliminado con éxito"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar el producto", "exception": str(e)})
    finally:
        db.close()

# endpoint para obtener estadísticas de un producto
@productsRouter.get("/statistics/{productID}", response_model=statistics, tags=["Estadisticas"])
def statistics(productID: int):
    db=Session()
    try:
        estadisticas = db.query(Statistics).filter(Statistics.producto == productID).first()
        if estadisticas:
            return JSONResponse(content=jsonable_encoder(estadisticas))
        else:
            return JSONResponse(status_code=404, content={"message": "Estadísticas no encontradas"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener las estadísticas del producto", "exception": str(e)})
    finally:
        db.close()  """