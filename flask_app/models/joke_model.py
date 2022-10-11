
from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'dad_jokes_red'


class Joke:
    def __init__(self, data):
        self.id = data['id']
        self.setup = data['setup']
        self.punchline = data['punchline']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dad_id = data['dad_id']
    
    def __repr__(self):
        return f'<Joke: {self.setup}>'

    @staticmethod
    # for post handler neeeeddddd to make sure if post is valid to post in db
    def validate_joke(form):
        is_valid = True
        if len(form['setup']) < 3:
            flash('Setup must be at least three characters.', 'setup')
            is_valid = False
        if len(form['punchline']) < 3:
            flash('Punchline must be at least three characters.', 'punchline')
            is_valid = False
        return is_valid

    # create a joke
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO jokes (setup, punchline, dad_id) VALUES (%(setup)s, %(punchline)s, %(dad_id)s);'
        joke_id = connectToMySQL(DATABASE).query_db(query, data)
        return joke_id

    # find all jokes (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from jokes;'
        results = connectToMySQL(DATABASE).query_db(query)
        jokes = []
        for result in results:
            jokes.append(Joke(result))
        return jokes

    # find one joke by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from jokes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        joke = Joke(results[0])
        return joke

    # update one joke by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE jokes SET setup = %(setup)s, punchline = %(punchline)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one joke by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM jokes WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True