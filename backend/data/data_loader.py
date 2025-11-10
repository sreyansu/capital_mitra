# backend/data/data_loader.py

import json
import os

DATA_DIR = os.path.dirname(__file__)

def load_json(file_name: str):
    """Loads a JSON file from the data directory."""
    path = os.path.join(DATA_DIR, file_name)
    with open(path, "r") as f:
        return json.load(f)

def get_customer(customer_id: str):
    data = load_json("customers.json")
    return next((c for c in data if c["customer_id"] == customer_id), None)

def get_offer(customer_id: str):
    data = load_json("offers.json")
    return next((o for o in data if o["customer_id"] == customer_id), None)

def get_credit_score(customer_id: str):
    data = load_json("credit_scores.json")
    return next((s for s in data if s["customer_id"] == customer_id), None)

def get_crm_record(customer_id: str):
    data = load_json("crm_data.json")
    return next((c for c in data if c["customer_id"] == customer_id), None)