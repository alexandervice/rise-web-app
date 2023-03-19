from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, ride
from flask import flash

class Message:
    database = "ohana-rideshares"
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.ride = None

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO messages (creator_id, ride_id, content , created_at , updated_at ) VALUES ( %(creator_id)s, %(ride_id)s, %(content)s , NOW() , NOW() );"
        result = connectToMySQL(cls.database).query_db( query, data )
        return result

    @classmethod
    def delete(cls, message_id):
        query  = "DELETE FROM messages WHERE id = %(id)s;"
        data = {"id": message_id}
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def get_all_messages_for_ride_with_creator(cls, ride_id):
        # Get all messages, for each post and their one associated User that created it
        query = "SELECT * FROM messages LEFT JOIN users ON messages.creator_id = users.id LEFT JOIN rides on messages.ride_id = rides.id WHERE ride_id = %(ride_id)s;"
        data = {"ride_id": ride_id}
        results = connectToMySQL(cls.database).query_db(query, data)
        if results == False:
            return []
        all_messages = []
        for row in results:
            # Create a message class instance from the information from each db row
            one_message = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_message_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "birth_date": row['birth_date'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_message_ride_info = {
                "id": row["rides.id"],
                "rider_id": row["rider_id"],
                "driver_id": row["driver_id"],
                "destination": row["destination"],
                "pickup_location": row["pickup_location"],
                "ride_date": row["ride_date"],
                "details": row["details"],
                "created_at": row['rides.created_at'],
                "updated_at": row['rides.updated_at']
            }

            # Create the User class instance that's in the user.py model file
            author = user.User(one_message_author_info)
            # Associate the post class instance with the User class instance by filling in the empty creator attribute in the message class
            one_message.creator = author
            
            # Create the Ride class instance that is in the ride.py model file
            rideshare_info = ride.Ride(one_message_ride_info)
            one_message.ride = rideshare_info

            # Append the message containing the associated User and Ride to your list of messages
            all_messages.append(one_message)
        return all_messages
    
    @staticmethod
    def validate_message( message ):
        is_valid = True
        # test whether a field matches the pattern
        if len(message['content']) < 1:
            flash("message cannot be empty.", "message")
            is_valid = False
        return is_valid