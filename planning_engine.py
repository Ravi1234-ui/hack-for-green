# rag/planning_engine.py

from rag.profile_engine import build_financial_profile
import math


# ==========================================================
# EMI CALCULATOR
# ==========================================================
def emi_calculator(principal, annual_rate_percent, tenure_years):
    monthly_rate = annual_rate_percent / (12 * 100)
    months = tenure_years * 12

    if monthly_rate == 0:
        return round(principal / months, 2)

    emi = (
        principal
        * monthly_rate
        * ((1 + monthly_rate) ** months)
        / (((1 + monthly_rate) ** months) - 1)
    )

    return round(emi, 2)


# ==========================================================
# LOAN ANALYSIS (Advanced)
# ==========================================================
def loan_analysis(principal, annual_rate_percent, tenure_years, month_prefix):
    profile = build_financial_profile(month_prefix)
    if "error" in profile:
        return profile

    emi = emi_calculator(principal, annual_rate_percent, tenure_years)

    income = profile["monthly_income"]
    surplus = profile["monthly_surplus"]
    debt_ratio = profile["debt_ratio_percent"]

    emi_income_ratio = (emi / income) * 100 if income > 0 else 0
    emi_surplus_ratio = (emi / surplus) * 100 if surplus > 0 else 0

    if emi_income_ratio <= 30:
        affordability = "Safe"
    elif emi_income_ratio <= 50:
        affordability = "Manageable"
    else:
        affordability = "Risky"

    return {
        "emi": emi,
        "emi_income_ratio_percent": round(emi_income_ratio, 2),
        "emi_surplus_ratio_percent": round(emi_surplus_ratio, 2),
        "existing_debt_ratio_percent": debt_ratio,
        "affordability_status": affordability
    }


# ==========================================================
# GOAL SAVINGS PLANNER
# ==========================================================
def goal_planner(goal_amount, timeline_months, month_prefix):
    profile = build_financial_profile(month_prefix)
    if "error" in profile:
        return profile

    surplus = profile["monthly_surplus"]
    required_monthly = goal_amount / timeline_months

    if surplus <= 0:
        feasibility = "Not Feasible"
        months_needed = None
    elif surplus >= required_monthly:
        feasibility = "Feasible"
        months_needed = timeline_months
    else:
        feasibility = "Not Feasible"
        months_needed = math.ceil(goal_amount / surplus)

    return {
        "goal_amount": goal_amount,
        "timeline_months": timeline_months,
        "required_monthly_saving": round(required_monthly, 2),
        "current_surplus": surplus,
        "feasibility": feasibility,
        "months_needed_using_full_surplus": months_needed
    }


# ==========================================================
# INVESTMENT GROWTH PROJECTION
# ==========================================================
def investment_projection(monthly_investment, annual_return_percent, years):
    monthly_rate = annual_return_percent / (12 * 100)
    months = years * 12

    future_value = 0

    for _ in range(months):
        future_value = (future_value + monthly_investment) * (1 + monthly_rate)

    return round(future_value, 2)


# ==========================================================
# RETIREMENT CORPUS ESTIMATION
# ==========================================================
def retirement_projection(current_age, retirement_age, monthly_expense, inflation_percent):
    years_left = retirement_age - current_age

    future_expense = monthly_expense * ((1 + inflation_percent / 100) ** years_left)
    required_corpus = future_expense * 12 * 25  # 25x rule

    return {
        "years_to_retirement": years_left,
        "inflation_adjusted_monthly_expense": round(future_expense, 2),
        "required_retirement_corpus": round(required_corpus, 2)
    }


# ==========================================================
# INSURANCE COVERAGE MODEL
# ==========================================================
def insurance_analysis(month_prefix):
    profile = build_financial_profile(month_prefix)
    if "error" in profile:
        return profile

    annual_income = profile["monthly_income"] * 12
    recommended_term_cover = annual_income * 15

    emergency_status = (
        "Insufficient" if profile["emergency_fund_months"] < 6 else "Adequate"
    )

    return {
        "recommended_term_cover": recommended_term_cover,
        "emergency_fund_status": emergency_status
    }


# ==========================================================
# FINANCIAL STRESS TEST
# ==========================================================
def stress_test(additional_emi, month_prefix):
    profile = build_financial_profile(month_prefix)
    if "error" in profile:
        return profile

    surplus = profile["monthly_surplus"]
    new_surplus = surplus - additional_emi

    new_savings_rate = (
        (new_surplus / profile["monthly_income"]) * 100
        if profile["monthly_income"] > 0
        else 0
    )

    risk = "High Risk" if new_savings_rate < 20 else "Stable"

    return {
        "new_surplus": round(new_surplus, 2),
        "new_savings_rate_percent": round(new_savings_rate, 2),
        "risk_status": risk
    }


# ==========================================================
# FINANCIAL INDEPENDENCE TIME
# ==========================================================
def financial_independence_time(monthly_investment, annual_return_percent, target_corpus):
    monthly_rate = annual_return_percent / (12 * 100)
    months = 0
    corpus = 0

    while corpus < target_corpus:
        corpus = (corpus + monthly_investment) * (1 + monthly_rate)
        months += 1

        if months > 1000 * 12:
            return "Not achievable with current inputs"

    years = months / 12

    return {
        "months_needed": months,
        "years_needed": round(years, 2)
    }
