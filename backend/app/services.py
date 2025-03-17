from firebase_admin import auth, firestore
from fastapi import HTTPException

# Firestore instance
db = firestore.client()

# Service - Assign role to user
def assign_role(uid: str, role: str):
    try:
        db.collection("users").document(uid).set({"role": role}, merge=True)
        auth.set_custom_user_claims(uid, {"role": role})
        return {"message": f"Role '{role}' assigned to user {uid}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Service - Get user role
def get_user_role(uid: str):
    try:
        user = auth.get_user(uid)
        return {"uid": uid, "role": user.custom_claims.get("role", "student")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Service - Save game session
def save_game_session(session_data: dict):
    try:
        session_ref = db.collection("game_sessions").document(session_data["session_id"])
        session_ref.set(session_data)
        return {"message": "Game session saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Service - Fetch game session
def get_game_session(session_id: str):
    try:
        session_doc = db.collection("game_sessions").document(session_id).get()
        if session_doc.exists:
            return session_doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
