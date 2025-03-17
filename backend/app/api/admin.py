from fastapi import APIRouter, HTTPException, Depends
from app.core.firebase import db

router = APIRouter()

# admin only func's 


@router.get("/users")
async def get_all_users():
    users_ref = db.collection("users").stream()
    users = [{"uid": user.id, **user.to_dict()} for user in users_ref]
    return {"users": users}


@router.delete("/delete-user/{uid}")
async def delete_user(uid: str):
    try:
        db.collection("users").document(uid).delete()
        return {"message": f"User {uid} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))