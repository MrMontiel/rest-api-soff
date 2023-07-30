import uuid
from sqlalchemy import select
from fastapi import status, HTTPException
from app.config.database import SessionLocal
from app.sales.pydantic_models.sale_pydantic import SaleCreate
from app.sales.sqlalchemy_models.sale_sqlalchemy import Sale, Client

session = SessionLocal()

def CreateSale(sale: SaleCreate):
  if not sale:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sale not created")
  if sale.type_sale == "" or sale.payment_method == "" or sale.id_client == "":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the type of sale, the payment_method and client are required")
  
  client = session.scalars(select(Client)).one()
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
  else:
    print(sale.id_client)
    new_sale = Sale(pyment_method=sale.payment_method, type_sale=sale.type_sale, id_client=uuid.UUID(sale.id_client))
    session.add(new_sale)
    session.commit()
    session.refresh(new_sale)
  return new_sale