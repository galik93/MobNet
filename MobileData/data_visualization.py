import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
import folium
from folium.plugins import HeatMap, HeatMapWithTime



def plot_throughput_vs_time(df_download, df_upload, date, time_down_col, time_upl_col, tp_col):
    
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
    
    # Sort the sampled and filtered DataFrame by the time_col column in ascending order
    sampled_filtered_df_down = sampled_filtered_df_down.sort_values(by='timestamp')
    sampled_filtered_df_upl = sampled_filtered_df_upl.sort_values(by='timestamp')
    
    
    # Combine download and upload data and add category column
    combined_data = pd.concat([sampled_filtered_df_down.assign(category='download'), 
                               sampled_filtered_df_upl.assign(category='upload')])
    
    # Create a hue column combining category and operator
    combined_data['hue'] = combined_data['category'] + ' - ' + combined_data['operator']
    
    color_dict = {
    'download - o2': 'darkblue',
    'upload - o2': 'lightblue',
    'download - telekom': 'darkgreen',
    'upload - telekom': 'lightgreen',
    'download - vodafone': 'darkred',
    'upload - vodafone': 'lightcoral'
    }
    
    ax = sns.lineplot(data=combined_data,
                      x='timestamp', y=tp_col, hue='hue', palette=color_dict, hue_order=list(color_dict.keys()))
    ax.set(xlabel='Date', ylabel='Throughput (Mbps)', title=f'Download and Upload Throughput vs Time on {date}')
    
    
    fig = plt.gcf()
    fig.set_size_inches(12, 12)
    
    plt.savefig(f'plots/rest/download_upload_throughput_{date}')
    plt.clf()


def plot_geographical_heatmap(df, name):
    
    # Create a map centered on the mean of latitude and longitude values
    center_lat = df['latitude'].mean()
    center_long = df['longitude'].mean()
    
    heatmap_map = folium.Map(location=[center_lat, center_long], zoom_start=12)
    
    # Create a heatmap layer using the throughput values and lat/long coordinates
    heatmap_data = df[['latitude', 'longitude', 'tp_cleaned']].astype(float).values.tolist()
    HeatMap(data=heatmap_data, radius=8, max_zoom=13).add_to(heatmap_map)
    
    heatmap_map.save(f'plots/rest/geographical_heatmap_{name}.html')

def plot_all_cellids_heatmap(df_download, df_upload, time_down_col, time_upl_col):
    
    df_download = df_download.rename(columns={time_down_col: 'timestamp'})
    df_upload = df_upload.rename(columns={time_upl_col: 'timestamp'})
    
    df_concat = pd.concat([df_download, df_upload])
    
    df_concat['timestamp'] = pd.to_datetime(df_concat['timestamp']).dt.floor('S')
    grouped_df = df_concat.groupby(['timestamp', 'latitude', 'longitude', 'cellid'])['speed'].mean().reset_index()
    
    # Create a map centered on the mean of the latitude and longitude values
    center_lat = df_concat['latitude'].mean()
    center_long = df_concat['longitude'].mean()
    heatmap_map = folium.Map(location=[center_lat, center_long], zoom_start=13)
    
    unique_timestamps = grouped_df['timestamp'].unique()
    heatmap_data = []

    for timestamp in unique_timestamps:
        timestamp_df = grouped_df[grouped_df['timestamp'] == timestamp]
        locations_weights = timestamp_df[['latitude', 'longitude', 'speed']].values.tolist()
        heatmap_data.append(locations_weights)
    
    heatmap_layer = HeatMapWithTime(heatmap_data, auto_play=True, max_opacity=0.5, min_speed=5, max_speed=60, radius=100, use_local_extrema=False,)
    
    # Add the HeatMap object to the map
    heatmap_layer.add_to(heatmap_map)
    
    # Save the map as an HTML file
    heatmap_map.save(f'plots/rest/geo_heatmap_all_cellids.html')  

def plot_signal_strength_vs_time(df_download, df_upload, date, time_down_col, time_upl_col, rsrq_col, rsrp_col, rssi_col):
    
    color_dict = {
        'download - rsrq': 'darkblue',
        'upload - rsrq': 'lightblue',
        'download - rsrp': 'darkgreen',
        'upload - rsrp': 'lightgreen',
        'download - rssi': 'darkred',
        'upload - rssi': 'lightcoral'
    }
    
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
    
    # Prepare the data for plotting by adding new column
    sampled_filtered_df_down['type'] = 'download'
    sampled_filtered_df_upl['type'] = 'upload'
    combined_data = pd.concat([sampled_filtered_df_down, sampled_filtered_df_upl])
    
    # Create a hue column combining type and metric
    for col in [rsrq_col, rsrp_col, rssi_col]:
        combined_data[f'{col}_hue'] = combined_data['type'] + ' - ' + col

    # Create the plot
    plt.figure(figsize=(12, 6))
    for col in [rsrq_col, rsrp_col, rssi_col]:
        for tp in ['download', 'upload']:
            sns.lineplot(data=combined_data[combined_data['type'] == tp], x='timestamp', y=col, hue=f'{col}_hue', palette=color_dict, hue_order=list(color_dict.keys()), legend=False)
    
    # Customize the plot
    plt.xlabel('Time')
    plt.ylabel('Signal Strength (dBm)')
    plt.title(f'Signal Strength Metrics vs Time (Download & Upload) on {date}')

    # Update the lineplot call
    sns.lineplot(data=combined_data, x='timestamp', y=col, hue=f'{col}_hue', palette=color_dict, hue_order=color_dict.keys(), legend='brief')

    # Set legend title
    plt.legend(title='Dataset & Metrics', loc='upper right')

    plt.yscale("symlog")  # Change y-axis scale to logarithmic
    plt.savefig(f'plots/rest/signal_strength_metrices_vs_time_{date}')
    plt.clf()
    
if __name__ == "__main__":
    
    # Plot Throughput vs Time for download dataset
    preprocessed_download = pd.read_csv("data/preprocessed/all_download_nexus5x_preprocessed.csv", parse_dates=['chipsettime'])
    preprocessed_upload = pd.read_csv("data/preprocessed/all_upload_nexus5x_preprocessed.csv", parse_dates=['qualitytimestamp'])
    
    # Plot Throughput vs time for both download and upload dataset, separately for each day. Data is shown separately for each operator
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-06', 'chipsettime','qualitytimestamp', 'tp_cleaned')
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-07', 'chipsettime','qualitytimestamp', 'tp_cleaned')
    plot_throughput_vs_time(preprocessed_download, preprocessed_upload,'2018-04-08', 'chipsettime','qualitytimestamp', 'tp_cleaned')
    
    # Plot geograpical heatmap
    plot_geographical_heatmap(preprocessed_download,'download')
    plot_geographical_heatmap(preprocessed_upload,'upload')
    
    # Plot geographical heatmap for all cellid changing location over time.
    plot_all_cellids_heatmap(preprocessed_download, preprocessed_upload, 'chipsettime','qualitytimestamp')
    
    # Plot signal strength vs time of each day
    plot_signal_strength_vs_time(preprocessed_download, preprocessed_upload, '2018-04-06' , 'chipsettime','qualitytimestamp', 'rsrq', 'rsrp', 'rssi')
    plot_signal_strength_vs_time(preprocessed_download, preprocessed_upload, '2018-04-07' , 'chipsettime','qualitytimestamp', 'rsrq', 'rsrp', 'rssi')
    plot_signal_strength_vs_time(preprocessed_download, preprocessed_upload, '2018-04-08' , 'chipsettime','qualitytimestamp', 'rsrq', 'rsrp', 'rssi')