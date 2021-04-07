# ourStuff

## Summary

This is the executive summary of our project.

<details>
  <summary>Extended Entity Relationship Diagram</summary>

  ![Extended Entity Relationship Diagram](https://raw.githubusercontent.com/stephanedorotich/ourStuff/main/resources/EERD.jpg)

</details>

<details>
  <summary>Relational Model</summary>

  ![Relational Model](https://raw.githubusercontent.com/stephanedorotich/ourStuff/main/resources/RM.jpg)

</details>
  

## Getting started

After cloning this repository, please ensure you have met the requirements.

### Requirements
The following resources must be installed locally.

* Python3
* Flask
* Flask_WTF
* WTForms
* SQLite3

<details>
<summary>Set-Up Instructions for Windows</summary>

### Getting Python3

  First, lets check your current version of Python and Pip. Please execute the following in Command Prompt
  ```
  python --version
  pip --version
  ```
  If you do not have Python version 3 or above or if you don't have any version, then you need to install Python3.
  
  This guide will help with installation: https://realpython.com/installing-python/
  
  Pip is a package manager which is bundled with Python. If you have installed the latest version of Python, you should also have Pip.
  
  If Pip is not installed, this guide will help with installation: https://pip.pypa.io/en/stable/installing/
  
### Flask and WTForms
  Our system has a few dependencies. The first is Flask, which is the Python microframework we are using to develop our API. Second, we use WTForms for creating and using forms.
  Finally, we use the flask_wtf package to integrate Flask and WTForms.
  
  Please execute the following in Command Prompt to install the packages
  ```
  pip install flask
  pip install flask_wtf
  pip install WTForms
  ```
  
  Please consult the following if you would like more information on these resources.
  Name | Source
  ----- | -----
  Flask | https://flask.palletsprojects.com/en/1.1.x/
  WTForms | https://wtforms.readthedocs.io/en/2.3.x/
  Flask_wtf | https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/

### SQLite
SQLite3 is installed in the standard Python3 library.

You're all set!
</details>

### Running the Webapp

To use the ourStuff webapp, please execute the following command

```
python3 OurStuff.py
```

Once the flask app starts running, a private IP address will be printed to your console. Please copy & paste the IP address to your favorite browser.
The IP address should look like this: ```http://127.0.0.1/5000/```. Have fun using our app!

## The Repository

<details>
  <summary>Folders</summary>
  
#### Resources
The resources folder contains files related to our design

#### Scripts
The scripts folder contains files for default actions on the database

#### Static
The static folder contains static stylesheets for our website

#### Templates
The templates folder contains html documents defining our webpages
</details>

<details>
  <summary>Files</summary>
  
Filename | Description
----- | -----
OurStuff.py | Defines our API
forms.py | Defines our WTForms
ourStuff.db | Our SQLite3 database file
</details>

## Developer tools

A few scripts have been developed for saving & reseting the database. This gives developers the freedom to experiment with the data while maintaining a common starting point for all team members.

Using the Command Prompt or Terminal, navigate to the project folder.

To reset the database to its default state, execute
```
python3 scripts/reset.py
```

To update the default state of the database to its current state, execute
```
python3 scripts/save.py
```
