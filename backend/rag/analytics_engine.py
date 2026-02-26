from rag.finance_engine import (
    total_income,
    total_expense,
    category_spending,
    savings_rate as base_savings_rate,
)

import csv
from collections import defaultdict

CSV_FILE = "data/transactions.csv"


# ==========================================
# LOAD DATA (SAFE)
# ==========================================
def load_data():
    try:
        with open(CSV_FILE, "r") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


# ==========================================
# SAVINGS RATE (%)
# ==========================================
def savings_rate():
    return base_savings_rate()


# ==========================================
# INVESTMENT RATIO (% of income)
# ==========================================
def investment_ratio():
    data = load_data()
    income = total_income()
    investment = 0

    for row in data:
        if (
            row["type"].lower() == "expense"
            and row["category"].lower() == "investment"
        ):
            investment += float(row["amount"])

    if income == 0:
        return 0

    return round((investment / income) * 100, 2)


# ==========================================
# FIXED VS VARIABLE EXPENSE RATIO
# ==========================================
def fixed_variable_ratio():
    data = load_data()

    fixed_categories = ["housing", "loan", "bills", "emi", "rent"]
    fixed = 0
    variable = 0

    for row in data:
        if row["type"].lower() == "expense":
            if row["category"].lower() in fixed_categories:
                fixed += float(row["amount"])
            else:
                variable += float(row["amount"])

    total = fixed + variable

    if total == 0:
        return {
            "fixed_percent": 0,
            "variable_percent": 0
        }

    return {
        "fixed_percent": round((fixed / total) * 100, 2),
        "variable_percent": round((variable / total) * 100, 2)
    }


# ==========================================
# TOP SPENDING CATEGORY
# ==========================================
def top_spending_category():
    data = load_data()
    category_totals = defaultdict(float)

    for row in data:
        if row["type"].lower() == "expense":
            category_totals[row["category"]] += float(row["amount"])

    if not category_totals:
        return None

    highest = max(category_totals, key=category_totals.get)

    return {
        "category": highest,
        "amount": category_totals[highest]
    }


# ==========================================
# FINANCIAL HEALTH SCORE (0–100)
# ==========================================
def financial_health_score():
    score = 0

    sr = savings_rate()
    ir = investment_ratio()
    expense = total_expense()
    income = total_income()

    # ----------------------------------
    # 1️⃣ Savings Rate (40%)
    # ----------------------------------
    if sr >= 40:
        score += 40
    elif sr >= 25:
        score += 30
    elif sr >= 15:
        score += 20
    elif sr >= 5:
        score += 10
    else:
        score += 5

    # ----------------------------------
    # 2️⃣ Investment Discipline (30%)
    # ----------------------------------
    if ir >= 25:
        score += 30
    elif ir >= 15:
        score += 20
    elif ir >= 5:
        score += 10
    else:
        score += 5

    # ----------------------------------
    # 3️⃣ Expense Control (20%)
    # ----------------------------------
    if income > expense:
        score += 20
    else:
        score += 5

    # ----------------------------------
    # 4️⃣ Diversification (10%)
    # ----------------------------------
    top_cat = top_spending_category()
    if top_cat:
        percent = (top_cat["amount"] / expense) * 100 if expense else 0

        if percent < 40:
            score += 10
        else:
            score += 5

    return min(score, 100)


# ==========================================
# SMART INSIGHTS ENGINE
# ==========================================
def generate_insights():
    insights = []

    sr = savings_rate()
    ir = investment_ratio()
    score = financial_health_score()
    top_cat = top_spending_category()

    # Savings Insight
    if sr < 20:
        insights.append("⚠️ Your savings rate is below 20%. Consider reducing discretionary spending.")
    elif sr >= 40:
        insights.append("✅ Excellent savings discipline! You are building strong financial security.")

    # Investment Insight
    if ir < 10:
        insights.append("📈 Your investment allocation is low. Consider SIPs or long-term investments.")
    elif ir >= 20:
        insights.append("🚀 Great job investing consistently for long-term wealth.")

    # Expense Concentration
    if top_cat:
        insights.append(
            f"📊 Highest spending category: {top_cat['category']} (₹{top_cat['amount']:,.2f})."
        )

    # Financial Health
    if score >= 80:
        insights.append("🏆 Your overall financial health is strong.")
    elif score >= 60:
        insights.append("👍 Your finances are stable but can be optimized.")
    else:
        insights.append("🔎 Your financial health needs improvement.")

    if not insights:
        insights.append("👍 Your finances are stable.")

    return insights


# ==========================================
# CASHFLOW STABILITY
# ==========================================
def cashflow_status():
    income = total_income()
    expense = total_expense()

    if income == 0:
        return "No income recorded."

    ratio = expense / income

    if ratio < 0.6:
        return "Healthy cashflow. Expenses are well controlled."
    elif ratio < 0.9:
        return "Moderate cashflow. Monitor spending carefully."
    else:
        return "High expense ratio. Risk of financial stress."
