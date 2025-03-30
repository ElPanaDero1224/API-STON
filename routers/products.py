from models.pydantic import products, statistics
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.db import Products, Statistics
from db.connection import Session
from typing import List

productsRouter = APIRouter()

# endpoint para obtener el inventario
@productsRouter.get("/inventory/", response_model=List[products], tags=["Inventario"])
def get_inventory():
    db=Session()
    try:
        inventario = db.query(Products).all()
        return JSONResponse(content=jsonable_encoder(inventario))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener el inventario", "exception": str(e)})
    finally:
        db.close()

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
        db.close()