from sqlalchemy import select
from app.infrastructure.database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from app.purchases.adapters.services.services import (
  CreatePurchase, 
  GetAllPurchases, 
  AddOrder, 
  ConfirmPurchase, 
  seePurchasesOrders,
  GetPurchaseById
  )

from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.purchases.adapters.serializers.purchase_schema import purchaseSchema, purchasesSchema, orderSchema, ordersSchema

from app.purchases.domain.pydantic.purchase import PurchaseCreate, OrderPurchaseCreate

from app.supplies.adapters.sqlalchemy.supply import Supply
from app.supplies.adapters.serializers.supply_schema import SupplySchema, suppliesSchema


session = SessionLocal()

purchases = APIRouter(
  prefix='/purchases',
  tags=["Purchases"]
)

@purchases.get('/supplies')
async def get_all_supplies():
  supplies = session.scalars(select(Supply)).all()
  return suppliesSchema(supplies)


@purchases.get('/')
async def get_all_purchases(limit: int = 100):
  purchases = GetAllPurchases()
  return {
    "amount_purchases": len(purchases),
    "purchases": purchasesSchema(purchases)
  }

@purchases.get('/{id_purchase}')
async def get_purchase_by_id(id_purchase: str):
  purchase = GetPurchaseById(id_purchase)
  return purchaseSchema(purchase)

@purchases.post('/')
async def create_purchase():
  new_purchase = CreatePurchase()
  return {
    "id": new_purchase.id,
    "message": "purchase created successfully"
  }

@purchases.post('/{id_purchase}/add-order')
async def add_order(id_purchase: str, order: OrderPurchaseCreate):
  new_order = AddOrder(id_purchase, order)
  return {
    "purchase_id": new_order.purchase_id,
    "supply_id": new_order.supply_id,
    "message": "order add successfully"
  }

@purchases.put('/{id_purchase}/confirm-purchase')
async def confirm_purchase(id_purchase: str, provider_id: str):
  purchase = ConfirmPurchase(id_purchase, provider_id)
  return {
    "id_purchase": purchase.id,
    "purchase": purchaseSchema(purchase)
  }
  
@purchases.get('/{id_purchase}/orders')
async def getAllOrdersByPurchaseId(id_purchase: str):
  orders = seePurchasesOrders(id_purchase)
  return {
    "id_purchase": id_purchase,
    "orders": ordersSchema(orders)
  }