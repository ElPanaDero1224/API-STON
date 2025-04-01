from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.connection import get_db
from models.db import Venta, Producto

ventasRouter = APIRouter(prefix="/ventas", tags=["Ventas"])

@ventasRouter.get("/top-sold")
def TopVentas(
    fecha_inicio: str = Query(..., description="Fecha de inicio en formato YYYY-MM-DD"),
    fecha_fin: str = Query(..., description="Fecha de fin en formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    # Consulta para obtener los productos más vendidos en el rango de fechas
    results = (
        db.query(Venta.producto_id, Producto.name, func.sum(Venta.cantidad).label("venta_total"))
        .join(Producto, Venta.producto_id == Producto.id)
        .filter(Venta.fecha.between(fecha_inicio, fecha_fin))
        .group_by(Venta.producto_id, Producto.name)
        .order_by(func.sum(Venta.cantidad).desc())
        .all()
    )

    return [{"producto": r.name, "venta_total": r.venta_total} for r in results]

