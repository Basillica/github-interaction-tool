## Table of contents
* [General info](#general-info)
* [Note](#note)
* [Technologies](#technologies)
* [Setup](#setup)
* [Tests](#test)

## General info
This project is a simple flask implementation that interacts with any valid github profile. Two endpoints are exposed:
* The endpoint /active/<user> returns a json object with a boolean field that is true if the specified user has pushed a code in the last 24 hours, and false if otherwise
* The endpoint /downwards/<repo> returns a json object with a boolean field that is true if the specified repo has had more deletions than additions in the last 7 days. False is returned if otherwise.

## Note
Given the dynamic structure of this program, **it is advisable to visit the endpoint '/active/user' first**. That way, the **user** is easily noted and information about the repos of the user can be fetched using the second endpoint **/downwards/repo**. If not, the program will simply advice you do so. 
	
## Technologies
This project is created with the following modules:
* Flask
* Beautifulsoup
* Requests
	
## Setup
To run this project on a local machine, simply follow the instructions below:

```
$ curl https://api.github.com/Basillica/github-interaction-tool-master
$ cd github-interaction-tool-master
$ virtualenv env
$ env\Script\activate
$ pip install -r requirements.txt
$ python run.py
```
Open the browser and navigate to **http://127.0.0.1:5000**

To run this program on docker, simply run the docker file using the following commands:
```
$ docker build . -t flask-app:v1
$ docker run -p 5000:5000 flask-app:v1
```

## Test

Basic test are also implemented.
These include the response of the index endpoint and the return object from the endpoint ( which is supposed to be a **JSON** object ).
To run the test, from the virtual environment:

```
$ python test.py
```
