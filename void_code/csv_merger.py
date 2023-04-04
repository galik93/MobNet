import pandas as pd


def merge_csv_files(*csv_files, output_file='merged_file.csv'):
    dfs = []
    for file in csv_files:
        # Get operator name from file path
        operator = file.split('/')[2].split('_')[0].lower()
        df = pd.read_csv(file)
        df['operator'] = operator  # Add new column with operator name
        dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(output_file, index=False)


merge_csv_files('data/Campaign3/o2_download_nexus5x.csv', 'data/Campaign3/telekom_download_nexus5x.csv',
                'data/Campaign3/vodafone_download_nexus5x.csv', output_file='data/Campaign3/all_download_nexus5x.csv')
merge_csv_files('data/Campaign3/o2_upload_nexus5x.csv', 'data/Campaign3/telekom_upload_nexus5x.csv',
                'data/Campaign3/vodafone_upload_nexus5x.csv', output_file='data/Campaign3/all_upload_nexus5x.csv')
