from fastapi import APIRouter, HTTPException
from app.core.firebase import db

router = APIRouter()

# Route - Fetch User Profile
@router.get("/profile/{uid}")
async def get_user_profile(uid: str):
    user_doc = db.collection("users").document(uid).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user_doc.to_dict()

# Route - Update User Profile
@router.put("/profile/{uid}")
async def update_user_profile(uid: str, profile_data: dict):
    try:
        db.collection("users").document(uid).set(profile_data, merge=True)
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route - Delete User Account
@router.delete("/profile/{uid}")
async def delete_user_profile(uid: str):
    try:
        db.collection("users").document(uid).delete()
        return {"message": "User profile deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
