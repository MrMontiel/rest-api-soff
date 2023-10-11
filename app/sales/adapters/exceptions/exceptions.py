from fastapi import HTTPException, status


def NoContentInOrder():
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="NO_CONTENT_IN_ORDER")

def OrderNotAvailability():
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="ORDER_NOT_AVAILABILITY")

def OrderNotFound():
    raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")