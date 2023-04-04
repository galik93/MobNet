import pandas as pd

class Cleaner:

    def meanGroupBy(df: pd.DataFrame, label: str, newLabel: str) -> pd.DataFrame:
        df_grouped = df.groupby(label, as_index=False)
        df = df_grouped.mean()
        df[newLabel] = df_grouped.size()["size"]
        df = Cleaner.dropColumns(df, label)
        return df

    def fillnaColumns(df: pd.DataFrame, labels: list[str], value: any):
        for l in labels:
            df[l] = df[l].fillna(value)

    def dropColumnsWithIdenticalValues(df: pd.DataFrame) -> pd.DataFrame:
        return df[[column for column in df if df[column].nunique() > 1]]

    def dropColumns(data: pd.DataFrame, labels: list[str]) -> pd.DataFrame:
        return data.drop(labels, axis="columns")

    # Diagnostic functions

    def displayDistinctValues(df: pd.DataFrame, labels: list[str]) -> pd.DataFrame:
        for l in labels:
            print(df.groupby(l).size(), "\n")
