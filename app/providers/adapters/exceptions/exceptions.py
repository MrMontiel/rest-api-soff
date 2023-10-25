from fastapi import HTTPException, status

def noprovider():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PROVIDER_NOT_FOUND")

def requiredprovider():
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="PROVIDER_IS_REQUIRED")

def notcreatedprovider():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="PROVIDER_NOT_CREATED")

def notdeleteprovider():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="PROVIDER_NOT_ELIMINATED")


def notupdateprovider():
    raise HTTPException(status_code=status.HTTP_406_NOT_FOUND, detail="PROVIDER_NOT_UPDATED")




