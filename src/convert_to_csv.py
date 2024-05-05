import tabula
from pdfminer.high_level import extract_pages
from utils import get_date_str, ensure_root_cwd


def count_pdf_pages(pdf_path):
    try:
        num_pages = 0
        for _ in extract_pages(pdf_path):
            num_pages += 1
        return num_pages
    except Exception as e:
        print(f"Error counting pages with pdfminer.six: {e}")
        return None


if __name__ == "__main__":
    ensure_root_cwd()

    # convert PDF
    pdf_path = f"data\\{get_date_str()}_statement.pdf"
    num_pages = count_pdf_pages(pdf_path)
    df = tabula.read_pdf(pdf_path, pages=f"2-{num_pages}", multiple_tables=False)
    df = df[0]

    # remove first 3 columns that we don't need
    df = df.iloc[:, 3:]

    # set column headers
    df.columns = ["Particulars", "Debits"]

    # basic data cleaning
    df = df[df["Debits"].notnull()]
    df = df[df["Particulars"].notnull()]
    df.drop(df[df["Debits"].str.contains("CR")].index, inplace=True)

    # save as csv
    df.to_csv(f"data\\{get_date_str()}.csv", index=False)
