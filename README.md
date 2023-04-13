# RISE Web App

RISE Web App is a Flask Python Project that allows users to create an account, add characters and Game Master Sessions to their account, view all of RISE's documentation, add friends, and anything else that may get added in the future.

## Ideas

Currently considering rebuilding the entire app with MERN instead of Flask. Essentially using JavaScript instead of Python.

## Installation

This project will eventually be deployed, until then you will need to install everything below.

Use the **requirements.txt** file to add all of the installation methods.

```bash
# If the requirements.txt file does not work
pip install flask PyMySQL flask-bcrypt
#navigate to the project folder
pipenv install flask PyMySQL
pipenv shell
pipenv install flask-bcrypt
```

## Project Status

Project is still in it's infancy and planning stages.

Things that we still need to do:
- Finish the database (possibly use NoSQL or MongoDB instead of MySQL)
- Make the database files to import
- Create the controllers and models for each of our major database tables
- Make logic for character info
- Handle leveling up
- Update logic for complex and fringe cases

## Contributors

alexandervice and tschelli
