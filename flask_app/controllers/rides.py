from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.ride import Ride
from flask_app.models.message import Message
from datetime import date, datetime

@app.route('/add_new_ride')
def add_ride():
    user=User.get_one(session['logged_in_user']["user_id"])
    return render_template("create_ride.html", user=user)

@app.route('/create_ride', methods=["POST"])
def create_ride():
    data = {
        "rider_id": session['logged_in_user']["user_id"],
        "destination" : request.form["destination"],
        "pickup_location" : request.form["pickup_location"],
        "ride_date" : request.form["ride_date"],
        "details" : request.form["details"]
    }
    if not Ride.validate_ride(data):
        print("ride creation rejected: bad form entry")
        return redirect('/add_new_ride')
    print(data)
    Ride.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/rides')
# NOTE never render_template on a POST route

@app.route('/rides/delete/<int:ride_id>')
def delete_ride(ride_id):
    messages=Message.get_all_messages_for_ride_with_creator(ride_id)
    if len(messages) > 0:
        for message in messages:
            if message.ride.id == ride_id:
                Message.delete(message.id)
    Ride.delete(ride_id)
    return redirect('/rides')

@app.route('/rides/<int:ride_id>')
def show_ride(ride_id):
    user=User.get_one(session['logged_in_user']["user_id"])
    # calling the get_one method and supplying it with the id of the ride we want to get
    # ride=Ride.get_one(ride_id)
    session["last_viewed_ride"] = ride_id
    rides=Ride.get_all_rides_with_rider_and_driver()
    for ride in rides:
        if ride.id == ride_id:
            ride_info = ride
    messages = Message.get_all_messages_for_ride_with_creator(ride_id)
    return render_template("show_ride.html",user=user, ride=ride_info, messages=messages)

@app.route('/rides/edit/<int:ride_id>')
def edit_ride(ride_id):
    user=User.get_one(session['logged_in_user']["user_id"])
    ride=Ride.get_one(ride_id)
    return render_template("edit_ride.html", user=user, ride=ride)

@app.route('/rides/update',methods=['POST'])
def update_ride():
    ride=Ride.get_one(request.form["ride_id"])
    data = {
        "rider_id": session['logged_in_user']["user_id"],
        "id": request.form["ride_id"],
        "destination" : ride.destination,
        "ride_date" : ride.ride_date.strftime('%Y-%m-%d'),
        "pickup_location" : request.form["pickup_location"],
        "details" : request.form["details"]
    }
    if not Ride.validate_ride(data):
        print("ride creation rejected: bad form entry")
        return redirect(f'/rides/edit/{data["id"]}')
    Ride.update(data)
    return redirect('/rides')


@app.route('/add_driver/<int:ride_id>', methods=["POST"])
def add_driver(ride_id):
    data = {
        "driver_id": session['logged_in_user']["user_id"],
        "id": ride_id,
    }
    Ride.set_driver(data)
    return redirect('/rides')

@app.route('/remove_driver/<int:ride_id>', methods=["POST"])
def remove_driver(ride_id):
    data = {
        "driver_id": session['logged_in_user']["user_id"],
        "id": ride_id,
        "rider_id": request.form["rider_id"]
    }
    print(request.form)
    Ride.cancel_driver(data)
    return redirect('/rides')