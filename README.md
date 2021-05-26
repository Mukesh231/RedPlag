A web based application to detect plagiarism within a set of text documents.

## UI and user authentication

We have used Django Web Framework for building both the frontend and backend. For authentication, we used the authentication support provided by django in the __django.contrib.auth__ module. Moreover, we have extended the default user model to suit our needs, ie., we have added functionality to only enable users affiliated with a registered organisation to sign up. Registered users are allowed to change their account passwords. We have implimented an UI to allow user to upload a zip file. A user can download all his previous uploads results. Name of the zip file submitted and time at which it is submitted will be displayed.

## The Core Logic

__Pre-processing__ : For each code file in C, C++, java, or python, the string which contains the contents of the file is refined by removing all the comments in the code. 

The first crucial checkpoint we arrive at is the computation of the term-document matrix. We achieve this using:
1. __Bag of Words__ : After pre-processing of the files is complete, we apply word-tokenisation to the string containing the contents of the files. Now, for each word in the file, we check if the word is a stop-word (i.e., a filler word that has no real meaning or relevance to the topic) and if it isn't we add it to a dictionary containing frequency counts for each word, or update the frequency count of the word if it is already present in the dictionary. Characters are converted to lowercase to avoid unecessary extras. This is our collection of the total document frequency, which shows the frequency of each word in the entire set of documents.
Follwing this, we again traverse all the files, but now, for each file, we create a new dictionary containing each word in the global dictionary mapped to its frequency *in the file*. We take the list of values and append it to a matrix, this is our naive term-document matrix. 
2. __tf-idf__ : The naive term-document matrix is updated by replacing each term in the matrix with the *relative frequency* of that word in our corpus.  The overall effect of this weighting scheme is to avoid a common problem when conducting text analysis: the most frequently used words in a document are often the most frequently used words in all of the documents. In contrast, terms with the highest tf-idf scores are the terms in a document that are distinctively frequent in a document, when that document is compared other documents.

Once we arrive at the refined term-document matrix, we proceed to apply __Latent Semantic Analysis__ to move ahead:

__Latent Semantic Analysis (LSA)__ : LSA attempts to cluster words of the document into "topics". We do this because the term-document matrix by itself is too large to perform computations on. Moreover, two documents may convey the same idea though they're using different words, and catching plagiarism in this case using our naive matrix would consume a lot of time and memory and not yield very satisfactory results. Thus, we use LSA, which is a statistical method to group words belonging to the same "topic" together. We essentially apply Singluar Value Decomposition (SVD) to our term-document matrix and reduce the relevant dimension (the dimension containing the terms in the matrix) to the required number of topics. To obtain the optimal number of topics, if the number of documents is very high ( 100- 100000) then generally 100-300 topics can be choosen. For small no.of documents we choose our no.of topics as to obtain large information in minimum possible no.of topics, to estimate such optimal number we can take no.of topics such that their variances add to 90-95 percent of total variance. By knowing optimal topics and document term matrix we can apply svd and obtain our final *topic-document* matrix.

Once we have our topic-document matrix ready, we normalise it and compute __cosine similarity__ for each pair of documents, with the results obtained in a square matrix obtained by the dot product of the topic-document matrix with itself. The similarity matrix is returned to the user, with the cosine similarity depicting the degree of similarity between each pair of documents.

# Built With
We have used Django Web Framework for building both the frontend and backend.
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
In addition, we have imported and made use of a few python modules which might need to to be installed separately in the developer's system, provided they aren't already present :P
Install the required modules with:
```sh
pip3 install numpy
pip3 install nltk
pip3 install pandas
pip3 install sklearn
pip3 install matplotlib
pip3 install mpld3
```
We have also used a resource belonging to the nltk module that can to be installed from the python3 shell using:
```sh
python3
>>> import nltk
>>> nltk.download('stopwords')
```
# Using the tool

Download this repository from github and follow the relevant instructions below to get going!

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

Now, create a **superuser** ID using
```sh
python3 manage.py createsuperuser
```
You will be required to enter your username, email and set a password. Once the superuser is created successfully, navigate to ```http://127.0.0.1:8000/admin/``` and login with your superuser credidentials. The superuser can now view and manipulate existing user and file data, register or deregister organisations, and much more.


## How to use:

For a user to sign up, they just have to decide a user name and password. As an additional form of security, a user is required to provide the passcode of the organisation they're associated with to create an account.
Once the user is in, they're free to use the tool.

The user can upload a zipped folder containing the files to be checked, provided he has signed up and logged in, of course. All files are required be present in a single folder. The user can upload a zip file of size upto 2MB. 

After uploading the folder, the user will be redirected to a page where they can download the result files. In addition, users can find the previous results of their file sets by clicking the ```Previous results``` button. 

## Registering an Organisation 
An organisation can only be registered by the dev or a superuser. Click on the Add+ button necxt to Organisations to register a organisation with its name and passcode.

Register an organisation from the shell, after navigating to the project directory, with:

```sh
python3 manage.py shell
>>> from accounts.models import Organisation
>>> org = Organisation(organame="REQUIRED ORGANISATION NAME", orgacode="REQUIRED ORGANISATION CODE")
>>> org.save()
```

