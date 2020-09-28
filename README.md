# Earthquake-DI-IBM-Cloud
Python Flask application for Data Analysis of Earthquake data worldwide. This application can be used as a Flask web application template meant for hosting on IBM Cloud.

The earthquake data was collected from https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php and added into an IBM DB2 instance on IBM cloud. Various queries are also implemented for reading the Earthquake data collected.

# Files:
1. The "templates" folder contains all the HTML pages used in this project.
2. The "app.py" file is the main servlet file.
3. "pip" file installs all the libraries needed for running the application.
4. "proc" file contains the default command that runs after your code is uploaded to IBM cloud. The default command runs the application.
5. "requirements" file contains all the libraries that need to be installed for the application to run.
6. "runtime" file states the python version that should be used while executing the source code. I have used python 3.7.7

To run this code on your system execute the requirements file first and then run the app.py file. 


