# rag/budget_advisor.py

import json
import os

BUDGET_FILE = "data/recommended_budget.json"


# ==========================================================
# SMART BUDGET ALLOCATION BASED ON SALARY
# ==========================================================
def suggest_budget_allocation(monthly_income: float):

    monthly_income = float(monthly_income)

    allocation = {
        "Housing": monthly_income * 0.30,
        "Food": monthly_income * 0.12,
        "Transport": monthly_income * 0.08,
        "Utilities": monthly_income * 0.05,
        "Shopping": monthly_income * 0.08,
        "Investment": monthly_income * 0.20,
        "Emergency": monthly_income * 0.07,
        "Entertainment": monthly_income * 0.05
    }

    return {k: round(v, 2) for k, v in allocation.items()}


# ==========================================================
# SAVE RECOMMENDED BUDGET
# ==========================================================
def save_recommended_budget(budget_dict):

    os.makedirs("data", exist_ok=True)

    with open(BUDGET_FILE, "w") as f:
        json.dump(budget_dict, f, indent=2)


# ==========================================================
# LOAD RECOMMENDED BUDGET
# ==========================================================
def load_recommended_budget():

    if not os.path.exists(BUDGET_FILE):
        return {}

    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
