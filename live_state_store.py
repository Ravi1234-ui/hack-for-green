# ==========================================================
# LIVE STATE STORE - REAL TIME FINANCIAL CORE
# ==========================================================

import json
import os
from datetime import datetime

LIVE_STATE_FILE = "data/live_state.json"


# ==========================================================
# INITIALIZE STATE
# ==========================================================

def _default_state():
    return {
        "financial_metrics": {
            "monthly_income": 0.0,
            "monthly_expense": 0.0,
            "daily_expense": 0.0,
            "net_savings": 0.0,
        },
        "category_totals": {},
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def _ensure_file():
    if not os.path.exists(LIVE_STATE_FILE):
        with open(LIVE_STATE_FILE, "w") as f:
            json.dump(_default_state(), f, indent=2)


# ==========================================================
# LOAD STATE
# ==========================================================

def load_live_metrics():
    _ensure_file()

    try:
        with open(LIVE_STATE_FILE, "r") as f:
            return json.load(f)
    except:
        # Recover if corrupted
        state = _default_state()
        save_live_metrics(state)
        return state


# ==========================================================
# SAVE STATE
# ==========================================================

def save_live_metrics(state):
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LIVE_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ==========================================================
# UPDATE SALARY
# ==========================================================

def update_monthly_income(amount: float):
    state = load_live_metrics()

    state["financial_metrics"]["monthly_income"] = float(amount)

    # Recalculate net savings
    income = state["financial_metrics"]["monthly_income"]
    expense = state["financial_metrics"]["monthly_expense"]

    state["financial_metrics"]["net_savings"] = income - expense

    save_live_metrics(state)
    return state["financial_metrics"]


# ==========================================================
# ADD EXPENSE
# ==========================================================

def add_expense(amount: float, category: str):
    state = load_live_metrics()

    amount = float(amount)

    # Update totals
    state["financial_metrics"]["monthly_expense"] += amount
    state["financial_metrics"]["daily_expense"] += amount

    # Update category
    if category not in state["category_totals"]:
        state["category_totals"][category] = 0.0

    state["category_totals"][category] += amount

    # Recalculate net savings
    income = state["financial_metrics"]["monthly_income"]
    expense = state["financial_metrics"]["monthly_expense"]

    state["financial_metrics"]["net_savings"] = income - expense

    save_live_metrics(state)

    return {
        "updated_metrics": state["financial_metrics"],
        "category_total": state["category_totals"][category]
    }


# ==========================================================
# RESET DAILY EXPENSE (midnight job)
# ==========================================================

def reset_daily_expense():
    state = load_live_metrics()
    state["financial_metrics"]["daily_expense"] = 0.0
    save_live_metrics(state)


# ==========================================================
# GET SUMMARY
# ==========================================================

def get_live_summary():
    state = load_live_metrics()
    return {
        "financial_metrics": state["financial_metrics"],
        "category_totals": state["category_totals"]
    }


# ==========================================================
# CLEAR ALL DATA (admin use)
# ==========================================================

def reset_all():
    save_live_metrics(_default_state())
