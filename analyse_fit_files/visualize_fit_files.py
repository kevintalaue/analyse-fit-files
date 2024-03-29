import matplotlib.pyplot as plt

from analyse_fit_files.parse_fit_file import compare_fit_file_dataframes


def plot_fit_file_data(dataframe_to_plot):
    """
    this function will plot fit file data
    options:
        dataframe_to_plot: dataframe
            dataframe to plot
    returns:
        None
    """
    for signal in dataframe_to_plot.columns[1:]:
        try:
            plt.figure(figsize=(20, 5))
            plot_title = signal
            plt.title(plot_title)
            plt.xlim(
                dataframe_to_plot["timestamp_None"].min(),
                dataframe_to_plot["timestamp_None"].max(),
            )
            plt.plot(
                dataframe_to_plot["timestamp_None"],
                dataframe_to_plot[signal],
                label=dataframe_to_plot[signal].mean(),
            )
            plt.legend(loc="upper right")
        except KeyError:
            pass


def line_plot_compare(
    dataframe_list_to_compare,
    signal,
):
    """
    this function will produce a line plot
    of the fit file data signal on the
    same axis to compare
    options:
        dataframe_to_plot: dataframe
            dataframe to plot
    returns:
        None
    """
    dataframe_list = compare_fit_file_dataframes(
        dataframe_list_to_compare,
    )
    plt.figure(figsize=(20, 5))
    for df in dataframe_list:
        plt.plot(
            df["timestamp_None"],
            df[signal],
            label=df[signal].mean(),
            alpha=0.5,
        )
    plt.title(signal)
    plt.legend(loc="upper right")
    plt.ylabel(signal.split("_")[1])
    plt.xlabel("timestamp")


def histogram_compare(
    dataframe_list_to_compare,
    signal,
):
    """
    this function will produce a histogram
    plot of the fit file data signal on the
    same axis to compare
    options:
        dataframe_to_plot: dataframe
            dataframe to plot
    returns:
        None
    """
    dataframe_list = compare_fit_file_dataframes(
        dataframe_list_to_compare,
    )
    plt.figure(figsize=(20, 5))
    for df in dataframe_list:
        plt.hist(
            x=df[signal],
            label=df[signal].mean(),
            alpha=0.5,
        )
    plt.title(signal)
    plt.legend(loc="upper right")
    plt.xlabel(signal.split("_")[1])
