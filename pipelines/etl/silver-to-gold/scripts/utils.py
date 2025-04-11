import pandas as pd
import re

def split_column_value(df, column_name):
    list_column_value = []
    
    for original_value in df[column_name].unique():
        # 1. Limpeza
        clean_value = original_value.lower()
        clean_value = clean_value.replace("(", "").replace(")", "").strip("_")
        clean_value = clean_value.replace("_", " ")
        clean_value = re.sub(r'\b(de|da|do|com)\b', '_', clean_value)
        clean_value = re.sub(r'\s+', ' ', clean_value).strip()
        clean_value = clean_value.replace(" ", "_")
        clean_value = re.sub(r'_+', '_', clean_value).strip("_")

        # 2. Tokenização
        tokens = clean_value.split("_")

        # 3. Armazenar [original, [tokens]]
        list_column_value.append([original_value, tokens])
    
    return list_column_value