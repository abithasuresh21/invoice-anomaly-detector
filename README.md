# Invoice Anomaly Detector

A Python tool that checks incoming invoices for suspicious patterns and produces a daily summary report.

## Problem

Small businesses and freelancers often receive bills that contain:
- **Duplicate invoices** (same vendor and amount billed twice)
- **Bank account changes** (a vendor's payment details suddenly change, a common fraud sign)
- **Unusual amounts** (a bill far outside the normal range)

Checking every bill by hand is slow, and mistakes are easy to miss.

## Approach

The script runs three checks on each invoice:

1. **Duplicate check:** flags invoices with the same vendor and amount as an earlier invoice (pandas `duplicated`).
2. **Bank change check:** flags every invoice from a vendor that has used more than one bank account.
3. **Amount anomaly check:** uses Isolation Forest (scikit-learn) to flag amounts that are unusual compared with the rest of the data.

Flagged invoices are saved to `flagged_invoices.csv`, and a readable summary is written to `summary_report.txt`.

## Project Structure


## Input Format

`invoice.csv` must have these columns (an optional `is_fraud` column is used for evaluation):


## Setup

Requires Python 3.10+.

```bash
pip install pandas scikit-learn
```

## Usage

```bash
python invoice.py
```

The script prints the flagged table, the summary, and evaluation metrics (accuracy, precision, recall) if `is_fraud` is present.

## Results (synthetic test data, 11 invoices)

| Metric    | Value |
|-----------|-------|
| Accuracy  | 0.73  |
| Precision | 0.60  |
| Recall    | 0.75  |

## Limitations

- The test data is small and synthetic, so these numbers are not a measure of real-world performance.
- The Isolation Forest `contamination` value (0.1) is set by hand and affects which amounts get flagged.
- Amount checks use only the amount column. Vendor-specific price history is not yet considered.
- The bank-change rule flags every invoice from a vendor whose bank changed, including older genuine invoices, so it needs human review.

## Daily Automation

On Windows, the script can run every day using Task Scheduler:
- Program: path to `python.exe`
- Arguments: `invoice.py`
- Start in: the `invoice_project` folder

## Future Improvements

- Vendor-wise amount history instead of a single global check
- Email or WhatsApp alert for flagged invoices
- Streamlit dashboard
- Larger real or public dataset for more reliable evaluation

