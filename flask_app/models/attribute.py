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


#MOVE TO FOCUS CLASS ONCE IT IS CREATED
    @classmethod
    def get_all_focuses_from_all_attributes(cls):
        query = "SELECT * FROM focuses JOIN attributes ON focuses.attribute_id = attributes.id;"
        results = connectToMySQL(cls.database).query_db(query)
        all_focuses_and_attributes = []

        for row in results:
            one_focus = cls(row)
            one_attribute_info = {
                "id": row['focuses.id'], 
                "attribute id": row['attribute_id'],
                "name": row['name'],
                "description": row['description'],
                "example": row['example'],
                "created_at": row['focuses.created_at'],
                "updated_at": row['focuses.updated_at']
                }
            
            attribute_instance = attribute.Attribute(one_attribute_info)
            one_focus.focuses.append(attribute_instance)

            all_focuses_and_attributes.append(one_focus)
        return all_focuses_and_attributes