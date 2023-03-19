from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import message
from flask import flash
from datetime import date, datetime

def is_in_past(ride_date):
        if isinstance(ride_date, str):
            ride_date = datetime.strptime(ride_date, '%Y-%m-%d').date()
        today=date.today()
        if ride_date < today:
            return True
        else:
            return False

class Ride:
    database = "ohana-rideshares"
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.pickup_location = data['pickup_location']
        self.ride_date = data['ride_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # None can represent a currently empty space for a single User dictionary to be placed here, as a Post is made by ONE User. We want a User instance and all their attributes to be placed here, so something like data['...'] will not work as we have to make the User instance ourselves.
        self.rider = None
        self.driver = None
        self. messages = []

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO rides (rider_id, driver_id, destination, pickup_location, ride_date, details, created_at , updated_at ) VALUES ( %(rider_id)s, %(rider_id)s, %(destination)s, %(pickup_location)s, %(ride_date)s, %(details)s, NOW() , NOW() );"
        result = connectToMySQL(cls.database).query_db( query, data )
        return result

    @classmethod
    def delete(cls, ride_id):
        query  = "DELETE FROM rides WHERE id = %(id)s;"
        data = {"id": ride_id}
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, ride_id):
        query = "SELECT * FROM rides WHERE id = %(id)s;"
        data = {
            "id": ride_id
        }
        results = connectToMySQL(cls.database).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def set_driver(cls, data):
        query = "UPDATE rides SET driver_id = %(driver_id)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results
    
    @classmethod
    def cancel_driver(cls, data):
        query = "UPDATE rides SET driver_id = %(rider_id)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE rides SET pickup_location = %(pickup_location)s, details = %(details)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results

    @classmethod
    def get_all_rides_with_rider_and_driver(cls):
        # Get all posts, and their one associated User that created it
        query = "SELECT * FROM rides LEFT JOIN users as rider ON rides.rider_id = rider.id LEFT JOIN users as driver ON rides.driver_id = driver.id;"
        results = connectToMySQL(cls.database).query_db(query)
        all_rides = []
        for row in results:
            # Create a post class instance from the information from each db row
            one_ride = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_ride_rider_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['rider.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "birth_date": row["birth_date"],
                "created_at": row['rider.created_at'],
                "updated_at": row['rider.updated_at']
            }

            one_ride_driver_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['driver.id'], 
                "first_name": row['driver.first_name'],
                "last_name": row['driver.last_name'],
                "email": row['driver.email'],
                "password": row['driver.password'],
                "birth_date": row["driver.birth_date"],
                "created_at": row['driver.created_at'],
                "updated_at": row['driver.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            rider = user.User(one_ride_rider_info)
            # Associate the post class instance with the User class instance by filling in the empty creator attribute in the post class
            one_ride.rider = rider

            # Create the User class instance that's in the user.py model file
            driver = user.User(one_ride_driver_info)
            # Associate the post class instance with the User class instance by filling in the empty creator attribute in the post class
            one_ride.driver = driver

            # Append the post containing the associated User to your list of posts
            all_rides.append(one_ride)
        return all_rides

    @staticmethod
    def validate_ride( ride ):
        is_valid = True
        # test whether a field matches the pattern
        if len(ride['destination']) < 3:
            flash("Destination must be at least 3 characters.", "ride")
            is_valid = False
        elif len(ride['destination']) > 255:
            flash("Destination must be less than 256 characters.", "ride")
            is_valid = False
        if len(ride['pickup_location']) < 3:
            flash("Pick-Up Location must be at least 3 characters.", "ride")
            is_valid = False
        elif len(ride['pickup_location']) > 255:
            flash("Pick-Up Location must be less than 256 characters.", "ride")
            is_valid = False
        if len(ride['details']) < 3:
            flash("Details must be at least 10 characters.", "ride")
            is_valid = False
        if len(ride['ride_date']) < 1:
            flash("Rideshare Date field is required.", "ride")
            is_valid = False
        elif is_in_past(ride['ride_date']):
            flash("Rideshare Date must not be in the past.", "ride")
            is_valid = False
        return is_valid