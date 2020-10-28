# RedPlag

This project was generated by Django version 3.1.2, We're working on building a copy checker that detects plagiarism in a given set of text documents.


## Development server
1. Move to ```<project-dir>```, and edit the settings related to DB, timezone and other settings in settings.py.

2. Make migrations by running 
```sh
$ python3 manage.py makemigrations
$ python3 manage.py makemigrations fileupload
$ python3 manage.py makemigrations accounts 
$ python3 manage.py migrate
```

Create a superuser by running the following command and enter valid credentials
```sh
$ python3 manage.py createsuperuser
```

Run $python3 manage.py runserver for a dev server. Navigate to http://127.0.0.1:8000/


## What we’ve implemented so far:
For Phase 1, we have worked on the implementing a robust user interface and integration with the backend. We've used the authentication support provided by django as a django contrib module in django.contrib.auth. However, we have extended the default user model to suit our needs, ie., we have added functionality to only enable users affiliated with a registered organisation to sign up. We have also allowed user change his/her password. We have implimented an UI to allow user to upload a zip file. We have also implimented an UI to allow user to download all his previous uploads results. Name of the zip file submitted and time at which it is submitted will be displayed.

## What technology (languages, frameworks, etc.) you’ve used
We have used Django Web Framework for both frontend and backend. 
Install python3 with
```sh
$ sudo apt update
$ sudo apt install python3
```
Install Django with
```sh
$ sudo apt install python3-pip
$ pip3 install Django
```

## How the tool is supposed to be run:
First off, an organisation has to contact one of the developers to get verified and register with the site. We provide the orgnisation with a passcode.
For a user to sign up, he/she just have to decide a user name and password. However, they need to provide the passcode of the organisation they're associated with to create an account.
Once the user is in, they're free to use the tool.
User can upload a zip of a folder containing the files to be checked. All files should be present in a single folder, which is to be zipped. User can upload a zip file of size upto 2MB. After uploading the file user will be redirected to a page where he can download the response file. In addition user can navigate to a page having previous results by clicking ```Previous results``` button in Home below ```upload``` button. 

## What is yet to be done
We are yet to implement the actual core logic to detect plagiarism. Once we are ready with that, we also plan to implement bonus features for language specific functionality and stub code.
We'll be out with a documentation as soon as we're ready with the tool. Stay tuned!

