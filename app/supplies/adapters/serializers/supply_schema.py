from app.supplies.adapters.sqlalchemy.supply import Supply

def SupplySchema(supply: Supply) -> dict:
    return{
        "id": supply.id,
        "name": supply.name,
        "price": supply.price,
        "quantity_stock": supply.quantity_stock,
        "unit_measure": supply.unit_measure,
        "status": supply.status
    }
    
def suppliesSchema(supplies: list [Supply]) -> list:
    return [SupplySchema(supply)for supply in supplies]
