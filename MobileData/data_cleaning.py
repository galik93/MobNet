import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple, List, Union

def read_data(files: List[str]) -> List[pd.DataFrame]:
    dataframes = []
    for file in files:
        operator = file.split('/')[-1].split('_')[0].lower()  # Extract the operator's name from the filename
        df = pd.read_csv(file)
        df['operator'] = operator  # Add a new column with the operator's name
        dataframes.append(df)
    return dataframes

def visualize_outliers(data: pd.DataFrame, numerical_cols: List[str]) -> None:
    # Get the columns with outliers
    outliers = identify_outliers_zscore(data[numerical_cols]) 
    outlier_cols = outliers.any()
    data_name = ''
    if data.shape[1] == 24:
        data_name = 'download'
    else: data_name = 'upload'

    # Create a box plot for each numerical column with outliers
    for col in outlier_cols.index[outlier_cols]:
        sns.boxplot(x=data[col])
        plt.title(f'Box plot for {col} column with outliers')
        plt.savefig(f'plots/outliers/{data_name}/{col} with outliers')
        plt.clf()
        
    data = data[~outliers.any(axis=1)] # Remove outliers from the dataframe
    
    # Create a box plot for each numerical column with removed outliers
    for col in outlier_cols.index[outlier_cols]:
        sns.boxplot(x=data[col])
        plt.title(f'Box plot for {col} column with removed outliers')
        plt.savefig(f'plots/outliers/{data_name}/{col} with removed outliers')
        plt.clf()

def identify_outliers_zscore(data: pd.DataFrame, threshold: Union[int, float] = 3) -> np.ndarray:
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold

def verify_columns(dataframes: List[pd.DataFrame]) -> None:
    for df in dataframes:
        print(df.shape[1])

def merge_data(download_dataframes: List[pd.DataFrame], upload_dataframes: List[pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    all_download = pd.concat(download_dataframes, ignore_index=True)
    all_upload = pd.concat(upload_dataframes, ignore_index=True)
    return all_download, all_upload

def compare_dtypes(download: pd.DataFrame, upload: pd.DataFrame) -> None:
    common_cols = set(download.columns).intersection(set(upload.columns))
    for col in common_cols:
        if download[col].dtype != upload[col].dtype:
            print(col, 'Type in download: ', download[col].dtype, 'Type in upload: ', upload[col].dtype)

def preprocess_data(data: pd.DataFrame, is_download = True) -> pd.DataFrame:
    # Check for missing or null values in the dataframe
    print(data.isnull().sum())

    # Remove duplicates
    print("Number of duplicate rows:", data.duplicated().sum()) # Check for duplicate rows in the dataframe
    data.drop_duplicates(inplace=True) # Drop duplicate rows from the dataframe

    # Outliers detecion and removal
    numerical_cols = ['mcsindex', 'tbs0', 'tbs1', 'tp_cleaned', 'scc', 'gpstime', 'longitude', 'latitude', 'speed', 'rsrq', 'rsrp', 'rssi', 'earfcn', 'cqi'] if is_download else ['mcsindex', 'tbs', 'rbs', 'tp_cleaned', 'speed', 'rsrq', 'rsrp', 'rssi', 'cqi'] # Select the numerical columns for outlier detection

    visualize_outliers(data, numerical_cols)

    # Changing formats of data types (e.g. timestamp to datetime format, int in both dataset for the same columns)
    data.iloc[:,0] = pd.to_datetime(data.iloc[:,0], unit='s', origin='unix')
    data['gpstime'] = pd.to_datetime(data['gpstime'], unit='s', origin='unix')
    data['cellid'] = data['cellid'].astype(int)
    data['earfcn'] = data['earfcn'].astype(int)

    # Count the frequency of each unique value in a column
    for col in data.columns:
        print(col)
        print(data[col].value_counts())
        
     # Check for any 'NaT (Not a Time)' values in the datetime type columns
    print(data[data.iloc[:,0].isna()]) #qualitytimestamp and #chipsettime
    print(data[data['gpstime'].isna()])

    return data

if __name__ == "__main__":
    # Define file paths for download and upload datasets
    download_dataset = [
        "data/Campaign3/o2_download_nexus5x.csv",
        "data/Campaign3/telekom_download_nexus5x.csv",
        "data/Campaign3/vodafone_download_nexus5x.csv"
    ]

    upload_dataset = [
        "data/Campaign3/o2_upload_nexus5x.csv",
        "data/Campaign3/telekom_upload_nexus5x.csv",
        "data/Campaign3/vodafone_upload_nexus5x.csv"
    ]

    # Read download and upload datasets into dataframes
    download_dataframes = read_data(download_dataset)
    upload_dataframes = read_data(upload_dataset)
    
     # Verify the number of columns in each dataset
    verify_columns(download_dataframes)
    verify_columns(upload_dataframes)

    
    # Concatenate download and upload dataframes
    all_download = pd.concat(download_dataframes, axis=0)
    all_upload = pd.concat(upload_dataframes, axis=0)

    compare_dtypes(all_download, all_upload)

    preprocessed_download = preprocess_data(all_download, is_download=True)
    preprocessed_upload = preprocess_data(all_upload, is_download=False)

    preprocessed_download.to_csv("data/preprocessed/all_download_nexus5x_preprocessed.csv", index=False)
    preprocessed_upload.to_csv("data/preprocessed/all_upload_nexus5x_preprocessed.csv", index=False)