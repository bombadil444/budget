import os
import pandas as pd
from categories import category_groups
from utils import get_date_str
from utils import ensure_root_cwd, init_google_sheet
from dotenv import load_dotenv
import sys


# match transactions and sum up the category totals
# add transaction to "not found" if no match is found
def sum_totals(df):
    category_totals = {category: 0 for category in category_groups.keys()}
    category_totals["not found"] = 0
    not_found = []

    for particulars in df["Particulars"].unique():
        found = False
        transactions = df[df["Particulars"] == particulars]
        debits = transactions["Debits"].sum()
        try:
            for category, keywords in category_groups.items():
                if any(keyword in particulars.lower() for keyword in keywords):
                    category_totals[category] += debits
                    found = True
                    break
            if not found:
                category_totals["not found"] += debits
                not_found.append([particulars, debits])
        except TypeError as e:
            print("Check csv to make sure all values are numeric")
            raise

    # calculate grand total for all transactions
    grand_total = df["Debits"].sum()

    return category_totals, grand_total, not_found


def display_results(category_totals, grand_total, not_found):
    print("Category Totals:")
    for category, total in category_totals.items():
        print(f"{category.capitalize()}: {total:.2f}")
    print(f"\nGrand Total: ${grand_total:.2f}")

    print("\nNot found:")
    sorted_not_found = sorted(not_found, key=lambda x: x[1], reverse=True)
    for row in sorted_not_found:
        print(f"{row[0]},   {row[1]}")


if __name__ == "__main__":
    ensure_root_cwd()
    load_dotenv()

    # generate data
    data = pd.read_csv(f"data\\{get_date_str()}.csv", usecols=["Particulars", "Debits"])
    category_totals, grand_total, not_found = sum_totals(data)

    # print data
    display_results(category_totals, grand_total, not_found)

    # if argument provided, update spreadsheet
    if len(sys.argv) > 1:
        client = init_google_sheet()

        # first arg is the cell in the spreadsheet to write to
        cell_to_insert = sys.argv[1]

        sheet = client.open_by_key(os.getenv("SPREADSHEET_ID")).worksheet(
            os.getenv("SHEET_NAME")
        )
        sheet_data = list(zip(list(category_totals.values())))
        sheet.update(range_name=cell_to_insert, values=sheet_data)
