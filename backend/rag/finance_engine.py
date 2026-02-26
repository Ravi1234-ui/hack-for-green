import csv
from collections import defaultdict
from datetime import datetime
import json

BUDGET_FILE = "data/budget.json"


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
# LOAD BUDGET DATA
# ==========================================
def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


# ==========================================
# TOTAL INCOME
# ==========================================
def total_income():
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "income"
    )


# ==========================================
# TOTAL EXPENSE
# ==========================================
def total_expense():
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "expense"
    )


# ==========================================
# NET SAVINGS
# ==========================================
def net_savings():
    return total_income() - total_expense()


# ==========================================
# CATEGORY SPENDING
# ==========================================
def category_spending(category):
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "expense"
        and row["category"].lower() == category.lower()
    )


# ==========================================
# ACCOUNT WISE SPENDING
# ==========================================
def account_wise_spending(account=None):
    data = load_data()
    summary = defaultdict(float)

    for row in data:
        if row["type"].lower() == "expense":
            summary[row["account"]] += float(row["amount"])

    if account:
        return summary.get(account, 0)

    if not summary:
        return "No account data available."

    most_used = max(summary, key=summary.get)
    return f"Most Used Account: {most_used} (₹{summary[most_used]:,.2f})"


# ==========================================
# ACCOUNT BALANCE (INCOME - EXPENSE)
# ==========================================
def account_balance(account):
    data = load_data()
    balance = 0

    for row in data:
        if row["account"].lower() == account.lower():
            if row["type"].lower() == "income":
                balance += float(row["amount"])
            else:
                balance -= float(row["amount"])

    return balance

# ==========================================
# MONTHLY INCOME
# ==========================================
def monthly_income(month_prefix):
    data = load_data()
    total = 0

    for row in data:
        try:
            date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            formatted = date_obj.strftime("%Y-%m")

            if formatted == month_prefix and row["type"].lower() == "income":
                total += float(row["amount"])

        except Exception:
            continue

    return total


# ==========================================
# MONTHLY EXPENSE
# ==========================================
def monthly_expense(month_prefix):
    data = load_data()
    total = 0

    for row in data:
        try:
            date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            formatted = date_obj.strftime("%Y-%m")

            if formatted == month_prefix and row["type"].lower() == "expense":
                total += float(row["amount"])

        except Exception:
            continue

    return total


# ==========================================
# MONTHLY SAVINGS RATE
# ==========================================
def savings_rate_monthly(month_prefix):
    income = monthly_income(month_prefix)
    expense = monthly_expense(month_prefix)

    if income == 0:
        return 0

    return round(((income - expense) / income) * 100, 2)

# ==========================================
# MONTHLY SUMMARY (DD-MM-YYYY SAFE)
# ==========================================
def monthly_summary(month_prefix):
    """
    Example:
    '2026-02'
    """
    data = load_data()
    income = 0
    expense = 0

    for row in data:
        try:
            date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            formatted = date_obj.strftime("%Y-%m")

            if formatted == month_prefix:
                if row["type"].lower() == "income":
                    income += float(row["amount"])
                else:
                    expense += float(row["amount"])

        except Exception:
            continue

    return {
        "income": income,
        "expense": expense,
        "net": income - expense
    }


# ==========================================
# HIGHEST CATEGORY
# ==========================================
def highest_category():
    data = load_data()
    category_totals = defaultdict(float)

    for row in data:
        if row["type"].lower() == "expense":
            category_totals[row["category"]] += float(row["amount"])

    if not category_totals:
        return None

    highest = max(category_totals, key=category_totals.get)
    return f"{highest} (₹{category_totals[highest]:,.2f})"


# ==========================================
# BIGGEST TRANSACTION
# ==========================================
def biggest_transaction():
    data = load_data()
    max_tx = None
    max_amount = 0

    for row in data:
        amt = float(row["amount"])
        if amt > max_amount:
            max_amount = amt
            max_tx = row

    if not max_tx:
        return None

    return (
        f"Biggest Transaction: ₹{float(max_tx['amount']):,.2f} "
        f"at {max_tx['merchant']} "
        f"({max_tx['category']})"
    )


# ==========================================
# SAVINGS RATE (%)
# ==========================================
def savings_rate():
    income = total_income()
    expense = total_expense()

    if income == 0:
        return 0

    return round(((income - expense) / income) * 100, 2)


# ==========================================
# PAYMENT METHOD SPENDING
# ==========================================
def payment_method_spending(method):
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "expense"
        and row["payment_method"].lower() == method.lower()
    )


# ==========================================
# INCOME BY SOURCE
# ==========================================
def income_by_source(source):
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "income"
        and source.lower() in row["merchant"].lower()
    )


