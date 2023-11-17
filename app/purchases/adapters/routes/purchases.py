import uuid
from sqlalchemy import select
from app.infrastructure.database import ConectDatabase
from fastapi import APIRouter, HTTPException
from app.purchases.adapters.services.services import (
  CreatePurchase, 
  GetAllPurchases, 
  AddOrder, 
  ConfirmPurchase, 
  seePurchasesOrders,
  GetPurchaseById,
  UpdateAmountOrder,
  DeleteOrderById,
  DeletePurchaseByid
  )

from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.purchases.adapters.serializers.purchase_schema import purchaseSchema, purchasesSchema, orderSchema, ordersSchema

from app.purchases.domain.pydantic.purchase import PurchaseCreate, OrderPurchaseCreate, PurchasesConfirm
from fastapi import Depends
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.supplies.adapters.serializers.supply_schema import SupplySchema, suppliesSchema
from app.auth.adapters.services.user import User, getCurrentActivateUser
session = ConectDatabase.getInstance()

purchases = APIRouter(
  prefix='/purchases',
  tags=["Purchases"]
)

@purchases.get('/')
async def get_all_purchases(limit: int = 100, offset:int=0, user: User = Depends(getCurrentActivateUser)):
  purchases = GetAllPurchases(limit, offset)
  return purchasesSchema(purchases)
  

@purchases.get('/{id_purchase}')
async def get_purchase_by_id(id_purchase: str, user: User = Depends(getCurrentActivateUser)):
  purchase = GetPurchaseById(id_purchase)
  return purchaseSchema(purchase)

@purchases.post('/')
async def create_purchase( user: User = Depends(getCurrentActivateUser)):
  new_purchase = CreatePurchase()
  return {
    "id": new_purchase.id,
    "message": "purchase created successfully"
  }

@purchases.post('/{id_purchase}/add-order')
async def add_order(id_purchase: str, order: OrderPurchaseCreate, user: User = Depends(getCurrentActivateUser)):
  new_order = AddOrder(id_purchase, order)
  return {
    "purchase_id": new_order.purchase_id,
    "supply_id": new_order.supply_id,
    "message": "order add successfully"
  }

@purchases.put('/{id_purchase}/confirm-purchase')
async def confirm_purchase(id_purchase: str, purchaseConfirm:PurchasesConfirm, user: User = Depends(getCurrentActivateUser)):
  purchase = ConfirmPurchase(id_purchase, purchaseConfirm.purchase_date,purchaseConfirm.provider_id, purchaseConfirm.invoice_number)
  return {
    "id_purchase": purchase.id,
    "purchase": purchaseSchema(purchase)
  }
  
@purchases.get('/{id_purchase}/orders')
async def getAllOrdersByPurchaseId(id_purchase: str, user: User = Depends(getCurrentActivateUser)):
  orders = seePurchasesOrders(id_purchase)
  return  ordersSchema(orders)
  
  
@purchases.put('/update-amount-order')
async def UpdateAmountOrderByPurchaseId(id_order:str, amount_supplies: int, user: User = Depends(getCurrentActivateUser)):
  order = UpdateAmountOrder(id_order, amount_supplies)
  return orderSchema(order)


@purchases.delete('/{id_order}/delete')
async def DeleteOrderPurchase(id_order: str, user: User = Depends(getCurrentActivateUser)):
  DeleteOrderById(id_order)
  return {
    "message": "Order deleted successfully"
  }

@purchases.delete('/{id_purchase}/deletepurchase')
async def DeletePurchase(id_purchase: str, user: User = Depends(getCurrentActivateUser)):
  DeletePurchaseByid(id_purchase)
  return{
    "message": "Purchase deleted successfully"
  }