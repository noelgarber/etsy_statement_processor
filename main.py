# This is a simple script for organizing Etsy statements into more Excel-friendly spreadsheets

import os
import numpy as np
import pandas as pd

def convert_vals(series, currency_symbol = "$"):
    vals = []
    for val_text in series:
        if val_text == "--":
            val = 0.0
        elif currency_symbol in val_text and val_text[0] != "-":
            val = float(val_text.split(currency_symbol)[1])
        elif currency_symbol in val_text and val_text[0] == "-":
            val = -1 * float(val_text.split(currency_symbol)[1])
        else:
            val = np.nan
        vals.append(val)
    vals = np.array(vals)
    return vals

csv_paths = []
while True:
    path = input("Enter path to next monthly statement CSV file; hit enter when done:  ")
    if path == "":
        break
    else:
        csv_paths.append(path)

dfs = []
for path in csv_paths:
    df = pd.read_csv(path)
    dfs.append(df)

output_df = pd.concat(dfs)
cols = list(output_df.columns)

listing_numbers = ["" for i in np.arange(len(output_df))]
order_numbers = ["" for i in np.arange(len(output_df))]
transaction_numbers = ["" for i in np.arange(len(output_df))]
for i, item in enumerate(output_df["Info"]):
    item = str(item)
    if "listing: " in item:
        listing_numbers[i] = item.split("listing: ")[1]
    elif "Listing #" in item:
        listing_numbers[i] = item.split("Listing #")[1]
    elif "auto-renew sold : " in item:
        listing_numbers[i] = item.split("auto-renew sold : ")[1]
    elif "Order #" in item:
        order_numbers[i] = item.split("Order #")[1]
    elif "order: " in item:
        order_numbers[i] = item.split("order: ")[1]
    elif "transaction: " in item:
        transaction_numbers[i] = item.split("transaction: ")[1]
    elif "transaction credit: " in item:
        transaction_numbers[i] = item.split("transaction credit: ")[1]

output_df["Listing"] = listing_numbers
output_df["Order #"] = order_numbers
output_df["Transaction #"] = transaction_numbers
cols = cols[0:4] + ["Listing", "Order #", "Transaction #"] + cols[4:]
output_df = output_df[cols]

currency_symbol = "$"
output_df["Amount"] = convert_vals(output_df["Amount"], currency_symbol)
output_df["Fees & Taxes"] = convert_vals(output_df["Fees & Taxes"], currency_symbol)
output_df["Net"] = convert_vals(output_df["Net"], currency_symbol)

save_folder = input("Done; please enter a folder to save to:  ")
save_path = os.path.join(save_folder, "processed_etsy_statements.csv")

output_df.to_csv(save_path)