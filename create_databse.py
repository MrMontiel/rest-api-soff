from app.infrastructure.database import engine, Base
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.providers.adapters.sqlachemy.provider import Provider
from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.users.adapters.sqlalchemy.user import User, Role, Permission,PermissionsRoles

Base.metadata.create_all(engine)