import pandas as pd
import openpyxl
import json

# df = pd.read_csv('C:/Users/lewis.anderson/Downloads/products_13_07_2022_12_53_analysed.csv')
df = pd.read_json('26_july_22_json.json')  # , orient='feed')
# data = json.loads('26_july_22_json.json')
# result = pd.json_normalize(data)


dicts = df.iloc[0, 0]
df = pd.DataFrame(dicts['add']['items'])

a_list = ['brand',
          'color',
          'colourBase',
          'frameType',
          'frameShape',
          'frameMaterial',
          'availability',
          'availabilityHometrial',
          'gender',
          'size',
          'sellingPrice',
          'newArrivals',
          'currency',
          'boutique',
          'salePrice']

for c in df:
    df[c] = df[c].astype(str)
    df[c] = df[c].str.replace("[", "").str.replace("]", "")

new_df = pd.DataFrame()

for l in a_list:
    # print(df.value_counts(l))
    print(df[df['availability'] == 'True'].value_counts(l))
    new_cols = df[df['availability'] == 'True'].value_counts(l).reset_index()
    # print(df.value_counts(l))
    # new_cols = df.value_counts(l).reset_index()
    new_df[l] = new_cols[l]
    new_df[l + "_count"] = new_cols[0]

new_df = new_df.fillna("")
content_df = df[df['docType'] != 'product'][['uniqueId', 'articleUrl', 'title', 'description', 'tags', 'documentType', 'docType']].fillna("")
product_df = df[df['docType'] == 'product'].fillna("").drop(['articleUrl', 'tags', 'documentType'], axis=1)

with pd.ExcelWriter('unbxd_feed_summary.xlsx') as writer:
    content_df.to_excel(writer, sheet_name='content', index=False)
    product_df.to_excel(writer, sheet_name='products', index=False)
    new_df.to_excel(writer, sheet_name='summary', index=False)
