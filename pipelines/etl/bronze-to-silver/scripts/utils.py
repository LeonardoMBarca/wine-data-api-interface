import os
import pandas as pd
from unicodedata import normalize

def standardize_dataframe(df, standardize_dict):
    """
    Standardizes the DataFrame by converting all string values to lowercase,
    renaming columns to lowercase, and applying a set of regex replacements.

    Parameters:
        df (pd.DataFrame): The input DataFrame to be standardized.
        standardize_dict (dict): Dictionary of regex patterns and their replacements.

    Returns:
        pd.DataFrame: The standardized DataFrame.
    """
    df = df.apply(lambda x: x.astype(str).str.lower())
    df.columns = map(str.lower, df.columns)
    df = df.replace(to_replace=standardize_dict, regex=True)

    return df

def accent_remove(text):
    """
    Removes accents from a given string using Unicode normalization.

    Parameters:
        text (str): The input string with potential accented characters.

    Returns:
        str: The unaccented version of the input string.
    """
    return normalize("NFKD", text).encode("ASCII", "ignore").decode(("ASCII"))