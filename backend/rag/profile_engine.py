# rag/profile_engine.py

from rag.finance_engine import load_data
from datetime import datetime
from collections import defaultdict


# ==========================================
# HELPER: MONTH FILTER
# ==========================================
def _filter_by_month(data, month_prefix):
    filtered = []

    for row in data:
        try:
            date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
        except:
            try:
                date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            except:
                continue

        formatted = date_obj.strftime("%Y-%m")

        if formatted == month_prefix:
            filtered.append(row)

    return filtered


# ==========================================
# BUILD COMPLETE FINANCIAL PROFILE
# ==========================================
def build_financial_profile(month_prefix=None):
    """
    Builds a complete financial profile that can be used for:
    - Loan planning
    - Insurance advisory
    - Investment analysis
    - Goal planning
    - Risk evaluation
    """

    data = load_data()

    if not data:
        return {"error": "No transaction data available."}

    if not month_prefix:
        month_prefix = datetime.now().strftime("%Y-%m")

    data = _filter_by_month(data, month_prefix)

    income = 0
    expense = 0

    category_expense = defaultdict(float)
    fixed_expense = 0
    investment = 0
    debt_payment = 0

    for row in data:
        try:
            amount = float(row["amount"])
            category = row["category"].lower()
            txn_type = row["type"].lower()

            if txn_type == "income":
                income += amount

            elif txn_type == "expense":
                expense += amount
                category_expense[category] += amount

                # Fixed expense detection
                if category in ["housing", "loan", "bills"]:
                    fixed_expense += amount

                # Investment detection
                if category in ["investment", "sip", "mutual fund"]:
                    investment += amount

                # Debt detection
                if category in ["loan", "emi"]:
                    debt_payment += amount

        except:
            continue

    surplus = income - expense
    savings_rate = round((surplus / income) * 100, 2) if income > 0 else 0
    expense_ratio = round((expense / income) * 100, 2) if income > 0 else 0
    fixed_ratio = round((fixed_expense / expense) * 100, 2) if expense > 0 else 0
    investment_ratio = round((investment / income) * 100, 2) if income > 0 else 0
    debt_ratio = round((debt_payment / income) * 100, 2) if income > 0 else 0
    emergency_months = round(surplus / expense, 2) if expense > 0 else 0

    profile = {
        "month": month_prefix,
        "monthly_income": income,
        "monthly_expense": expense,
        "monthly_surplus": surplus,
        "savings_rate_percent": savings_rate,
        "expense_ratio_percent": expense_ratio,
        "fixed_expense_percent": fixed_ratio,
        "investment_ratio_percent": investment_ratio,
        "debt_ratio_percent": debt_ratio,
        "emergency_fund_months": emergency_months,
        "category_expense_breakdown": dict(category_expense)
    }

    return profile
