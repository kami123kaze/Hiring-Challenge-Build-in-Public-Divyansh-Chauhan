from fastapi import APIRouter, HTTPException
from app.core.firebase import db

router = APIRouter()


@router.get("/stats/{uid}")
async def get_user_stats(uid: str):
    stats_doc = db.collection("game_stats").document(uid).get()
    if not stats_doc.exists:
        raise HTTPException(status_code=404, detail="No stats found for this user")
    return stats_doc.to_dict()


@router.get("/stats/overall")
async def get_overall_stats():
    stats_ref = db.collection("game_stats").stream()
    stats = [stat.to_dict() for stat in stats_ref]
    return {"overall_stats": stats}
