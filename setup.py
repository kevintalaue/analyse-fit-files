from setuptools import find_packages, setup

from analyse_fit_files import __version__

setup(
    name="analyse-fit-files",
    packages=find_packages(exclude=["tests"]),
    version=__version__,
    description="this repo is for parsing fit files and visualizing the data and getting statistics more than Strava provides",
    url="https://github.com/kevintalaue/analyse-fit-files",
    author="kevin_talaue",
    author_email="kevintalaue@hotmail.com",
)
