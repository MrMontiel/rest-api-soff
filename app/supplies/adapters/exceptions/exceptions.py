from fastapi import HTTPException, status

def notsupply():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SUPPLY_NOT_FOUND")

def requiredsupply():
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="SUPPLY_IS_REQUIRED")

def notcreatedsupply():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="SUPPLY_NOT_CREATED")

def notdeletesupply():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="SUPPLY_NOT_ELIMINATED")


def notupdatesupply():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="SUPPLY_NOT_UPDATED")

def nameisalreadyexist():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NAME_ALREADY_EXISTS")




