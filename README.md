# Udacity Full Stack Web Developer Capstone Project

## Motivation

Cerate a backend app which demonstrates the functionalites of endpoints with RBAC to implement JWT that JWT authentication has been included in the project.

The motivation for this project is to demonstrate skills in authentication tools (Auth0), RBAC endpoints, error handling, test writting, and handling data between the front and back, and finally deploy it in Heroku cloud platform.

## Setup and dependencies

Make sure to install

- python3
- pip
- psql

To start the project you can create a virtual enviorment
python3 -m venv env
source env/bin/activate python

and then install the required packages, PIP dependencies by running:

pip install -r requirements.txt

you should run this first to set the virables enviorment
source setup.sh

The endpoints are ready to be tested with the deployed server by running the following command:
python3 test_app.python

The deployed application can be dound here:
https://capstonehazem.herokuapp.com/

### Key dependencies

- Flask
- SQLAlchemy
- Flask-CORS

## Instruction for deployment Heroku

1- Create Procfile and put these lines on it

- web: gunicorn app:app
  2- login through heroku client
- heroku login
- heroku create name_of_your_app
  The output will include a git url for your Heroku application. Copy this as, we'll use it in a moment.
- git remote add heroku heroku_git_url
- heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
- git push heroku master
  Once your app is deployed run this command to migrate database:
- heroku run python manage.py db upgrade --app name_of_your_application
  that's is now you have your application deployed/.

## Avaliable Endpoints:

1- GET '/movie' to get all the movies.
{
'success': True,
'movies': movie_list
}

2- GET '/actor' to get all the actors.
{
'success': True,
'movies': actors_list
}

3- DELETE '/movie/{id} to remove specific movie id from the list.
{
"sucess":True,
'deleted': id
}

4- POST '/movie' to add a new movie to the movie list.
{
"sucess":True,
'Created':movie.id

}

5- PATCH '/movie/{id}' to edit an exisiting movie

{
"sucess":True,
"updated_movie": [movie.format()]
}

## TESTING:

python test_app.py

## Avaliable Roles

### Permissions:

- 'get-movies' : Get the list of all movies
- 'get-actors': Get the list of all actors
- 'post-movie': Post a new movie
- 'delete-movie': Delete a movie
- 'patch-movie': Update an existitng movie

### Roles

#### CEO Role

Can list all the movies, actors, post a new movie, delete an exisitng movie or edit it.

#### Developer Role

Can list all the movies and actors.
