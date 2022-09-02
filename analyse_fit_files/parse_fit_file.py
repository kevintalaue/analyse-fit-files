import pandas as pd

from tqdm import tqdm

from fitparse import FitFile as ffp


def get_fit_file_data(path_to_file):
    """
    this function will read in a fit file
    get the data and make it into a dataframe
    options:
        path_to_file: str
            file path for fit file
    returns:
        ff_data: dataframe
            dataframe of parsed fit file data
    """
    file = ffp(path_to_file)
    recordings = []

    for record in tqdm(file.get_messages("record")):
        temporary_dataframe = pd.DataFrame(record.as_dict()["fields"])
        temporary_dataframe["column_label"] = (
            temporary_dataframe["name"].astype(str)
            + "_"
            + temporary_dataframe["units"].astype(str)
        )
        column_names = temporary_dataframe["column_label"].to_list()
        temporary_dataframe = temporary_dataframe[["value"]].transpose()
        temporary_dataframe.columns = column_names
        temporary_dataframe["timestamp_None"] = pd.to_datetime(
            temporary_dataframe["timestamp_None"]
        )
        recordings.append(temporary_dataframe)

    fit_file_dataframe = pd.concat(recordings).reset_index(drop=True)
    return fit_file_dataframe


def get_latest_minimum_timestamp(list_of_fit_file_dataframes):
    """
    this function will go through the dataframe
    list and get the minimum timestamps for each dataframe
    and return the latest timestamp such that all the dataframes
    will be filtered at the same timestamp
    options:
        list_of_fit_file_dataframes: list
            list of dataframes
    returns:
        latest_minimum_timestamp: timestamp
            timestamp in the format from the original
            dataframe
    """
    list_of_minimum_timestamps = [
        dataframe["timestamp_None"].min() for dataframe in list_of_fit_file_dataframes
    ]
    latest_minimum_timestamp = max(list_of_minimum_timestamps)
    return latest_minimum_timestamp


def get_earliest_maximum_timestamp(list_of_fit_file_dataframes):
    """
    this function will go through the dataframe
    list and get the maximum timestamps for each dataframe
    and return the earliest timestamp such that all the dataframes
    will be filtered at the same timestamp
    options:
        list_of_fit_file_dataframes: list
            list of dataframes
    returns:
        earliest_maximum_timestamp: timestamp
            timestamp in the format from the original
            dataframe
    """
    list_of_maximum_timestamps = [
        dataframe["timestamp_None"].max() for dataframe in list_of_fit_file_dataframes
    ]
    earliest_maximum_timestamp = min(list_of_maximum_timestamps)
    return earliest_maximum_timestamp


def filter_dataframe_on_timestamps(
    fit_file_dataframe,
    minimum_timestamp,
    maximum_timestamp,
):
    """
    this function will filter a dataframe
    on certain timestamps
    options:
        fit_file_dataframe: dataframe
            dataframe to filter
        minimum_timestamp: timestamp
            start timestamp to filter the dataframe
        maximum_timestamp: timestamp
            end timestamp to filter the dataframe
    returns:
        filtered_fit_file_dataframe: dataframe
            dataframe filtered on the start and end
            timestamps
    """
    filtered_fit_file_dataframe = fit_file_dataframe[
        (fit_file_dataframe["timestamp_None"] >= minimum_timestamp)
        & (fit_file_dataframe["timestamp_None"] <= maximum_timestamp)
    ]
    return filtered_fit_file_dataframe


def compare_fit_file_dataframes(fit_file_dataframe_list):
    """
    this function will take a list of dataframes
    and filter them on certain timestamps such that
    the dataframes start and end at the same time
    to compare the data
    options:
        fit_file_dataframe_list: list
            list of dataframes to filter
    returns:
        fit_file_dataframe_list_to_compare: list
            filtered list of dataframes to filter
    """
    retrieved_minimum_timestamp = get_latest_minimum_timestamp(
        list_of_fit_file_dataframes=fit_file_dataframe_list
    )
    retrieved_maximum_timestamp = get_earliest_maximum_timestamp(
        list_of_fit_file_dataframes=fit_file_dataframe_list
    )
    fit_file_dataframe_list_to_compare = []
    for file in fit_file_dataframe_list:
        file = filter_dataframe_on_timestamps(
            fit_file_dataframe=file,
            minimum_timestamp=retrieved_minimum_timestamp,
            maximum_timestamp=retrieved_maximum_timestamp,
        )
        fit_file_dataframe_list_to_compare.append(file)
    return fit_file_dataframe_list_to_compare


def top_average_over_time(fit_file_dataframe, signal):
    """
    this function will find the top average for the signal
    over the time in seconds for the duration of the fit file
    options:
        fit_file_dataframe: dataframe
            dataframe to find top average over time
    returns:
        top_average_over_time_dataframe: dataframe
            top average over time dataframe
    """
    duration_in_seconds = int(
        (
            fit_file_dataframe["timestamp_None"].max()
            - fit_file_dataframe["timestamp_None"].min()
        ).total_seconds()
    )
    top_average = []
    for second in range(1, duration_in_seconds + 1):
        top = (
            fit_file_dataframe.rolling(window=f"{second}s", on="timestamp_None")[signal]
            .mean()
            .max()
        )
        top_average.append(
            {
                "timestamp_None": second,
                signal: top,
            }
        )

    top_average_over_time_dataframe = pd.DataFrame(top_average)
    return top_average_over_time_dataframe
