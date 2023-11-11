from fastapi import HTTPException, status

def Norole():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ROLE_NOT_FOUND")    
    
def Requieredrol():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ROLE_IS_REQUIRED")

def roleExists():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="THE_ROLE_ALREADY_EXISTS")


