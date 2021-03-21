# ourStuff

## Requirements
The following resources must be installed locally.

* python3
* flask (python3 library)

<details>
<summary>Set-Up Instructions for Windows</summary>
Open the Command Prompt. (by pressing the Windows Key and typing 'cmd')

### Install python3
You can check your current versions of python and pip by using the commands:
```
python --version
pip --version
```
If you do not have python 3.0 or above, please install it. [This guide](https://realpython.com/installing-python/) will help with installation.

### Install Flask
```
pip install flask
```

### SQLite
SQLite3 is installed in the standard Python3 library.

You're all set!
</details>

<details>
<summary>Resetting the Database</summary>
A few python scripts are included to help reset the database.

Using the command line, navigate to the project folder. You can now reset the database to its default state with the following command:
```
python3 scripts/resetDB.py
```
</details>

<details>
<summary>Diagrams</summary>
![Extended Entity Relationship Diagram](https://github.com/stephanedorotich/ourStuff/tree/master/resources/EERD.jpg)

![Relational Model](Relationship Diagram](https://github.com/stephanedorotich/ourStuff/tree/master/resources/RM.jpg)
</details>

## Resources
The resources folder contains files related to our design

## Scripts
The scripts folder contains files for default actions on the database
