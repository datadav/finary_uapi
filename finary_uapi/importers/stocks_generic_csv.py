import csv
import sys
import pandas as pd


# "isin_code", "description","quantity","price","currency"
def import_stocks_generic_csv(filename: str):
    stocks_df = pd.read_csv(filename).dropna(subset=["ISIN"])
    stocks_df["isin_code"] = stocks_df["ISIN"]
    stocks_df["currency"] = "USD"
    stocks_df["description"] = ""
    stocks_df["quantity"] = stocks_df["Shares"]
    stocks_df["price"] = stocks_df["Cost (Per Share)"].apply(lambda row: float(row.replace("$", "")))
    print(stocks_df[["description", "isin_code", "quantity", "price", "currency"]].to_dict(
        orient="records"
    ))
    return stocks_df[["description", "isin_code", "quantity", "price", "currency"]].to_dict(
        orient="records"
    )


def import_stocks_generic_csv_deprecated(filename: str):
    results = []
    with open(filename, newline="") as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        if has_header:
            next(csv_reader)
        for row in csv_reader:
            isin_code = row[0]
            description = row[1]
            quantity = row[2]
            price = row[3]
            currency = row[3]
            results.append(
                {
                    "description": description,
                    "isin_code": isin_code,
                    "quantity": quantity,
                    "price": price,
                    "currency": currency,
                }
            )

    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    args = sys.argv[1:]
    result = import_stocks_generic_csv(args[0])
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
