import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_throughput_vs_time(df, time_col, tp_col, title):
    sns.set_style("darkgrid")
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=df, x=time_col, y=tp_col)
    ax.set(xlabel='Time', ylabel='Download Throughput (Mbps)', title=title)
    plt.show()


if __name__ == "__main__":
    # Plot Throughput vs Time for download dataset
    preprocessed_download = pd.read_csv("data/preprocessed/all_download_nexus5x_preprocessed.csv")
    plot_throughput_vs_time(preprocessed_download, 'chipsettime', 'tp_cleaned', "Download Throughput vs Time")
