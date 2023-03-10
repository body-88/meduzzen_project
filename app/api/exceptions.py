from fastapi import HTTPException
from fastapi import status

def raise_not_authenticated():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authenticated"
    )
    
def wrong_account():
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="It's not your account"
        )