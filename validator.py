import re

def validate_invoice(data):
    issues = []

    # Required fields
    if not data.get("vendor"):
        issues.append("Missing vendor name")

    if not data.get("date"):
        issues.append("Missing invoice date")

    if not data.get("total_amount"):
        issues.append("Missing total amount")

    # Amount validation
    amount = str(data.get("total_amount", "")).replace(",", "").replace("$", "").replace("₹", "")
    
    try:
        float(amount)
    except:
        issues.append("Total amount is not a valid number")

    return issues