from fastapi import APIRouter
import json

router = APIRouter(prefix="/offer", tags=["Offer"])

@router.get("/")
def get_offers():
    with open("data/customers.json") as f:
        data = json.load(f)
    return data