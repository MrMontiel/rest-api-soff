from app.Sales.sqlalchemy_models.sale import Sale, SalesOrders

def saleSchema(sale: Sale) -> dict:
  return {
    "id": sale.id,
    "sale_date": sale.sale_date,
    "amount_order": sale.amount_order,
    "payment_method": sale.pyment_method,
    "type_sale": sale.type_sale,
    "total": sale.total,
    "status": sale.status
  }
  
def salesSchema(sales: list[Sale]) -> list:
  return [saleSchema(sale) for sale in sales]

def orderSchema(order: SalesOrders) -> dict:
  return {
    "id": order.id,
    "sale_id": order.sale_id,
    "product_id": order.product_id,
    "amount_product": order.amount_product,
    "total": order.total
  }


def ordersSchema(orders: list[SalesOrders]) -> list:
  return [orderSchema(order) for order in orders]