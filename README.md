# RedPlag

This project was generated by Django version 3.1.2, We're working on building a copy checker that detects plagiarism in a given set of text documents.


##Development server
Make migrations by running **python3 manage.py makemigrations fileupload**, **python3 manage.py makemigrations accounts**, **python3 manage.py makemigrations**, **python3 manage.py migrate** .

Create a superuser by running **python3 manage.py createsuperuser** and enter valid credentials

Run "python3 manage.py runserver" for a dev server. Navigate to http://127.0.0.1:8000/


##What we’ve implemented so far:
For Phase 1, we have worked on the implementing a robust user interface and integration with the backend.

##What technology (languages, frameworks, etc.) you’ve used
We've used the authentication support provided by django as a django contrib module in django.contrib.auth. However, we have extended the default user model to suit or needs, ie., we have added functionality to only enable users affiliated with a registered organisation to sign up.

##How the tool is supposed to be run:
First off, an organisation has to contact one of the developers to get verified and register with the site. We provide the orgnisation with a passcode.
For a user to sign up, the just have to decide a user name and password. However, they need to provide the passcode of the organisation they're associated with to create an account.
Once the user is in, they're free to use the tool.

##What is yet to be done
We are yet to implement the actual core logic to detect plagiarism. Once we are ready with that, we also plan to implement bonus features for language specific functionality and stub code.
We'll be out with a documentation as soon as we're ready with the tool. Stay tuned!


