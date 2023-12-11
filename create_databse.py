from app.infrastructure.database import engine, Base
from app.products.adapters.sqlalchemy.product import Product, RecipeDetail
from app.providers.adapters.sqlachemy.provider import Provider
from app.purchases.adapters.sqlalchemy.purchase import Purchase, PurchasesOrders
from app.sales.adapters.sqlalchemy.sale import Sale, SalesOrders, Client
from app.supplies.adapters.sqlalchemy.supply import Supply
from app.users.adapters.sqlalchemy.user import User
from app.roles.adapters.sqlalchemy.role import Role, PermissionsRoles
from app.permissions.adapters.slqalchemy.permission import Permission
from app.auth.adapters.sqlalchemy.models import RecoverPassword
from sqlalchemy.orm import Session
import uuid

session = Session(engine)
Base.metadata.create_all(engine)


# Se crea el proveedor y el cliente general
providergeneral = Provider(id=str(uuid.uuid4()), nit='00000000', name='general', company='general', address='general', date_registration='2023-11-15T14:57:54.817206', phone='0000000000', city='general', status=True )
clientgeneral = Client(id=str(uuid.uuid4()), name='general', direction='general', phone='00000000', email='general@general.com')

# Se crea los permisos
permissionsale = Permission(id='25162d25-38e8-422a-903c-db06130db632', name='ventas', status=True)
permissionpurchase = Permission(id='c79142b2-2b68-4976-b039-07449e269728', name='compras', status=True)
permissionproduct = Permission(id='ff7e2c46-f149-4cae-a812-ab90ad264f4a', name='productos', status=True)
permissionsupply = Permission(id='a67fc2fa-7adf-413d-8064-888d335bfc01', name='insumos', status=True)
permissionprovider = Permission(id='82b396e1-334a-48ed-8991-56f45385a7c3', name='proveedores', status=True)
permissionuser = Permission(id='0db47368-891d-4e22-9f12-aa5ae235694e', name='usuarios', status=True)
permissionrole = Permission(id='de24d27b-885f-47e9-adbc-2682779f6397', name='roles', status=True)
permissionconfig = Permission(id='3b8d4b94-68ff-4779-9c83-78ae2fbf7e8f', name='configuracion', status=True)

# Se crea el rol administrador y base
roleAdministrador = Role(id='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', name='Administrador', status=True)
roleBase = Role(id=str(uuid.uuid4()), name='Base', status=True)
try:
    session.add_all([providergeneral, clientgeneral, permissionsale, permissionpurchase, permissionproduct, permissionsupply,permissionprovider, permissionuser, permissionrole, permissionconfig, roleAdministrador, roleBase ])
    session.commit()
except Exception as e:
    print(f"Error al insertar registros: {e}")
    session.rollback()
finally:
    session.close()

# Se le dan los permisos a el rol administrador
associationone= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='25162d25-38e8-422a-903c-db06130db632')
associationtwo= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='c79142b2-2b68-4976-b039-07449e269728')
associationthree= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='ff7e2c46-f149-4cae-a812-ab90ad264f4a')
associationfour= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='a67fc2fa-7adf-413d-8064-888d335bfc01')
associationfive= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='82b396e1-334a-48ed-8991-56f45385a7c3')
associationsix= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='0db47368-891d-4e22-9f12-aa5ae235694e')
associationseven= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='de24d27b-885f-47e9-adbc-2682779f6397')
associationeight= PermissionsRoles(id=str(uuid.uuid4()), id_role='06bf9dfe-1244-44a6-9f93-3fb79e8f82dc', id_permission='3b8d4b94-68ff-4779-9c83-78ae2fbf7e8f')
try:
    session.add_all([ associationone, associationtwo, associationthree, associationfour,associationfive, associationsix, associationseven, associationeight  ])
    session.commit()
except Exception as a:
    print(f"Error al insertar registros: {a}")
    session.rollback()
finally:
    session.close()




#Se crea el usuario administrador
user = User(name="Xiomara", document_type="CC", document="1020431543", phone="3045705678", email="leidyxiomara19@hotmail.com", password="Leidy1234", status=True, id_role="06bf9dfe-1244-44a6-9f93-3fb79e8f82dc")
try:
    session.add(user)
    session.commit()
except Exception as e:
    print(f"Error al insertar registros {e}")
finally:
    session.close()
