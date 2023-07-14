# How do I run the backend? #
```main.py``` is the entry point for the backend. <br> 
* To run the static analysis, use ``` python main.py -s <path to program directory> ``` from the command line in the \\backend directory. Make sure that the last slash in the directory path is escaped. Ex. ```samplecode\test\\```. <br>
* To run the dynamic analysis, use ``` python main.py -d <path to program directory> <path to program entry point file> <cmdArgs>```, where ```<cmdArgs>``` is an arbitrary list of command line arguments for the target program, separated by spaces.

## Required Packages ##
The following packages are necessary:
* Numpy (https://numpy.org/install/)
* Pandas (https://pandas.pydata.org/docs/getting_started/install.html#installing-from-pypi)
* Matplotlib.pyplot (https://matplotlib.org/stable/users/installing/index.html)

## Usage ##
You will first need to open up the react portion of this project. To do so, visit [here](https://github.students.cs.ubc.ca/CPSC410-2022W-T1/Project2Group8/blob/backend/frontend/README.md). <br>
Return to the command line and run a static or dynamic analysis following the instructions above. After you have verified that it has completed, go back to the frontend web page and click on "Update" to fetch the results of your analysis.
