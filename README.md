# analyse-fit-files
I started out riding bikes and now I run, I am also nerd with a love for data and datascience. This repo is for parsing fit files and visualizing the data and getting statistics more than Strava provides

## Getting Started
### Linux/Mac
1. Clone this repository from the ```main``` branch
2. Using the terminal ```cd``` into the ```analyse-fit-files``` repository after it's been cloned
3. Using a terminal run the ```python -m venv env``` or ```python3 -m venv env``` command
4. Using the terminal run ```source env/bin/activate```
5. Using a terminal run the ```pip install -r requirements.txt``` command
6. Create a local ```data``` folder within your local repository

### Windows
1. Run ```pip install virtualenv``` in the command line
2. Clone this repository from the ```main``` branch
3. Using the command line ```cd``` into the ```analyse-fit-files``` repository after it's been cloned
4. Using the command line run ```virtualenv --python C:\Path\To\Python\python.exe env``` 
5. Using the command line run ```.\env\Scripts\activate``` to activate your newly created ```env```
6. Using the command line run ```pip install -r requirements.txt``` 
7. Create a local ```data``` folder within your local repository

## Convert Fit File to Csv File
Run ```python scripts/fit_file_to_csv.py```