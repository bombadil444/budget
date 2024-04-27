import pandas as pd
from categories import category_groups


def clean_data(df):
    df["Particulars"] = df["Particulars"].str.replace(r"[^\w\s]", "", regex=True)
    df["Debits"] = df["Debits"].str.replace(r"[^\d\-+\.]", "", regex=True)
    df["Debits"] = pd.to_numeric(df["Debits"], errors="coerce")
    return df


# match transactions and sum up the category totals
# add transaction to "not found" if no match is found
def sum_totals(df):
    category_totals = {category: 0 for category in category_groups.keys()}
    category_totals["not found"] = 0
    not_found = []

    for particulars in df["Particulars"].unique():
        found = False
        for category, keywords in category_groups.items():
            if any(keyword in particulars.lower() for keyword in keywords):
                transactions = df[df["Particulars"] == particulars]
                category_totals[category] += transactions["Debits"].sum()
                found = True
                break
        if not found:
            transactions = df[df["Particulars"] == particulars]
            category_totals["not found"] += transactions["Debits"].sum()
            not_found.append(particulars)

    # Calculate grand total for all transactions
    grand_total = df["Debits"].sum()

    return category_totals, grand_total, not_found


def display_results(category_totals, grand_total, not_found):
    print("Category Totals:")
    for category, total in category_totals.items():
        print(f"{category.capitalize()}: {total:.2f}")
    print(f"\nGrand Total: ${grand_total:.2f}")

    print("\nNot found:")
    for particular in not_found:
        print(particular)


if __name__ == "__main__":
    data = pd.read_csv("spending\\202404.csv", usecols=["Date", "Particulars", "Debits"])
    data = clean_data(data)
    category_totals, grand_total, not_found = sum_totals(data)
    display_results(category_totals, grand_total, not_found)
