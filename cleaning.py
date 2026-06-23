import pandas as pd


def clean_column_names(df):
    """
    Standardize dataframe column names.
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    df.rename(columns={"st": "state"}, inplace=True)

    return df


def clean_inconsistent_values(df):
    """
    Clean inconsistent values in selected columns.
    """
    df = df.copy()

    # Clean gender values
    df["gender"] = df["gender"].replace({
        "Female": "F",
        "female": "F",
        "Femal": "F",
        "F": "F",
        "Male": "M",
        "male": "M",
        "M": "M"
    })

    # Clean state values
    df["state"] = df["state"].replace({
        "AZ": "Arizona",
        "Cali": "California",
        "WA": "Washington"
    })

    # Clean education values
    df["education"] = df["education"].replace({
        "Bachelors": "Bachelor"
    })

    # Clean customer lifetime value
    df["customer_lifetime_value"] = (
        df["customer_lifetime_value"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    # Clean vehicle class values
    df["vehicle_class"] = df["vehicle_class"].replace({
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury"
    })

    return df


def handle_missing_values(df):
    """
    Fill missing values using median for numeric columns
    and mode for categorical columns.
    """
    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(include="object").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode()[0])

    return df


def remove_duplicates(df):
    """
    Remove duplicate rows and reset the index.
    """
    df = df.copy()

    df.drop_duplicates(keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def convert_numeric_to_integer(df):
    """
    Convert all numeric columns to integers.
    """
    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].astype(int)

    return df


def main(df):
    """
    Run the full data cleaning process.
    """
    df = clean_column_names(df)
    df = clean_inconsistent_values(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_numeric_to_integer(df)

    return df