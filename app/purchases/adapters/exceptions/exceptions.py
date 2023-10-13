from fastapi import HTTPException, status

def ProviderNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PROVIDER_NOT_FOUND")

def PurchasesNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PURCHASES_NOT_FOUND")

def PurchaseNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PURCHASE_NOT_FOUND")

def SupplyNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SUPPLY_NOT_FOUND")

def PurchaseConfirm():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NOT_ADD_ORDERS_PURCHASE_CONFIRMED")

def OrderRequiredForConfirm():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ORDERS_REQUIRED_CONFIRM_PURCHASE")

def IdPurchaseRequired():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID_PURCHASE_IF_REQUIRED")

def OrderNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ORDER_NOT_FOUND")

def NotDeletePurchaseConfirm():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PURCHASE_IS_CONFIRMED")

def NotConfirmPurchase():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVOICE_NUMBER_IS_NULL")

def NotConfirmPurchaseInvoiceExist():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVOICE_NUMBER_EXIST")