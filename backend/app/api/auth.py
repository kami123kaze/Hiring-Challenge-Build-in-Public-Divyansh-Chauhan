from fastapi import APIRouter, Depends, HTTPException
from app.core.firebase import verify_firebase_token, assign_user_role, get_user_role
from app.models.game_models import TokenData

router = APIRouter()

# Route - verification
@router.post("/verify")
async def verify_user(data: TokenData):
    return verify_firebase_token(data.token)

# Route  - admin assign
@router.post("/assign-role/{uid}/{role}")
async def assign_role(uid: str, role: str):
    return assign_user_role(uid, role)

# Route - User 
@router.get("/get-role/{uid}")
async def get_role(uid: str):
    return get_user_role(uid)
