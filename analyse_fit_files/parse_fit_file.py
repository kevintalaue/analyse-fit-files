from fitparse import fp
import pandas as pd


def parse_fit_file(path_to_file):
    file = fp(path_to_file)
    recordings = []

    for record in file.get_messages("record"):
        df = pd.DataFrame(record.as_dict()["fields"])
        df["col_lab"] = df["name"].astype(str) + "_" + df["units"].astype(str)
        cols = df["col_lab"].to_list()
        df = df[["value"]].transpose()
        df.columns = cols
        recordings.append(df)

    return pd.concat(recordings).reset_index(drop=True)


def main():
    parse_fit_file(path_to_file=input())


if __name__ == "__main__":
    main()
