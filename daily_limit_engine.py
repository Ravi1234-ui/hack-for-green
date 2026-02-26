# ==========================================================
# DAILY LIMIT ENGINE - REAL-TIME FINANCIAL CONTROL SYSTEM
# ==========================================================

from datetime import datetime
from rag.memory_manager import get_daily_pocket_limit
from rag.live_state_store import load_live_metrics


# ==========================================================
# DATE UTILITIES
# ==========================================================

def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")


# ==========================================================
# CORE DAILY LIMIT CHECK (REAL-TIME)
# ==========================================================

def check_limit_for_date():

    state = load_live_metrics()
    daily_limit = get_daily_pocket_limit()

    if not daily_limit:
        return {
            "status": "limit_not_set",
            "date": get_today_string()
        }

    spent_today = state["financial_metrics"].get("daily_expense", 0.0)
    limit = float(daily_limit)

    remaining = limit - spent_today
    percent = (spent_today / limit) * 100 if limit > 0 else 0

    result = {
        "date": get_today_string(),
        "limit": round(limit, 2),
        "spent": round(spent_today, 2),
        "remaining": round(max(remaining, 0), 2),
        "percent_used": round(percent, 2)
    }

    if spent_today > limit:
        result["status"] = "exceeded"
        result["exceeded_by"] = round(spent_today - limit, 2)

    elif percent >= 80:
        result["status"] = "near_limit"

    else:
        result["status"] = "safe"
        result["saved"] = round(remaining, 2)

    return result


# ==========================================================
# SPENDING VELOCITY (REAL-TIME MONTH PROJECTION)
# ==========================================================

def spending_velocity():

    state = load_live_metrics()

    monthly_spent = state["financial_metrics"].get("monthly_expense", 0.0)
    income = state["financial_metrics"].get("monthly_income", 0.0)

    today_day = datetime.now().day

    if today_day == 0:
        return {"status": "no_data"}

    projected_monthly = (monthly_spent / today_day) * 30

    return {
        "average_daily_spending": round(monthly_spent / today_day, 2),
        "projected_monthly_spending": round(projected_monthly, 2),
        "monthly_income": income
    }


# ==========================================================
# RISK PREDICTION (MONTH-END)
# ==========================================================

def predict_over_spending():

    velocity = spending_velocity()

    if velocity.get("status"):
        return velocity

    income = velocity.get("monthly_income", 0)

    if income == 0:
        return {
            "status": "no_income_data"
        }

    projected = velocity["projected_monthly_spending"]

    if projected > income:
        return {
            "risk": "high",
            "message": "Projected spending exceeds income.",
            "projected_expense": projected,
            "income": income,
            "expected_deficit": round(projected - income, 2)
        }

    if projected > income * 0.8:
        return {
            "risk": "moderate",
            "message": "Spending is high relative to income.",
            "projected_expense": projected,
            "income": income
        }

    return {
        "risk": "low",
        "message": "Spending pace is healthy.",
        "projected_expense": projected,
        "income": income
    }


# ==========================================================
# BEHAVIOR TAGGING (REAL-TIME DISCIPLINE)
# ==========================================================

def behavioral_tagging():

    result = check_limit_for_date()

    status = result.get("status")

    if status == "exceeded":
        return "impulsive_spending"

    if status == "near_limit":
        return "borderline_control"

    return "disciplined"


# ==========================================================
# REDUCTION STRATEGY (CATEGORY-AWARE)
# ==========================================================

def generate_reduction_suggestions():

    state = load_live_metrics()
    category_totals = state.get("category_totals", {})

    suggestions = []

    if category_totals:

        # Sort by highest spending
        sorted_categories = sorted(
            category_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in sorted_categories[:3]:
            suggestions.append(
                f"Reduce spending in {category} (₹{round(amount, 2)})"
            )

    # Add general advice
    suggestions.extend([
        "Delay non-essential purchases.",
        "Cook at home instead of ordering food.",
        "Use public transport where possible.",
        "Set micro-limits for top spending categories."
    ])

    return suggestions
