import os
import pandas as pd

from void_code.cleaner import Cleaner

DATA_DIR = "data"

def main():
    # Load
    data = pd.read_excel(os.path.join(DATA_DIR, "logTest.xlsx"), na_values="?")

    # 1. Drop columns with identical values
    data = Cleaner.dropColumnsWithIdenticalValues(data)

    # 2. Drop the "address" because of strange meaning (contains only values 1 and 2)
    data = Cleaner.dropColumns(data, ["address"])

    # 3. Drop columns with multiple missing values and a nontrivial generation method
    data = Cleaner.dropColumns(data, ["bStep", "availability"])

    # 4. Tokenize the "order" column
    data["order"] = data["order"].map({"y": 1, "n": 0})

    # 5. Drop rows where "cSumPrice" and "bSumPrice" is null
    data = data.dropna(subset=["cSumPrice", "bSumPrice"], how="all")

    # 6. Fulfill remaining empty basket columns ("bMinPrice", "bMaxPrice", "bSumPrice") with 0
    Cleaner.fillnaColumns(data, ["bMinPrice", "bMaxPrice", "bSumPrice"], 0)

    # 7. Average the rows based on "sessionNo" add a column with the number of averaged rows
    data = Cleaner.meanGroupBy(data, "sessionNo", "numberOfOrders")

    # 8. Split orders into done by registered customers and guests
    customers = data.loc[data["customerNo"].notna()]
    guests = data.loc[data["customerNo"].isna()]

    # 8.a. Drop "customerNo" in customers' orders
    customers = Cleaner.dropColumns(customers, ["customerNo"])

    # 8.b. Drop columns related to customer in guests' orders
    guests = Cleaner.dropColumns(
        guests,
        ["customerNo", "maxVal", "customerScore", "accountLifetime", "payments", "age", "lastOrder"]
    )

    # Save
    customers.to_excel(os.path.join(DATA_DIR, "logTest_customers.xlsx"))
    guests.to_excel(os.path.join(DATA_DIR, "logTest_guests.xlsx"))

if __name__ == "__main__":
    main()
