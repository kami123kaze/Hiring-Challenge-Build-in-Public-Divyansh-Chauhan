from pydantic import BaseModel
from typing import Optional

# User 
class User(BaseModel):
    uid: str
    email: str
    role: str = "student"

# Game session 
class GameSession(BaseModel):
    session_id: str
    user_id: str
    start_time: str
    end_time: Optional[str] = None
    score: Optional[int] = 0
    attempts: Optional[int] = 0
    level: int

# token for auth
class TokenData(BaseModel):
    uid: str
    email: str
    role: str
