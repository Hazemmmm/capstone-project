import os
from flask import (
    Flask,
    request,
    abort,
    jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
    setup_db,
    Actor,
    Movie
)
from flask_sqlalchemy import SQLAlchemy
from auth import (
    AuthError,
    requires_auth
)

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization")
        response.headers.add(
            "Acess-Control-Allow-Methods",
            "GET, POST, PUT, OPTIONS, PATCH,DELTE")

        return response

    @app.route("/")
    def index():
        return jsonify({'message': "Welcome to my Capstone Project! :)"})

    @app.route("/movie", methods=["GET"])
    @requires_auth('get-movies')
    def get_movies(jwt):
        movies = Movie.query.all()
        if not movies:
            abort(404)
        try:

            movie_list = [movie.format() for movie in movies]
            return jsonify({
                "sucess": True,
                'movies': movie_list
            })

        except Exception as e:
            print(sys.exc_info())
            abort(500)

    @app.route("/actor", methods=["GET"])
    @requires_auth('get-actors')
    def get_actors(jwt):

        try:

            actors = Actor.query.all()
            if not actors:
                abort(404)

            actors_list = [actor.format() for actor in actors]
            return jsonify({
                "sucess": True,
                "actors": actors_list
            })
        except Exception as e:
            print(sys.exc_info())
            abort(500)
            db.session.rollback()
        finally:
            db.session.close()

    @app.route('/movie', methods=['POST'])
    @requires_auth('post-movies')
    def add_movie(jwt):
        try:

            body = request.get_json()
            new_title = body.get('title')
            new_releaseDate = body.get("release_date")

            if ((new_title is None) or (new_releaseDate is None)):
                abort(404)

            movie = Movie(title=new_title, release_date=new_releaseDate)
            movie.insert()

            return jsonify({
                "sucess": True,
                'Created': movie.id

            })

        except Exception as e:
            print(sys.exc_info())
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete-movie')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                "sucess": True,
                'deleted': id
            })

        except Exception as e:
            print(sys.exc_info())
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    @app.route('/movie/<int:id>', methods=['PATCH'])
    @requires_auth('patch-movie')
    def patch_movie(jwt, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if not movie:
                abort(404)
            body = request.get_json()
            new_title = body.get('title')
            new_releaseDate = body.get('release_date')

            if ((new_title is not None) or (new_releaseDate is not None)):
                movie.title = new_title
                movie.release_date = new_releaseDate

            movie.update()
            return jsonify({
                "sucess": True,
                "updated_movie": [movie.format()]
            })

        except Exception as e:
            print(sys.exc_info())
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            "sucess": False,
            "error": 422,
            "message": "Un-Processable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "sucess": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internalError(error):
        return jsonify({
            "sucess": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(exception):
        return jsonify({
            'sucess': False,
            'error': exception.status_code,
            'message': exception.error['code']
        }), exception.status_code

    return app


app = create_app()

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run()
