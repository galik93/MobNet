import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_throughput_vs_time(df_download, df_upload, date, time_down_col, time_upl_col, tp_col, title):
    
    sns.set_style("darkgrid")
    plt.figure(figsize=(10, 6))
    
    df_download = df_download.rename(columns={time_down_col: 'timestamp'})
    df_upload = df_upload.rename(columns={time_upl_col: 'timestamp'})
    
    
    # Convert timestamp values to datetime objects
    df_download['timestamp'] = pd.to_datetime(df_download['timestamp']).dt.floor('H')
    df_upload['timestamp'] = pd.to_datetime(df_upload['timestamp']).dt.floor('H')
    
    # Filter the dataframe to only include rows within the date range
    filtered_df_down = df_download[df_download['timestamp'].dt.date == pd.to_datetime(date).date()].copy()
    filtered_df_upl = df_upload[df_upload['timestamp'].dt.date == pd.to_datetime(date).date()].copy()
    
    # Format the time column to display only the year, month, day, and hour
    filtered_df_down.loc[:, 'timestamp'] = filtered_df_down['timestamp'].dt.strftime('%Y-%m-%d %H h')
    filtered_df_upl.loc[:, 'timestamp'] = filtered_df_upl['timestamp'].dt.strftime('%Y-%m-%d %H h')
    
    # Use random sampling to randomly sample n rows from the dataframe
    sample_size_down = int(0.25 * filtered_df_down.shape[0]) # Set as 25% for the filtered dataset
    sample_size_upl = int(0.25 * filtered_df_upl.shape[0]) # Set as 25% for the filtered dataset
    
    sampled_filtered_df_down = filtered_df_down.sample(n=sample_size_down)
    sampled_filtered_df_upl = filtered_df_upl.sample(n=sample_size_upl)
    
    # # Sort the sampled and filtered DataFrame by the time_col column in ascending order
    sampled_filtered_df_down = sampled_filtered_df_down.sort_values(by='timestamp')
    sampled_filtered_df_upl = sampled_filtered_df_upl.sort_values(by='timestamp')
    
    
    ax = sns.lineplot(data=pd.concat([sampled_filtered_df_down.assign(category='download'), 
                                  sampled_filtered_df_upl.assign(category='upload')]),
                  x='timestamp', y=tp_col, hue='category', palette=['blue', 'orange'])
    ax.set(xlabel='Date', ylabel='Download and Upload Throughput (Mbps)', title=title)
    
    
    fig = plt.gcf()
    fig.set_size_inches(12, 12)
    
    plt.savefig(f'plots/rest/download_upload_throughput_{date}')
    plt.clf()


if __name__ == "__main__":
    # Plot Throughput vs Time for download dataset
    preprocessed_download = pd.read_csv("data/preprocessed/all_download_nexus5x_preprocessed.csv", parse_dates=['chipsettime'])
    preprocessed_upload = pd.read_csv("data/preprocessed/all_upload_nexus5x_preprocessed.csv", parse_dates=['qualitytimestamp'])
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-06', 'chipsettime','qualitytimestamp', 'tp_cleaned', "Download and Upload Throughput vs Time")
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-07', 'chipsettime','qualitytimestamp', 'tp_cleaned', "Download and Upload Throughput vs Time")
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-08', 'chipsettime','qualitytimestamp', 'tp_cleaned', "Download and Upload Throughput vs Time")
