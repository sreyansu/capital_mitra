from fastapi import APIRouter

router = APIRouter(prefix="/sanction", tags=["Sanction"])

@router.get("/")
def get_sanction_letter():
    return {"link": "/static/letters/sanction_letter.pdf"}