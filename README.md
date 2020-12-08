# RedPlag - A Plagiarism Checker

This project was generated by Django version 3.1.2. We're working on building a copy checker that detects plagiarism in a given set of text documents.


## Development server
1. Move to ```<project-dir>```, and edit the settings related to DB, timezone and other settings in settings.py.

2. Make migrations by running 
```sh
python3 manage.py makemigrations
python3 manage.py makemigrations fileupload
python3 manage.py makemigrations accounts 
python3 manage.py migrate
```

Create a superuser by running the following command and entering your credentials
```sh
python3 manage.py createsuperuser
```

Run ```$ python3 manage.py runserver``` for a dev server. Navigate to ```http://127.0.0.1:8000/```


## What we have implemented so far:
For __Phase 1__ of this project, we have worked on implementing a robust user interface and integration with the backend. We've used the authentication support provided by django as a django contrib module in __django.contrib.auth__. Moreover, we have extended the default user model to suit our needs, ie., we have added functionality to only enable users affiliated with a registered organisation to sign up. Registered users are allowed to change their account passwords. We have implimented an UI to allow user to upload a zip file. We have also implimented an UI to allow user to download all his previous uploads results. Name of the zip file submitted and time at which it is submitted will be displayed.

## Built With
We have used Django Web Framework for both frontend and backend.
Install python3 with
```sh
sudo apt update
sudo apt install python3
```
Install Django with
```sh
sudo apt install python3-pip
pip3 install Django
```

## How the tool is supposed to be run:

For a user to sign up, they just have to decide a user name and password. As an additional form of security, a user is required to provide the passcode of the organisation they're associated with to create an account.
Once the user is in, they're free to use the tool.

### Registering an Organisation 
First create a **superuser** using
```sh
python3 manage.py createsuperuser
```
You will be required to enter your username, email and set a password. Once the superuser is created successfully, navigate to ```http://127.0.0.1:8000/admin/``` and login with your superuser credidentials and register Organisations as required.

The user can upload a zipped folder containing the files to be checked. All files are required be present in a single folder. User can upload a zip file of size upto 2MB. 

After uploading the folder, the user will be redirected to a page where they can download the response file. In addition, the user can find the previous results of their file sets by clicking the ```Previous results``` button. 

## What is yet to be done
We are yet to implement the actual core logic to detect plagiarism. Once we are ready with that, we also plan to implement bonus features for language specific functionality and stub code.
We'll be out with a documentation as soon as we're ready with the tool. Stay tuned!