# ==========================================
# MERCHANT SPENDING
# ==========================================
def merchant_spending(merchant):
    data = load_data()
    return sum(
        float(row["amount"])
        for row in data
        if row["type"].lower() == "expense"
        and merchant.lower() in row["merchant"].lower()
    )


# ==========================================
# SPENDING TREND (Daily)
# ==========================================
def daily_spending_summary():
    data = load_data()
    summary = defaultdict(float)

    for row in data:
        if row["type"].lower() == "expense":
            summary[row["date"]] += float(row["amount"])

    return dict(summary)


# ==========================================
# EXPENSE BY ACCOUNT + CATEGORY
# ==========================================
def account_category_breakdown(account):
    data = load_data()
    summary = defaultdict(float)

    for row in data:
        if (
            row["type"].lower() == "expense"
            and row["account"].lower() == account.lower()
        ):
            summary[row["category"]] += float(row["amount"])

    return dict(summary)
# =============================
# TRANSACTION COUNT
# =============================
def transaction_count(category=None, date=None):
    data = load_data()
    count = 0

    for row in data:
        if row["type"].lower() != "expense":
            continue

        if category and row["category"].lower() != category.lower():
            continue

        if date and row["date"] != date:
            continue

        count += 1

    return count


# =============================
# PERCENTAGE OF CATEGORY (vs Income)
# =============================
def percentage_of_category(category):
    income = total_income()
    category_total = category_spending(category)

    if income == 0:
        return 0

    return round((category_total / income) * 100, 2) if income > 0 else 0



# =============================
# DATE BASED SPENDING
# =============================
def date_based_spending(date_str):
    data = load_data()
    total = 0

    for row in data:
        if row["type"].lower() == "expense" and row["date"] == date_str:
            total += float(row["amount"])

    return total
# ==========================================
# BUDGET STATUS CHECK
# ==========================================
def check_budget_status(month_prefix=None):
    data = load_data()
    budgets = load_budget()
    result = {}

    # Calculate expense totals per category for month (if given)
    category_totals = defaultdict(float)

    for row in data:
        try:
            if row["type"].lower() != "expense":
                continue

            if month_prefix:
                date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
                formatted = date_obj.strftime("%Y-%m")
                if formatted != month_prefix:
                    continue

            category_totals[row["category"]] += float(row["amount"])

        except Exception:
            continue

    # Compare with budgets
    for category, budget in budgets.items():
        spent = category_totals.get(category, 0)
        percent = (spent / budget) * 100 if budget > 0 else 0

        if percent < 80:
            status = "Within Limit"
        elif percent <= 100:
            status = "Warning"
        else:
            status = "Exceeded"

        result[category] = {
            "budget": budget,
            "spent": round(spent, 2),
            "percent_used": round(percent, 2),
            "status": status
        }

    return result
# ==========================================
# LARGE TRANSACTION DETECTION
# ==========================================
def detect_large_transactions(threshold=5000):
    data = load_data()
    large_txns = []

    for row in data:
        try:
            amount = float(row["amount"])
            if amount > threshold:
                large_txns.append(row)
        except Exception:
            continue

    large_txns.sort(key=lambda x: float(x["amount"]), reverse=True)
    return large_txns
# ==========================================
# CATEGORY SPIKE DETECTION
# ==========================================
def detect_category_spike(category, current_month, previous_month):
    current = 0
    previous = 0

    data = load_data()

    for row in data:
        try:
            if row["type"].lower() != "expense":
                continue

            if row["category"].lower() != category.lower():
                continue

            date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            formatted = date_obj.strftime("%Y-%m")

            if formatted == current_month:
                current += float(row["amount"])
            elif formatted == previous_month:
                previous += float(row["amount"])

        except Exception:
            continue

    if previous == 0:
        return {"alert": False}

    increase_percent = ((current - previous) / previous) * 100

    return {
        "category": category,
        "current": round(current, 2),
        "previous": round(previous, 2),
        "increase_percent": round(increase_percent, 2),
        "alert": increase_percent > 30
    }
# ==========================================
# FINANCIAL HEALTH SCORE
# ==========================================
def financial_health_score(month_prefix):
    income = monthly_income(month_prefix)
    expense = monthly_expense(month_prefix)

    if income == 0:
        return 0

    savings_rate_value = savings_rate_monthly(month_prefix)
    expense_control = 100 - ((expense / income) * 100)

    budget_status = check_budget_status(month_prefix)

    discipline_count = 0
    total_categories = len(budget_status)

    for cat in budget_status.values():
        if cat["status"] == "Within Limit":
            discipline_count += 1

    discipline_score = (
        (discipline_count / total_categories) * 100
        if total_categories > 0
        else 0
    )

    score = (
        savings_rate_value * 0.4 +
        expense_control * 0.2 +
        discipline_score * 0.2 +
        20  # Investment placeholder
    )

    return round(score, 2)
