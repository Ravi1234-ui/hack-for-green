# ==========================================================
# MEMORY MANAGER - SAFE + ROBUST VERSION
# ==========================================================

import json
import os
from datetime import datetime
from typing import Any, Dict


HISTORY_FILE = "data/chat_history.json"
STATE_FILE = "data/conversation_state.json"
USER_MEMORY_FILE = "data/user_memory.json"

MAX_HISTORY = 200


# ==========================================================
# INTERNAL SAFE JSON HELPERS
# ==========================================================

def _safe_read_json(path: str, default: Any):
    if not os.path.exists(path):
        return default

    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data
    except Exception:
        return default


def _safe_write_json(path: str, data: Any):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


# ==========================================================
# INITIALIZATION
# ==========================================================

def initialize_memory():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        _safe_write_json(HISTORY_FILE, [])

    if not os.path.exists(STATE_FILE):
        _safe_write_json(STATE_FILE, {})

    if not os.path.exists(USER_MEMORY_FILE):
        _safe_write_json(USER_MEMORY_FILE, {})


# ==========================================================
# SHORT-TERM CHAT HISTORY
# ==========================================================

def save_chat(question: str, answer: str):
    initialize_memory()

    history = _safe_read_json(HISTORY_FILE, [])

    if not isinstance(history, list):
        history = []

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "answer": answer
    })

    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    _safe_write_json(HISTORY_FILE, history)


def get_recent_history(limit: int = 8):
    initialize_memory()

    history = _safe_read_json(HISTORY_FILE, [])

    if isinstance(history, list):
        return history[-limit:]

    return []


# ==========================================================
# CONVERSATION STATE (MULTI-STEP FLOW)
# ==========================================================

def load_state() -> Dict:
    initialize_memory()
    state = _safe_read_json(STATE_FILE, {})
    return state if isinstance(state, dict) else {}


def save_state(state: Dict):
    _safe_write_json(STATE_FILE, state)


def set_pending_intent(intent: str, required_fields=None):
    state = load_state()
    state["pending_intent"] = intent
    state["required_fields"] = required_fields or []
    state["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(state)


def clear_pending_intent():
    state = load_state()
    state.pop("pending_intent", None)
    state.pop("required_fields", None)
    save_state(state)


def get_pending_intent():
    state = load_state()
    return state.get("pending_intent"), state.get("required_fields", [])


def store_parameters(params: dict):
    state = load_state()
    state.setdefault("parameters", {})
    state["parameters"].update(params)
    save_state(state)


def get_parameters():
    state = load_state()
    return state.get("parameters", {})


# ==========================================================
# LONG-TERM USER MEMORY
# ==========================================================

def load_user_memory() -> Dict:
    initialize_memory()
    memory = _safe_read_json(USER_MEMORY_FILE, {})
    return memory if isinstance(memory, dict) else {}


def update_user_memory(key: str, value: Any):
    memory = load_user_memory()
    memory[key] = value
    _safe_write_json(USER_MEMORY_FILE, memory)


def get_user_memory(key: str = None):
    memory = load_user_memory()
    if key:
        return memory.get(key)
    return memory


# ==========================================================
# SALARY MANAGEMENT
# ==========================================================

def set_monthly_salary(amount: float):
    update_user_memory("monthly_salary", float(amount))
    update_user_memory(
        "salary_updated_at",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


def get_monthly_salary() -> float:
    value = get_user_memory("monthly_salary")
    return float(value) if value else 0.0


# ==========================================================
# DAILY POCKET LIMIT MANAGEMENT
# ==========================================================

def set_daily_pocket_limit(amount: float):
    update_user_memory("daily_pocket_limit", float(amount))
    update_user_memory(
        "daily_limit_updated_at",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


def get_daily_pocket_limit() -> float:
    value = get_user_memory("daily_pocket_limit")
    return float(value) if value else 0.0
