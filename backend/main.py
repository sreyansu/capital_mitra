from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers import chat, upload, sanction, offer  

app = FastAPI(title="CapitalMitra Backend API")

# --- 1️⃣ CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2️⃣ Mount Static Folder ---
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# --- 3️⃣ Register Routers ---
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(sanction.router)
app.include_router(offer.router)

# --- 4️⃣ Root Endpoint ---
@app.get("/")
def home():
    return {"message": "✅ CapitalMitra backend is running successfully!"}