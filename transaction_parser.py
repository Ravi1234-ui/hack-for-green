# ==========================================================
# TRANSACTION PARSER - FULLY INTEGRATED WITH LIVE STATE
# ==========================================================

import csv
import re
import os
from datetime import datetime

from rag.live_state_store import add_expense, update_monthly_income

CSV_FILE = "data/transactions.csv"


# ==========================================================
# ENSURE CSV EXISTS
# ==========================================================

def _ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "date",
                "type",
                "merchant",
                "category",
                "amount",
                "account",
                "payment_method",
                "notes"
            ])


# ==========================================================
# CATEGORY KEYWORDS (Expandable)
# ==========================================================

CATEGORY_KEYWORDS = {
    "Food": ["food", "swiggy", "zomato", "restaurant", "dinner", "lunch", "pizza"],
    "Shopping": ["amazon", "shopping", "clothes", "electronics"],
    "Groceries": ["grocery", "bigbasket", "vegetables"],
    "Transport": ["uber", "ola", "transport", "cab"],
    "Housing": ["rent", "house", "emi"],
    "Investment": ["sip", "mutual fund", "investment"],
    "Income": ["salary", "income", "freelance", "credited", "received"],
    "Entertainment": ["movie", "netflix", "entertainment"]
}


ACCOUNT_KEYWORDS = {
    "HDFC Savings": ["hdfc"],
    "SBI Salary": ["sbi"],
    "Credit Card": ["credit", "card"]
}


PAYMENT_KEYWORDS = {
    "UPI": ["upi"],
    "Card": ["card"],
    "NetBanking": ["netbanking"],
    "Cash": ["cash"],
    "AutoDebit": ["autodebit"]
}


# ==========================================================
# EXTRACT AMOUNT (Robust)
# ==========================================================

def extract_amount(text):
    text = text.replace("₹", "").replace("rs", "").replace("Rs", "")
    matches = re.findall(r"\d+(?:\.\d+)?", text)
    if matches:
        return float(matches[0])
    return None


# ==========================================================
# DETECT CATEGORY
# ==========================================================

def detect_category(text):
    text = text.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return category

    return "General"


# ==========================================================
# DETECT ACCOUNT
# ==========================================================

def detect_account(text):
    text = text.lower()

    for account, keywords in ACCOUNT_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return account

    return "HDFC Savings"


# ==========================================================
# DETECT PAYMENT METHOD
# ==========================================================

def detect_payment_method(text):
    text = text.lower()

    for method, keywords in PAYMENT_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return method

    return "UPI"


# ==========================================================
# DETECT TYPE
# ==========================================================

def detect_type(text):
    text = text.lower()

    if any(word in text for word in ["earned", "income", "received", "salary", "credited"]):
        return "income"

    return "expense"


# ==========================================================
# ADD TRANSACTION FROM NATURAL LANGUAGE
# ==========================================================

def add_transaction_from_text(user_text):

    _ensure_csv()

    amount = extract_amount(user_text)

    if amount is None:
        return {
            "status": "error",
            "message": "No valid amount detected."
        }

    tx_type = detect_type(user_text)
    category = detect_category(user_text)
    account = detect_account(user_text)
    payment_method = detect_payment_method(user_text)

    date = datetime.now().strftime("%Y-%m-%d")  # consistent format

    merchant = "Manual Entry"

    new_row = [
        date,
        tx_type,
        merchant,
        category,
        amount,
        account,
        payment_method,
        user_text
    ]

    try:
        # --------------------------------------------------
        # Write to CSV
        # --------------------------------------------------
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(new_row)

        # --------------------------------------------------
        # Update LIVE STATE (critical)
        # --------------------------------------------------
        if tx_type == "income":
            update_monthly_income(amount)
        else:
            add_expense(amount, category)

        return {
            "status": "success",
            "type": tx_type,
            "amount": amount,
            "category": category,
            "account": account,
            "payment_method": payment_method
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
