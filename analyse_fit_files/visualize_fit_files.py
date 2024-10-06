import matplotlib.pyplot as plt
import numpy as np

from analyse_fit_files.parse_fit_file import (
    compare_fit_file_dataframes,
    decimal_time2clock_time,
    mins_per_mile_or_km,
)


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


def plot_sport_peak_curve(
    primary_fitfile_dataframe,
    primary_sport_peak_curve,
    secondary_fitfile_dataframe=None,
    secondary_sport_peak_curve=None,
    sport="running",
):
    """function to plot the peak average over time for running pace or power and heart rate
    with the ability to compare past activities

    Args:
        primary_fitfile_dataframe (dataframe): parsed fit file data from the device
        primary_sport_peak_curve (dataframe): dataframe of the peak sports metric curve over time
        secondary_fitfile_dataframe (dataframe, optional): parsed fit file data from the device. Defaults to None.
        secondary_sport_peak_curve (dataframe, optional): dataframe of the peak sports metric curve over time. Defaults to None.
        sport (str, optional): sport to plot peak curve. Defaults to "running".
    """
    # set the metric
    metric = "Pace"
    if sport == "cycling":
        metric = "Power"

    # data info
    print(
        primary_fitfile_dataframe["timestamp_None"].dt.date.unique()
    )  # primary plot date
    if secondary_fitfile_dataframe is not None:
        print(
            secondary_fitfile_dataframe["timestamp_None"].dt.date.unique()
        )  # secondary plot date

    # plot properties
    fig, ax1 = plt.subplots(figsize=(30, 10))  # make the plot
    plt.title(
        f"Peak {metric} and Heart Rate Curve",
        fontsize=40,
    )  # title the plot

    # primary plot
    sp = ax1.plot(
        primary_sport_peak_curve["timestamp_None"],
        primary_sport_peak_curve["sport_metric"],
        color="blue",
        alpha=0.8,
        linewidth=5,
        label=f'Avg Recent Pace{decimal_time2clock_time(mins_per_mile_or_km(primary_fitfile_dataframe["speed_m/s"].mean(), "km"))}',
    )  # primary plot peak sport metric curve over activity time
    if secondary_sport_peak_curve is not None:
        sp1 = ax1.plot(
            secondary_sport_peak_curve["timestamp_None"],
            secondary_sport_peak_curve["sport_metric"],
            color="blue",
            alpha=0.5,
            linewidth=5,
            label=f'Avg Past {metric}{decimal_time2clock_time(mins_per_mile_or_km(secondary_fitfile_dataframe["speed_m/s"].mean(), "km"))}',
        )  # secondary plot peak sport metric curve over activity time
    ax1.set_ylabel(f"{metric}", fontsize=20)  # set the y label for pace
    # x ticks
    x_max_t = np.max(primary_sport_peak_curve.index.max())  # total seconds in the data
    x_max_t = x_max_t / 3600  # get the hours
    x_max_t = np.floor(x_max_t)  # round downwards
    x_max_t = int(x_max_t * 3600)  # maximum amount of seconds in the data
    xlabticks = {
        "0s": 0,
        "1m": 60,
        "5m": 300,
        "10m": 600,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "2h": 7200,
        "3h": 10800,
        "4h": 14400,
        "5h": 18000,
        "6h": 21600,
        "7h": 25200,
        "8h": 28800,
        "9h": 32400,
        "10h": 36000,
        "11h": 39600,
        "12h": 43200,
        "13h": 46800,
        "14h": 50400,
        "15h": 54000,
        "16h": 57600,
        "17h": 61200,
        "18h": 64800,
        "19h": 68400,
        "20h": 72000,
        "21h": 75600,
        "22h": 79200,
        "23h": 82800,
    }  # dictionary of the x labels and ticks
    max_labels = len(
        [
            value
            for value in list(xlabticks.values())
            if value < np.max(primary_fitfile_dataframe.index.max())
        ]
    )  # number of maximum x ticks and labels for the data
    plt.xticks(
        ticks=list(xlabticks.values())[:max_labels],
        labels=list(xlabticks.keys())[:max_labels],
    )  # set the x ticks
    plt.grid()  # make a grid
    plt.xlabel(
        "Activity Time",
        fontsize=20,
    )  # x label
    if sport == "running":
        # y1 ticks
        y1labticks = [
            decimal_time2clock_time(tick) for tick in (plt.yticks()[0])
        ]  # list of y labels and ticks, make the primary y ticks into clock time
        plt.yticks(
            ticks=plt.yticks()[0],
            labels=y1labticks,
        )  # set the primary y ticks and labels

    # seondary plot
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    hr = ax2.plot(
        primary_sport_peak_curve["timestamp_None"],
        primary_sport_peak_curve["heart_rate"],
        color="red",
        alpha=0.8,
        linewidth=5,
        label=f'Avg Recent Heart Rate {primary_fitfile_dataframe["heart_rate_bpm"].mean().__round__()}',
    )  # primary plot heart rate curve over activity time
    if secondary_sport_peak_curve is not None:
        hr1 = ax2.plot(
            secondary_sport_peak_curve["timestamp_None"],
            secondary_sport_peak_curve["heart_rate"],
            color="red",
            alpha=0.5,
            linewidth=5,
            label=f'Avg Past Heart Rate {secondary_fitfile_dataframe["heart_rate_bpm"].mean().__round__()}',
        )  # secondary plot heart rate curve over activity time
    ax2.set_yticks(
        np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks()))
    )
    ax2.set_ylabel(
        "Heart Rate",
        fontsize=20,
    )  # set the y label for heart rate

    # y2 ticks
    y2labticks = [
        round(tick) for tick in (plt.yticks()[0])
    ]  # list of y labels and ticks, round the secondary y axis labels to whole numbers
    plt.yticks(
        ticks=plt.yticks()[0],
        labels=y2labticks,
    )  # set the secondary y ticks and labels

    # added these three lines
    lns = sp + hr
    if secondary_sport_peak_curve is not None:
        lns = sp + sp1 + hr + hr1  # for two plots
    labs = [l.get_label() for l in lns]
    ax2.legend(
        lns,
        labs,
        loc=0,
    )

    # show the plot
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()  # show the plot
