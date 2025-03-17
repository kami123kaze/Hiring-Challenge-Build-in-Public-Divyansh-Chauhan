from fastapi import APIRouter, Depends, HTTPException, Header
from app.core.firebase import get_document_ref, verify_firebase_token

router = APIRouter()

# Save game progress & update leaderboard
@router.post("/game/save_progress")
async def save_game_progress(
    token: str = Header(...), score: int = 0, streak: int = 0, difficulty: str = "easy", username: str = "Guest"
):
    decoded_token = verify_firebase_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = decoded_token["uid"]

    # Save game progress in game_sessions
    game_ref = get_document_ref("game_sessions", user_id)
    game_ref.set({
        "score": score,
        "streak": streak,
        "difficulty": difficulty
    }, merge=True)

    # Update leaderboard (only if new score is higher)
    leaderboard_ref = get_document_ref("leaderboard", user_id)
    existing_doc = leaderboard_ref.get()

    if existing_doc.exists:
        existing_score = existing_doc.to_dict().get("score", 0)
        if score > existing_score:  # Only update if new score is higher
            leaderboard_ref.set({
                "userId": user_id,
                "username": username,
                "score": score
            }, merge=True)
    else:
        leaderboard_ref.set({
            "userId": user_id,
            "username": username,
            "score": score
        })

    return {"message": "Game progress & leaderboard updated"}

# Retrieve game progress
@router.get("/game/get_progress")
async def get_game_progress(token: str = Header(...)):
    decoded_token = verify_firebase_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = decoded_token["uid"]
    game_ref = get_document_ref("game_sessions", user_id)
    doc = game_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"score": 0, "streak": 0, "difficulty": "easy"}  # Default values
