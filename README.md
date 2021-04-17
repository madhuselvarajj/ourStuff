# ourStuff

## Summary

This is the executive summary of our project.


## Getting started

  Please begin by cloning this repository. You can download it as a Zip file from https://github.com/stephanedorotich/ourStuff or you can use the following command:
  ```
  git clone https://github.com/stephanedorotich/ourStuff.git
  ```
  You will need Python v3.0 or above and PIP (a package manager for Python). Python is necessary to run our project and PIP will be used to install the project's dependencies.  

### Getting Python3

  Check your current version of Python and Pip by executing the following using your Command Prompt or Terminal
  ```
  python --version
  pip --version
  ```
  If you do not have Python v3.0 or above, please install it. [This guide](https://realpython.com/installing-python/) will help with installation. Pip is a package manager bundled with Python. If it is not installed, [this guide](https://pip.pypa.io/en/stable/installing/) will help with installation.

### Project Dependencies

  To install project dependencies, please run the following command
  
  If using Command Prompt:
  ```
  pip install e .
  ```
  
  If using Terminal:
  ```
  python -m pip install e .
  ```

### Running the Webapp

To run the app, execute the following command

```
python OurStuff.py
```

Once the flask app starts running, a private IP address will be printed to your console. Please copy & paste the IP address to your favorite browser.
The IP address should look like this: ```http://127.0.0.1/5000/```. Have fun using our app!

## The Repository

<details>
  <summary>Folders</summary>

#### Scripts
The scripts folder contains scripts for creating and restoring our database

#### Static
The static folder contains our webapp's static css stylesheet

#### Templates
The templates folder our webapp's html documents
</details>

<details>
  <summary>Files</summary>
  
Filename | Description
----- | -----
admin.py | API for Admin functionality
auth.py | API for authenticating users
db.py | for opening and closing connection to our db
forms.py | WTForm definitions
ourStuff.db | Our SQLite3 database file
OurStuff.py | API
setup.py | Python script to make project "pip installable"
</details>

## Developer tools

Two scripts are provided for saving & reseting the database state. This gives developers the freedom to experiment with the data while maintaining a common starting point for all team members.

Using the Command Prompt or Terminal, navigate to the project folder.

To reset the database to its default state, execute
```
python3 scripts/reset.py
```
This will recreate the database and populate it using 'scripts/populate_db.sql'

To update the default state to the current state, execute
```
python3 scripts/save.py
```
This will save the current database state to 'scripts/populate_db.sql'
