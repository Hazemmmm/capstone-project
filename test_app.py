
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_user = 'postgres'
        self.database_password = 'postgres'
        self.database_host = '127.0.0.1:5432'
        self.database_name = 'test_capstone'
        # self.database_path = 'postgres://{}:{}@{}/{}'.format(self.database_user, self.database_password, self.database_host, self.database_name)
        self.database_path = 'postgres://lulfqpegtegxij:e0135146ffc824e92355d323a9bf4d69a7d3605301334c907d2279089faee986@ec2-54-208-96-16.compute-1.amazonaws.com:5432/dd87refgtcrif7'
        setup_db(self.app, self.database_path)
        
        toke_CEO = os.environ.get('TOKEN_CEO')
        token_developer = os.environ.get('TOKEN_DEVELOPER')

        self.CEO_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + toke_CEO
        }
        
        self.developer_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_developer
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_movies(self):
        res = self.client().get(
            '/movie',
            content_type='application/json',
            headers=self.developer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_fails(self):
        res = self.client().get(
            '/movies',
            content_type='application/json',
            headers=self.developer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['sucess'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_actors(self):
        res = self.client().get(
            '/actor',
            content_type='application/json',
            headers=self.developer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_fails(self):
        res = self.client().get(
            '/atcors',
            content_type='application/json',
            headers=self.developer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['sucess'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_new_movie(self):
        len_movie_before_adding = len(Movie.query.all())

        res = self.client().post('/movie', json={
            'title': 'test case 1',
            'release_date': '1997-11-11'
        }, content_type='application/json', headers=self.CEO_headers)

        len_movie_after_adding = len(Movie.query.all())

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(len_movie_after_adding - len_movie_before_adding == 1)

    def test_add_new_movie_fails(self):

        res = self.client().post(
            '/movie',
            json={},
            content_type='application/json',
            headers=self.CEO_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['sucess'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'], 'internal server error')

    def test_delete_movie(self):

        new_movie = Movie(title='test delete case', release_date='2021-11-12')
        new_movie.insert()

        movie_id = new_movie.id
        res = self.client().delete(
            '/movie/{}'.format(movie_id),
            content_type='application/json',
            headers=self.CEO_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(data['deleted'])

    def test_delte_movie_fails(self):

        res = self.client().delete(
            '/movie/12432435',
            content_type='application/json',
            headers=self.CEO_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['sucess'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_patch_movie(self):

        patch_movie = {
            "title": "test-patch-case-updated",
            "release_date": "1997-11-12"
        }
        data_updatd = json.dumps(patch_movie)

        res = self.client().patch(
            f"/movie/{27}",
            content_type='application/json',
            data=data_updatd,
            headers=self.CEO_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(data['updated_movie'])

    def test_patch_movie_fails(self):
        patch_movie = {
            'title': '',
            'release_date': '11-10-124'

        }
        data_updatd = json.dumps(patch_movie)

        res = self.client().patch(
            f"/movie/{36}",
            content_type='application/json',
            data=data_updatd,
            headers=self.CEO_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['sucess'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'], 'internal server error')


if __name__ == '__main__':
    unittest.main()
