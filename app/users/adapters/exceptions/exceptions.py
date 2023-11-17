from fastapi import HTTPException, status


def Nouser():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FAUND")

def RequieredUser():
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="INFO_IS_REQUIRED")

def UserExists():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="THE_USER_ALREADY_EXISTS")

def UserExistsEmail():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="THE_EMAIL_USER_ALREADY_EXISTS")
