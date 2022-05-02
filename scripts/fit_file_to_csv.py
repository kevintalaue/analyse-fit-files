import click

from analyse_fit_files.parse_fit_file import get_fit_file_data


def format_read_path(file_path):
    """
    this function will format the
    file path to the fit file
    options:
        file_path: str
            fit file read path
    returns:
        formatted_path: str
            formatted file path
    """
    formatted_path = file_path.replace("\\", "/")
    formatted_path = formatted_path.replace('"', "")
    return formatted_path


def generate_save_path(file_path):
    """
    this function will generate the
    file path to save the csv file
    options:
        file_path: str
            fit file read path
    returns:
        save_path: str
            generated save path
    """
    save_path = file_path.replace(".fit", ".csv")
    return save_path


@click.command(help="Convert fit file to csv file")
@click.option(
    "--path_to_fit_file",
    "-path",
    type=str,
    required=True,
    prompt=True,
    help="Path to fit file to convert",
)
def main(path_to_fit_file):
    read_file_path = format_read_path(file_path=path_to_fit_file)
    save_file_path = generate_save_path(file_path=path_to_fit_file)
    get_fit_file_data(path_to_file=read_file_path).to_csv(path_or_buf=save_file_path)


if __name__ == "__main__":
    main()
