from flask import redirect, request, session
from flask_app import app
# from flask_app.models.user import User
# from flask_app.models.post import Post
from flask_app.models.message import Message

@app.route('/create_message', methods=["POST"])
def create_message():
    data = {
        "creator_id": session['logged_in_user']["user_id"],
        "ride_id": request.form["ride_id"],
        "content" : request.form["content"]
    }
    if not Message.validate_message(data):
        print("comment creation rejected: bad form entry")
        return redirect(f'/rides/{data["ride_id"]}')
    Message.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect(f'/rides/{data["ride_id"]}')
# NOTE never render_template on a POST route


@app.route('/messages/delete/<int:message_id>')
def delete_message(message_id):
    Message.delete(message_id)
    return redirect(f'/rides/{session["last_viewed_ride"]}')