from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders

def purchaseSchema(purchase: Purchase) -> dict:
    return{
        "id" : purchase.id,
        "purchase_date": purchase.purchase_date,
        "amount_order": purchase.amount_order,
        "provider_id": purchase.provider_id,
        "total": purchase.total,
        "status": purchase.status
    }
    
def purchasesSchema(purchases: list[Purchase]) -> list:
  return [purchaseSchema(purchase) for purchase in purchases]

def orderSchema(order: PurchasesOrders) -> dict:
    return{
        
        "id_order": order.id,
        "purchase_id": order.purchase_id,
        "supply_id": order.supply_id,
        "amount_supplies": order.amount_supplies,
        "price_supplies": order.price_supplies,
        "subtotal": order.subtotal
    }

def ordersSchema(orders: list[PurchasesOrders]) -> list:
  return [orderSchema(order) for order in orders]