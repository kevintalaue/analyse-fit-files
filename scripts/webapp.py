import streamlit as st
import pandas as pd

import os

import plotly.graph_objects as go

from analyse_fit_files.parse_fit_file import get_fit_file_data

# Title
st.title("Data Upload and Analysis Web App")

st.write(
    f"""
    My name is Kevin Talaue\n
    I am currently a triathlete in training who loves to program and analyze data\n
    Welcome to this open source web app that allows you to upload multiple data sources to compare fitfile data\n
    """
)

st.markdown(
    "[Click here to visit my Strava Page](https://www.strava.com/athletes/kevintalauecr)"
)
st.markdown(
    "[Click here to visit my Instagram Page](https://www.instagram.com/kevintalauecr)"
)
st.markdown(
    "[Click here to visit my Youtube Channel](https://www.youtube.com/@kevintalaueCR)"
)

# Upload file
uploaded_file = st.file_uploader(
    "Upload your data file (fit)",
    type=["fit"],
    accept_multiple_files=True,
)


def interactive_compare(dataframes, signal):
    """
    this function will take a dictionary of dataframes
    and plot it on the same axis with an interactive plot
    options:
        dataframes: dict
            dictionary of the dataframe objects to compare and plot {dataframe_name(str): dataframe(object)}
        signal: str
            signal or column to compare and plot
    returns:
        None
    """
    fig = go.Figure()  # create the figure
    for (
        device,
        data,
    ) in (
        dataframes.items()
    ):  # iterate over the dictionary of data frame objects to plot
        fig.add_trace(go.Scatter(x=data["timestamp_None"], y=data[signal], name=device))
        ymax = data[signal].max()
        xpos = data.loc[data[signal] == ymax, "timestamp_None"].index[0]
        xmax = data["timestamp_None"][xpos]
        fig.add_annotation(
            x=xmax,
            y=ymax,
            text=f'{device} {ymax} {signal.split("_")[-1:][0].title()} Max',
        )
    fig.update_layout(
        title=signal.replace("_", " ").title(),
        xaxis_title="timestamp".title(),
        yaxis_title=signal.split("_")[-1:][0].title(),
        legend_title="Device",
        hovermode="x unified",
    )

    st.plotly_chart(fig)


if uploaded_file:
    dataframe_list = {}
    # Read the uploaded file into a DataFrame
    for file in uploaded_file:
        temp_df = get_fit_file_data(file)
        dataframe_list[file.name] = temp_df
    # Create radio buttons for selection
    option = st.radio("Chose a signal", temp_df.columns)

    # Display the selected option
    st.write("You selected:", option)
    interactive_compare(dataframes=dataframe_list, signal=option)
