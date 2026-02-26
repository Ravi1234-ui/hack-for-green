# ==========================================================
# PATHWAY STREAM ENGINE - REAL-TIME RECONCILIATION LAYER
# ==========================================================

import time
import csv
import os
from datetime import datetime
from collections import defaultdict

from rag.live_state_store import save_live_metrics
from rag.memory_manager import load_user_memory


CSV_FILE = "data/transactions.csv"
CHECK_INTERVAL = 3  # seconds
LARGE_TX_THRESHOLD = 10000  # anomaly detection threshold


# ==========================================================
# SAFE CSV READ
# ==========================================================

def read_transactions():
    if not os.path.exists(CSV_FILE):
        return []

    try:
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


# ==========================================================
# COMPUTE LIVE METRICS FROM CSV
# ==========================================================

def compute_metrics(transactions):

    monthly_income = 0.0
    monthly_expense = 0.0
    daily_expense = 0.0
    category_totals = defaultdict(float)
    anomaly_flags = []
    budget_alerts = []

    # IMPORTANT: Match transaction_parser format
    today_str = datetime.now().strftime("%d-%m-%Y")
    current_month = datetime.now().strftime("%Y-%m")

    for row in transactions:
        try:
            amount = float(row.get("amount", 0))
            tx_type = row.get("type", "").lower()
            category = row.get("category", "General")

            # Parse date safely
            try:
                date_obj = datetime.strptime(row["date"], "%d-%m-%Y")
            except Exception:
                continue

            month_prefix = date_obj.strftime("%Y-%m")

            # -------------------------------
            # Monthly metrics
            # -------------------------------
            if month_prefix == current_month:
                if tx_type == "income":
                    monthly_income += amount
                else:
                    monthly_expense += amount
                    category_totals[category] += amount

            # -------------------------------
            # Daily metrics
            # -------------------------------
            if row["date"] == today_str and tx_type == "expense":
                daily_expense += amount

            # -------------------------------
            # Anomaly detection
            # -------------------------------
            if amount >= LARGE_TX_THRESHOLD:
                anomaly_flags.append({
                    "amount": amount,
                    "category": category,
                    "date": row["date"]
                })

        except Exception:
            continue

    net_savings = monthly_income - monthly_expense

    # ------------------------------------------------------
    # Budget Alert Check
    # ------------------------------------------------------
    user_memory = load_user_memory()
    recommended_budget = user_memory.get("recommended_budget", {})

    for category, limit in recommended_budget.items():
        spent = category_totals.get(category, 0.0)
        if limit and spent > limit:
            budget_alerts.append({
                "category": category,
                "limit": limit,
                "spent": spent,
                "status": "exceeded"
            })

    return {
        "financial_metrics": {
            "monthly_income": round(monthly_income, 2),
            "monthly_expense": round(monthly_expense, 2),
            "daily_expense": round(daily_expense, 2),
            "net_savings": round(net_savings, 2),
        },
        "category_totals": dict(category_totals),
        "budget_alerts": budget_alerts,
        "anomaly_flags": anomaly_flags,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ==========================================================
# STREAM LOOP (ROW COUNT BASED WATCHER - STABLE)
# ==========================================================

def start_stream():

    print("📡 Pathway Stream Engine Started...")

    last_row_count = 0

    while True:
        try:
            if not os.path.exists(CSV_FILE):
                time.sleep(CHECK_INTERVAL)
                continue

            transactions = read_transactions()
            current_row_count = len(transactions)

            # Detect change by row count
            if current_row_count != last_row_count:

                metrics = compute_metrics(transactions)

                # Overwrite live state
                save_live_metrics(metrics)

                last_row_count = current_row_count

                print("🔄 Live metrics reconciled from CSV.")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("⚠️ Stream Error:", e)
            time.sleep(CHECK_INTERVAL)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    start_stream()
