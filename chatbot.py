# ==========================================================
# INTELLIGENT FINANCIAL AI - CHATBOT CORE
# ==========================================================

from rag.intent_classifier import classify_intent
from rag.profile_engine import build_financial_profile
from rag.live_state_store import load_live_metrics
from groq import Groq

import os
import json
import re
import traceback
from rag.planning_engine import (
    loan_analysis,
    goal_planner,
    insurance_analysis,
    investment_projection,
    retirement_projection,
    stress_test
)
# NEW FEATURE IMPORTS
from rag.daily_limit_engine import (
    check_limit_for_date,
    predict_over_spending,
    generate_reduction_suggestions
)
from rag.memory_manager import (
    set_monthly_salary,
    set_daily_pocket_limit,
    get_daily_pocket_limit
)
from rag.budget_advisor import suggest_budget_allocation, save_recommended_budget
from rag.transaction_parser import add_transaction_from_text


from rag.finance_engine import *
from rag.analytics_engine import *
from rag.memory_manager import *

from rag.retriever import query_index
from groq import Groq

import os
import json
import re
import traceback

from datetime import datetime


# ==========================================================
# ENVIRONMENT SETUP
# ==========================================================

# ==========================================================
# SAFE GROQ CLIENT FACTORY (NEW)
# ==========================================================

def get_llm_client():
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not set.")

    return Groq(api_key=api_key)


# ==========================================================
# HELPER: EXTRACT NUMBERS
# ==========================================================

def extract_numbers(text):
    matches = re.findall(r"\d+(?:\.\d+)?", text)
    return list(map(float, matches))


# ==========================================================
# HELPER: DETECT MONTH
# ==========================================================

def detect_month_from_question(question):
    match = re.search(r"(20\d{2}-\d{2})", question)
    if match:
        return match.group(1)

    # fallback → current month
    return datetime.now().strftime("%Y-%m")
# ==========================================================
# TOOL EXECUTION MAP
# ==========================================================

def execute_financial_tool(intent, question, month_prefix):

    numbers = extract_numbers(question)
    live_metrics = load_live_metrics()
    profile = build_financial_profile(month_prefix)

    # Merge live metrics into profile (real-time override)
    if live_metrics and isinstance(live_metrics, dict):
        financial_live = live_metrics.get("financial_metrics", {})
        profile.update(financial_live)


    # ------------------------------------------------------
    # LOAN PLANNING
    # ------------------------------------------------------
    if intent == "loan_planning":

        if len(numbers) >= 3:
            principal, rate, tenure = numbers[:3]
            result = loan_analysis(principal, rate, tenure, month_prefix)
            clear_pending_intent()
            return result

        else:
            set_pending_intent("loan_planning", ["principal", "rate", "tenure"])
            return {
                "status": "missing_parameters",
                "required": ["principal", "rate", "tenure"]
            }

    # ------------------------------------------------------
    # GOAL PLANNING
    # ------------------------------------------------------
    if intent == "financial_goal":

        if len(numbers) >= 2:
            goal_amount, timeline = numbers[:2]
            result = goal_planner(goal_amount, timeline, month_prefix)
            clear_pending_intent()
            return result

        else:
            set_pending_intent("financial_goal", ["goal_amount", "timeline_months"])
            return {
                "status": "missing_parameters",
                "required": ["goal_amount", "timeline_months"]
            }

    # ------------------------------------------------------
    # INSURANCE
    # ------------------------------------------------------
    if intent == "insurance_planning":
        return insurance_analysis(month_prefix)

    # ------------------------------------------------------
    # INVESTMENT
    # ------------------------------------------------------
    if intent == "investment_planning":

        if len(numbers) >= 3:
            monthly, rate, years = numbers[:3]
            future_value = investment_projection(monthly, rate, years)
            return {"future_value": future_value}

        return {
            "status": "missing_parameters",
            "required": ["monthly_investment", "return_percent", "years"]
        }

    # ------------------------------------------------------
    # RETIREMENT
    # ------------------------------------------------------
    if intent == "retirement_planning":

        if len(numbers) >= 4:
            current_age, retirement_age, expense, inflation = numbers[:4]
            return retirement_projection(current_age, retirement_age, expense, inflation)

        return {
            "status": "missing_parameters",
            "required": ["current_age", "retirement_age", "monthly_expense", "inflation_percent"]
        }

    # ------------------------------------------------------
    # ADVISORY / HEALTH / RISK
    # ------------------------------------------------------
    if intent in ["advisory", "financial_health", "risk_analysis", "cashflow_analysis"]:
        return profile

    # ------------------------------------------------------
    # TRANSACTION DATA
    # ------------------------------------------------------
    if intent == "transaction_query":
        return profile
        # ------------------------------------------------------
    # DAILY LIMIT MANAGEMENT
    # ------------------------------------------------------
    if intent == "daily_limit_management":

        # If user setting limit
        if numbers:
            validated = float(numbers[0])
            set_daily_pocket_limit(validated)
            return {
                "status": "limit_set",
                "daily_limit": validated
            }

        # Otherwise check today's status
        return check_limit_for_date()

    # ------------------------------------------------------
    # INCOME UPDATE
    # ------------------------------------------------------
    if intent == "income_update":

        if numbers:
            salary = float(numbers[0])
            set_monthly_salary(salary)

            # Auto suggest allocation
            budget_plan = suggest_budget_allocation(salary)
            save_recommended_budget(budget_plan)

            return {
                "status": "salary_updated",
                "monthly_salary": salary,
                "recommended_budget": budget_plan
            }

        return {
            "status": "missing_parameters",
            "required": ["monthly_salary"]
        }

    # ------------------------------------------------------
    # TRANSACTION ENTRY
    # ------------------------------------------------------
    if intent == "transaction_entry":

        if len(numbers) >= 1:
            amount = numbers[0]

            # Basic default handling
            add_transaction(
                type_="expense",
                merchant="Manual Entry",
                category="General",
                amount=amount,
                account="HDFC Savings",
                payment_method="UPI"
            )

            return {
                "status": "transaction_added",
                "amount": amount
            }

        return {
            "status": "missing_parameters",
            "required": ["amount"]
        }

    # ------------------------------------------------------
    # BUDGET RECOMMENDATION
    # ------------------------------------------------------
    if intent == "budget_recommendation":

        profile = build_financial_profile(month_prefix)

        salary = profile.get("monthly_income")

        if salary:
            plan = suggest_budget_allocation(salary)
            return {
                "status": "budget_suggestion",
                "recommended_budget": plan
            }

        return {
            "status": "missing_salary"
        }


    return None
