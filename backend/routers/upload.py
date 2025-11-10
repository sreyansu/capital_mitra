from fastapi import APIRouter, File, UploadFile
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("static/uploads", exist_ok=True)
    path = f"static/uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded successfully", "path": path}