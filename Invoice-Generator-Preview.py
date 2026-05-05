# By Jesse M, 06/2025

import csv
import os
import shutil
from docx import Document
from python_docx_replace import docx_replace
import datetime

INVOICE_TEMPLATE = "Invoice-Template.docx"
INVOICE_SAVE_LOCATION = "Invoices"

CLIENT_INDEX = 1
DATE_INDEX = 2
INVOICE_ID_INDEX = 4
PRICE_QUOTED_INDEX = 5

# Note: this are not real client names - this is just to show format.
CLIENT_FULL_NAMES = {
    "FB": "Fizz Buzz",
}

# Date now object
datenow = datetime.datetime.now()

# Get previous month
prev_month = (datenow.replace(day=1) - datetime.timedelta(days=1))
month_id = prev_month.strftime("%b")

input(f"For previous month - {month_id}.")

# Find CSV file in current directory
csv_file = None
for file in os.listdir():
    if file.endswith(".csv"):
        csv_file = file
        input(f"Found CSV file: {csv_file}")
        break
assert csv_file, "No CSV file found"

# Clear previous redundant invoices (for prev. month)
shutil.rmtree(INVOICE_SAVE_LOCATION)
os.mkdir(INVOICE_SAVE_LOCATION)

# Read CSV file
csv_file = open(csv_file)
csv_reader = csv.reader(csv_file)

invoice_data = {}

for row in csv_reader:
    # Skip header row
    if row[0] == "Status":
        continue
    
    invoice_id = row[INVOICE_ID_INDEX]
    # Skip irrelevant months
    if not f"-{month_id}-" in invoice_id:
        continue

    client_id = row[CLIENT_INDEX]

    if not client_id in invoice_data:
        invoice_data[client_id] = {
            "tutoring_dates": [],
            "amount_payable": 0,
            "invoice_id": invoice_id,
        }

    invoice_data[client_id]["tutoring_dates"].append(row[DATE_INDEX])

    price_quoted_str = row[PRICE_QUOTED_INDEX]
    if price_quoted_str and price_quoted_str[3] != "-":
        invoice_data[client_id]["amount_payable"] += float(price_quoted_str[3:])

# Ensure invoice data exists
assert invoice_data, f"No invoice data found for {month_id}."

print()
print("Generating invoices...")

current_date = datenow.strftime("%d/%m/%Y")

for client_id, data in invoice_data.items():
    if data["amount_payable"] == 0:
        print(f"No amount payable for client {client_id}. Skipping...")
        continue

    # Ensure client has an associated full name
    assert client_id in CLIENT_FULL_NAMES, f"Client '{client_id}' not in database."

    doc_data = {
        "invoice_id": data["invoice_id"],
        "current_date": current_date,
        "client_full_name": CLIENT_FULL_NAMES[client_id],
        "tutoring_dates": ", ".join(data["tutoring_dates"]),
        "amount_payable": int(data["amount_payable"]),
    }

    invoice_path = os.path.join(INVOICE_SAVE_LOCATION, f"Invoice-{data['invoice_id']}.docx")

    # Delete old document (if applicable)
    if os.path.isfile(invoice_path):
        os.remove(invoice_path)

    doc = Document(INVOICE_TEMPLATE)
    docx_replace(doc, **doc_data)

    doc.save(invoice_path)


csv_file.close()

print()
print("Invoices generated successfully!")