# ==========================================================
# LLM RESPONSE ENGINE
# ==========================================================

def generate_llm_response(question, tool_result=None):
    history = get_recent_history(limit=5)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional financial AI advisor. "
                "Provide clear, structured, analytical responses. "
                "Use provided financial context carefully."
            ),
        }
    ]

    # Inject conversation history
    for item in history:
        messages.append({"role": "user", "content": item["question"]})
        messages.append({"role": "assistant", "content": item["answer"]})

    # Inject tool result if exists
    context_parts = []

    if tool_result:
        context_parts.append(
            "Financial Computation Result:\n" +
            json.dumps(tool_result, indent=2)
        )

    # Inject live real-time metrics
    try:
        live_metrics = load_live_metrics()
        if live_metrics:
            context_parts.append(
                "Live Financial State:\n" +
                json.dumps(live_metrics.get("financial_metrics", {}), indent=2)
            )
    except:
        pass

    if context_parts:
        question = question + "\n\n" + "\n\n".join(context_parts)

    messages.append({"role": "user", "content": question})

    # ✅ SAFE CLIENT CREATION (NEW)
    client = get_llm_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content


# ==========================================================
# MAIN ASK ORCHESTRATOR
# ==========================================================

def ask(question):

    try:
        month_prefix = detect_month_from_question(question)

        # -------------------------------------------------
        # 1️⃣ Always classify first (important)
        # -------------------------------------------------
        classification = classify_intent(question)
        intent = classification["intent"]

        q_lower = question.lower().strip()

        # -------------------------------------------------
        # HARD OVERRIDE FOR SIMPLE CORE QUERIES
        # -------------------------------------------------
        if q_lower in [
            "salary",
            "income",
            "monthly salary",
            "monthly_salary",
            "monthly income"
        ]:
            intent = "transaction_query"

        # -------------------------------------------------
        # GENERAL CORE FINANCIAL QUERIES
        # -------------------------------------------------
        core_keywords = [
            "income",
            "expense",
            "monthly expense",
            "monthly income",
            "net savings",
            "spending",
            "surplus",
            "cashflow"
        ]

        if any(keyword in q_lower for keyword in core_keywords):
            intent = "transaction_query"



        # -------------------------------------------------
        # 2️⃣ Check if previous intent pending
        # -------------------------------------------------
        pending_intent, required_fields = get_pending_intent()

        # 🔄 If user changed topic → clear old pending
        if pending_intent and intent != pending_intent:
            clear_pending_intent()
            pending_intent = None

        # -------------------------------------------------
        # 3️⃣ Handle pending intent (if still active)
        # -------------------------------------------------
        if pending_intent:

            numbers = extract_numbers(question)

            if numbers:
                tool_result = execute_financial_tool(
                    pending_intent,
                    question,
                    month_prefix
                )

                # If calculation completed
                if tool_result and tool_result.get("status") != "missing_parameters":
                    clear_pending_intent()
                    answer = generate_llm_response(question, tool_result)
                    save_chat(question, answer)
                    return answer

            # Better conversational guidance
            example_hint = ""
            if pending_intent == "financial_goal":
                example_hint = "Example: '800000 in 12 months'"
            elif pending_intent == "loan_planning":
                example_hint = "Example: '5000000 8% 20 years'"

            answer = (
                f"To continue, I need: {', '.join(required_fields)}. "
                f"{example_hint}"
            )

            save_chat(question, answer)
            return answer

        # -------------------------------------------------
        # 4️⃣ Execute tool for new intent
        # -------------------------------------------------
        tool_result = execute_financial_tool(intent, question, month_prefix)

        if tool_result:

            if isinstance(tool_result, dict) and tool_result.get("status") == "missing_parameters":
                answer = (
                    f"I need more details: {', '.join(tool_result['required'])}. "
                    f"For example, include numbers like amount and timeline."
                )
                save_chat(question, answer)
                return answer

                        # Special handling for daily limit
            if intent == "daily_limit_management" and isinstance(tool_result, dict):

                status = tool_result.get("status")

                if status == "limit_set":
                    answer = f"✅ Daily pocket limit set to ₹{tool_result['daily_limit']}."

                elif status == "safe":
                    answer = (
                        f"🎉 You are within your daily limit.\n"
                        f"Spent: ₹{tool_result['spent']} / ₹{tool_result['limit']}\n"
                        f"Remaining: ₹{tool_result['remaining']}"
                    )

                elif status == "near_limit":
                    answer = (
                        f"⚠ You are near your daily limit.\n"
                        f"Spent: ₹{tool_result['spent']} / ₹{tool_result['limit']}"
                    )

                elif status == "exceeded":
                    tips = generate_reduction_suggestions()
                    answer = (
                        f"🚨 You exceeded your daily limit by ₹{tool_result['exceeded_by']}.\n\n"
                        f"Suggestions to reduce expenses:\n- " + "\n- ".join(tips)
                    )

                elif status == "limit_not_set":
                    answer = "Daily pocket limit is not set. Please set it first."

                else:
                    answer = generate_llm_response(question, tool_result)

                save_chat(question, answer)
                return answer


        # -------------------------------------------------
        # 5️⃣ RAG Fallback (semantic transaction retrieval)
        # -------------------------------------------------
        try:
            if intent != "transaction_query":
                retrieved_docs = query_index(question)
                if retrieved_docs:
                    context = "\n".join(retrieved_docs)
                    answer = generate_llm_response(
                        question + "\n\nRelevant Transaction Context:\n" + context
                    )
                    save_chat(question, answer)
                    return answer
        except Exception:
            pass


        # -------------------------------------------------
        # 6️⃣ Pure LLM (general finance / unrelated)
        # -------------------------------------------------
        answer = generate_llm_response(question)
        save_chat(question, answer)
        return answer

    except Exception as e:
        return f"⚠️ System Error: {str(e)}"



# ==========================================================
# RUN LOOP
# ==========================================================
if __name__ == "__main__":
    print("🚀 Advanced Financial AI Started")

    while True:
        try:
            user_input = input("\nAsk: ")

            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting.")
                break

            print("\n🤖 Answer:\n")
            print(ask(user_input))

        except Exception as e:
            print("⚠️ FULL ERROR TRACE:")
            traceback.print_exc()
