import pandas as pd
from thefuzz import fuzz
from thefuzz import process

df_customers = pd.read_csv('customers.csv')
df_transactions = pd.read_csv('transactions.csv')

customer_names = df_customers['customer_name'].tolist()
transaction_names = df_transactions['customer_name'].tolist()

#Considering a threshold of 90% for matching names
def match_names(name, list_of_names, threshold=90):
    match = process.extractOne(name, list_of_names, scorer=fuzz.token_sort_ratio)
    if match[1] >= threshold:
        return match[0]
    else:
        return None

df_customers['matched_name'] = df_customers['customer_name'].apply(lambda x: match_names(x, transaction_names))

merged_df = pd.merge(df_customers, df_transactions, left_on='matched_name', right_on='customer_name', how='inner')

renamed_df = merged_df[['customer_id', 'customer_name_x', 'email', 'transaction_id', 'amount', 'transaction_date']].rename(columns={
    'customer_name_x': 'customer_name'
})

renamed_df.to_csv('consolidated_dataset.csv', index=False)
