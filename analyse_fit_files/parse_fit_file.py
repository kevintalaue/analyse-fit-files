import pandas as pd

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

    for record in file.get_messages("record"):
        temporary_dataframe = pd.DataFrame(record.as_dict()["fields"])
        temporary_dataframe["column_label"] = (
            temporary_dataframe["name"].astype(str)
            + "_"
            + temporary_dataframe["units"].astype(str)
        )
        column_names = temporary_dataframe["column_label"].to_list()
        temporary_dataframe = temporary_dataframe[["value"]].transpose()
        temporary_dataframe.columns = column_names
        recordings.append(temporary_dataframe)

    fit_file_dataframe = pd.concat(recordings).reset_index(drop=True)
    return fit_file_dataframe


def get_latest_minimum_timestamp(list_of_fit_file_dataframes):
    list_of_minimum_timestamps = [
        dataframe["timestamp_None"].min() for dataframe in list_of_fit_file_dataframes
    ]
    latest_minimum_timestamp = max(list_of_minimum_timestamps)
    return latest_minimum_timestamp


def get_earliest_maximum_timestamp(list_of_fit_file_dataframes):
    list_of_maximum_timestamps = [
        dataframe["timestamp_None"].max() for dataframe in list_of_fit_file_dataframes
    ]
    earliest_maximum_timestamp = max(list_of_maximum_timestamps)
    return earliest_maximum_timestamp


def filter_dataframe_on_timestamps(
    fit_file_dataframe, minimum_timestamp, maximum_timestamp
):
    fit_file_dataframe = fit_file_dataframe[
        (fit_file_dataframe["timestamp_None"] >= minimum_timestamp)
        & (fit_file_dataframe["timestamp_None"] <= maximum_timestamp)
    ]
    return fit_file_dataframe


def compare_fit_file_dataframes(fit_file_dataframe_list):
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
