from fastapi import HTTPException, status


def Nouser():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER NOT FAUND")

def RequieredUser():
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="INFO IS REQUIRED")
    