from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import csv


# ======================================================
# CONFIGURATION
# ======================================================
EMBEDDING_DIM = 384
INDEX_FILE = "vector.index"
DOC_FILE = "documents.pkl"
CSV_FILE = "data/transactions.csv"


# ======================================================
# GLOBAL LAZY OBJECTS
# ======================================================
model = None
index = None
documents = []


# ======================================================
# SAFE LAZY LOADER
# ======================================================
def load_model():
    global model
    if model is None:
        try:
            model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print(f"⚠️ Failed to load embedding model: {e}")
            model = None
    return model


def load_index():
    global index, documents

    if index is not None:
        return

    try:
        if os.path.exists(INDEX_FILE) and os.path.exists(DOC_FILE):
            index = faiss.read_index(INDEX_FILE)
            with open(DOC_FILE, "rb") as f:
                documents = pickle.load(f)
        else:
            index = faiss.IndexFlatL2(EMBEDDING_DIM)
            documents = []
    except Exception as e:
        print(f"⚠️ Failed to load index: {e}")
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        documents = []


# ======================================================
# SAVE STATE
# ======================================================
def save_state():
    global index, documents
    try:
        if index:
            faiss.write_index(index, INDEX_FILE)
            with open(DOC_FILE, "wb") as f:
                pickle.dump(documents, f)
    except Exception as e:
        print(f"⚠️ Failed saving state: {e}")


# ======================================================
# ADD DOCUMENT
# ======================================================
def add_document(text, structured_data=None):
    global index, documents

    load_model()
    load_index()

    if not model:
        return

    try:
        vector = model.encode([text]).astype("float32")
        faiss.normalize_L2(vector)
        index.add(vector)

        documents.append({
            "text": text,
            "data": structured_data
        })

        save_state()

    except Exception as e:
        print(f"⚠️ Failed to add document: {e}")


# ======================================================
# SEMANTIC SEARCH
# ======================================================
def query_index(query, k=5):

    load_model()
    load_index()

    if not model or not documents:
        return []

    try:
        query_vector = model.encode([query]).astype("float32")
        faiss.normalize_L2(query_vector)

        distances, indices = index.search(
            query_vector,
            min(k, len(documents))
        )

        results = []
        for i in indices[0]:
            if i < len(documents):
                results.append(documents[i]["text"])

        return results

    except Exception as e:
        print(f"⚠️ Query failed: {e}")
        return []


# ======================================================
# STRUCTURED ACCESS
# ======================================================
def get_all_structured():
    load_index()
    return [
        doc["data"]
        for doc in documents
        if doc.get("data")
    ]


# ======================================================
# STRUCTURED SUMMARY
# ======================================================
def structured_summary():
    data = get_all_structured()

    total_income = 0
    total_expense = 0

    for row in data:
        if row["type"].lower() == "income":
            total_income += float(row["amount"])
        else:
            total_expense += float(row["amount"])

    return {
        "income": total_income,
        "expense": total_expense,
        "net": total_income - total_expense
    }


# ======================================================
# REBUILD INDEX FROM CSV
# ======================================================
def rebuild_index_from_csv(csv_path=CSV_FILE):

    load_model()

    global index, documents

    if not model:
        print("❌ Embedding model not loaded.")
        return

    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    documents = []

    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:

                structured = {
                    "date": row["date"],
                    "type": row["type"],
                    "merchant": row["merchant"],
                    "category": row["category"],
                    "amount": float(row["amount"]),
                    "account": row["account"],
                    "payment_method": row["payment_method"],
                    "notes": row.get("notes", "")
                }

                text = (
                    f"On {structured['date']}, you made a {structured['type']} of ₹{structured['amount']} "
                    f"at {structured['merchant']} for {structured['category']} "
                    f"using {structured['payment_method']} from {structured['account']}."
                )

                vector = model.encode([text]).astype("float32")
                faiss.normalize_L2(vector)
                index.add(vector)

                documents.append({
                    "text": text,
                    "data": structured
                })

        save_state()
        print("✅ Index rebuilt successfully.")

    except Exception as e:
        print(f"❌ Error rebuilding index: {e}")
