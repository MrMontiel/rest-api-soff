from fastapi import HTTPException, status

def ProductNotFound(): 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PRODUCT_NOT_FOUND")

def IdProductRequired():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID_PRODUCT_REQUIRED")

def SupplyNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SUPPLY_NOT_FOUND")

def ProductNotUpdate():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CANNOT_UPDATE_INACTIVE_PRODUCT")

def DetailsRequired():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DETAILS_REQUIRED_FOR_CONFIRM_PRODUCT")

def InfoProductRequired():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NAME_AND_SALE_PRICE_REQUIRED")

def NameProductExist():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NAME_ALREADY_EXISTS")

def DetailsNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DETAILS_NOT_FOUND")