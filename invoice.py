import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def load_invoices():
    """invoice.csv file-la irundhu invoices-ah padikkum."""
    invoice = pd.read_csv("invoice.csv", dtype={"bank_account": str})
    invoice["suspicious"] = False
    return invoice


def check_duplicates(invoice):
    """Same vendor + same amount irundha suspicious."""
    possible_dup = invoice.duplicated(subset=["vendor", "amount"])
    invoice.loc[possible_dup, "suspicious"] = True


def check_bank_change(invoice):
    """Vendor-oda bank account maariyirundha, andha vendor-oda ella rows-um suspicious."""
    bank_changed = invoice.groupby("vendor")["bank_account"].nunique() > 1
    bank_flag = invoice["vendor"].map(bank_changed)
    invoice.loc[bank_flag, "suspicious"] = True


def check_amount_anomaly(invoice):
    """Isolation Forest vechu thani-aana amounts-ah kandupidikkum."""
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(invoice[["amount"]])
    invoice["iso_pred"] = model.predict(invoice[["amount"]])
    invoice.loc[invoice["iso_pred"] == -1, "suspicious"] = True


def evaluate(invoice):
    """Model prediction-ah actual answer-oda compare pannum."""
    actual = invoice["is_fraud"]
    predicted = invoice["suspicious"].astype(int)

    print("Accuracy :", round(accuracy_score(actual, predicted), 2))
    print("Precision:", round(precision_score(actual, predicted), 2))
    print("Recall   :", round(recall_score(actual, predicted), 2))


def make_summary(invoice):
    """Flagged invoices-oda summary-ah text file-la save pannum."""
    flagged = invoice[invoice["suspicious"]]

    lines = [
        f"Total invoices: {len(invoice)}",
        f"Flagged: {len(flagged)}",
        "",
    ]
    for _, row in flagged.iterrows():
        lines.append(f"{row['invoice_id']} | {row['vendor']} | Rs {row['amount']}")

    text = "\n".join(lines)
    with open("summary_report.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


def main():
    invoice = load_invoices()

    check_duplicates(invoice)
    check_bank_change(invoice)
    check_amount_anomaly(invoice)

    print(invoice[["invoice_id", "vendor", "amount", "bank_account", "iso_pred", "suspicious"]])
    evaluate(invoice)
    make_summary(invoice)
    invoice.to_csv("flagged_invoices.csv", index=False)


if __name__ == "__main__":
    main()