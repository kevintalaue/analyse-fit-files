import matplotlib.pyplot as plt

from analyse_fit_files.parse_fit_file import compare_fit_file_dataframes


def plot_fit_file_data(
    dataframe_to_plot,
    datasource,
):
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
            plot_title = signal.replace("_", " ").title()
            plt.title(plot_title)
            plt.xlim(
                dataframe_to_plot["timestamp_None"].min(),
                dataframe_to_plot["timestamp_None"].max(),
            )
            plt.plot(
                dataframe_to_plot["timestamp_None"],
                dataframe_to_plot[signal],
                label=f"{datasource} {dataframe_to_plot[signal].mean()}",
            )
            plt.legend(loc="upper right")
        except KeyError:
            pass


def line_plot_compare(
    dataframe_list_to_compare,
    datasource_list,
    signal,
):
    """
    this function will produce a line plot
    of the fit file data signal on the
    same axis to compare
    options:
        dataframe_list_to_compare: list
            list of the dataframe objects to compare and plot
        datasource_list: list
            list of the device name or name of the source of the data 
        signal: str
            signal to compare and plot
    returns:
        None
    """
    dataframe_list = compare_fit_file_dataframes(
        dataframe_list_to_compare,
    )
    plt.figure(figsize=(40, 10))
    for loc, df in enumerate(dataframe_list):
        plt.plot(
            df["timestamp_None"],
            df[signal],
            label=f"{datasource_list[loc]} {round(df[signal].mean(), 2)} avg",
            alpha=0.5,
        )
        ymax = df[signal].max()
        xpos = df.loc[df[signal] == ymax, "timestamp_None"].index[0]
        xmax = df["timestamp_None"][xpos]
        plt.title(signal.replace("_", " ").title())
        plt.legend(loc="lower right")
        plt.annotate(text=f'{datasource_list[loc]} {ymax} max', xy=(xmax, ymax), xytext=(xmax, ymax+1))
        plt.ylabel(signal.split("_")[-1:][0])
        plt.xlabel("timestamp")


def histogram_compare(
    dataframe_list_to_compare,
    datasource_list,
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
    for loc, df in enumerate(dataframe_list):
        plt.hist(
            x=df[signal],
            label=f"{datasource_list[loc]} {df[signal].mean()}",
            alpha=0.5,
        )
    plt.title(signal.replace("_", " ").title())
    plt.legend(loc="upper right")
    plt.xlabel(signal.split("_")[-1:][0])
