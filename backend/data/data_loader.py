import json
import os

DATA_DIR = os.path.dirname(__file__)

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_customer_by_id(cid):
    data = load_json("customers.json")
    return next((c for c in data if c["customer_id"] == cid), None)

def get_customer_by_pan(pan):
    data = load_json("customers.json")
    return next((c for c in data if c["pan"].upper() == pan.upper()), None)

def get_credit_score(cid):
    data = load_json("credit_scores.json")
    record = next((r for r in data if r["customer_id"] == cid), None)
    return record.get("credit_score") if record else None

def get_offers():
    return load_json("offers.json")