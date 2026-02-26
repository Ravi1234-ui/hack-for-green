# rag/intent_classifier.py

from groq import Groq
import os
import json
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set.")

client = Groq(api_key=API_KEY)


# ==========================================================
# AVAILABLE INTENTS (Extended Professional Coverage)
# ==========================================================
INTENT_LIST = {
    # Core finance
    "transaction_query",
    "budget_analysis",
    "financial_goal",
    "loan_planning",
    "insurance_planning",
    "investment_planning",
    "retirement_planning",
    "tax_planning",
    "risk_analysis",
    "cashflow_analysis",
    "financial_health",
    "advisory",
    "general_finance",
    "market_information",

    # Advanced system features
    "daily_limit_management",
    "income_update",
    "transaction_entry",
    "behavioral_analysis",
    "spending_pattern",
    "budget_recommendation",
    "financial_strategy",
    "comparison_analysis",

    # Fallback
    "unrelated"
}


# ==========================================================
# INTENT CLASSIFIER (Safe + Robust)
# ==========================================================
def classify_intent(question: str) -> dict:
    """
    Returns:
    {
        "intent": "<category>",
        "confidence": "high/medium/low"
    }
    """

    prompt = f"""
You are a professional intent classifier for an advanced AI Financial Assistant.

Classify the user's question into ONE best-matching category.

The assistant supports:

--- Core Finance ---
1. transaction_query
2. budget_analysis
3. financial_goal
4. loan_planning
5. insurance_planning
6. investment_planning
7. retirement_planning
8. tax_planning
9. risk_analysis
10. cashflow_analysis
11. financial_health
12. advisory
13. general_finance
14. market_information

--- Advanced System Features ---
15. daily_limit_management
16. income_update
17. transaction_entry
18. behavioral_analysis
19. spending_pattern
20. budget_recommendation
21. financial_strategy
22. comparison_analysis

23. unrelated

Respond ONLY in valid JSON format like this:

{{
  "intent": "loan_planning",
  "confidence": "high"
}}

User Question:
"{question}"
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # --------------------------------------------------
        # SAFE JSON EXTRACTION
        # --------------------------------------------------
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON manually if model adds text
            try:
                start = content.index("{")
                end = content.rindex("}") + 1
                result = json.loads(content[start:end])
            except:
                return {"intent": "general_finance", "confidence": "low"}

        intent = result.get("intent", "").strip()
        confidence = result.get("confidence", "low")

        if intent not in INTENT_LIST:
            return {"intent": "general_finance", "confidence": "low"}

        if confidence not in ["high", "medium", "low"]:
            confidence = "low"

        return {
            "intent": intent,
            "confidence": confidence
        }

    except Exception:
        return {"intent": "general_finance", "confidence": "low"}
