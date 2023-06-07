from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Attribute:
    database = "rise"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.focuses = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO attributes (name, description) VALUES (%(name)s, %(description)s);"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM attributes WHERE id = %(attribute_id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM attributes WHERE id = %(attribute_id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE attributes SET name = %(name)s, description = %(description)s, WHERE id = %(attribute_id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results


