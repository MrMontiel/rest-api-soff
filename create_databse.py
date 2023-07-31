from app.infrastructure.database import engine, Base
from app.products.adapters.sqlalchemy.product import Product, Association
from app.providers.adapters.sqlachemy.provider import Provider
from app.purchases.adapters.sqlalchemy.purchase import Purchase, Association as AssociationPurchase
from app.sales.adapters.sqlalchemy.sale import Sale, Association as AssociationSale, Client
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.users.adapters.sqlalchemy.user import User, Role, Permission, Association as AssociationUser

Base.metadata.create_all(engine)