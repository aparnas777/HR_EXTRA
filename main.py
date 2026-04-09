from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from user_routes import router as user_router
from admin_routes import router as admin_router
import os

app = FastAPI(title="HR Policy Chatbot API")

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

# Mount static directories
# Verify the paths are correct based on the project root
base_dir = os.path.dirname(__file__)
user_path = os.path.join(base_dir, "user")
admin_path = os.path.join(base_dir, "admin")

# Create folders if they don't exist
os.makedirs(user_path, exist_ok=True)
os.makedirs(admin_path, exist_ok=True)

app.mount("/user", StaticFiles(directory=user_path, html=True), name="user_ui")
app.mount("/admin", StaticFiles(directory=admin_path, html=True), name="admin_ui")

@app.get("/")
async def root():
    # Redirect base to the user UI
    return RedirectResponse(url="/user/")

# To run: uvicorn main:app --reload