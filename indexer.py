from rag.retriever import add_document

with open("data/transactions.csv", "r") as f:
    lines = f.readlines()[1:]  # skip header

for line in lines:
    parts = line.strip().split(",")
    if len(parts) == 4:
        t, m, a, c = parts
        text = f"On {t}, you spent ₹{a} at {m} for {c}."
        add_document(text)

print("Index built successfully.")
