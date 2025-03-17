from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import auth, game
from app.api import dashboard

# Initialize FastAPI
app = FastAPI(title="Balance Scale Addition Game Backend")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "https://hiring-challenge-build-in-public.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(game.router, prefix="/game", tags=["Game"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "Balance Scale Addition Game Backend is Running"}