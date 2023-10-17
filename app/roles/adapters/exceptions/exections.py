from fastapi import HTTPException, status

def Norole():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    
def Requieredrol():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role is required")


