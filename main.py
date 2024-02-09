from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from generate_unique_code import generate_unique_code
from room_codes import room_codes

app = Flask(__name__)
app.config["SECRET_KEY"] = "h3fhVd2dDn8DcS"
socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "GET":
        return render_template("home.html")
    
    name = request.form.get("name")
    code = request.form.get("code")
    join = request.form.get("join", False)
    create = request.form.get("create", False)

    if not name:
        return render_template("home.html", error="Name not provided!", name=name, code=code)

    if join and not code:
        return render_template("home.html", error="Room Code not provided!", name=name, code=code)

    if not create and code not in room_codes:
        return render_template("home.html", error="Room Code not available!", name=name, code=code)

    room = code

    if create:
        room = generate_unique_code(4)
        room_codes[room] = {
            "members": 0,
            "messages": []
            }
        
    session["room"] = room
    session["name"] = name
    
    return redirect(url_for("room"))

@app.route("/room")
def room():
    return render_template("room.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
