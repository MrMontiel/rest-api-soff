from fastapi import Depends, HTTPException, status

def InvalidCredentials():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CREDENCIALES_INVALIDAS")

def UnauthorizedException():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INACTIVATE", headers= {"WWW-Authenticate": "Bearer"})

def InactivateUser():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INACTIVATE")

def EmailNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EMAIL_NOT_FOUND")

def CodeNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CODE_NOT_FOUND_OR_EXPIRED")

def CodeConfirmed():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CODE_CONFIRMATED")

def UserNotFound():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="USER_ID_NOT_FOUND")

def ApikeyNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="APIKEY_NOT_FOUND")