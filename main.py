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

    if join != False and not code:
        return render_template("home.html", error="Room Code not provided!", name=name, code=code)

    if create == False and code not in room_codes:
        return render_template("home.html", error="Room not available!", name=name, code=code)

    room = code

    if create != False:
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
    room = session.get("room")
    name = session.get("name")

    if not room or not name or room not in room_codes:
        return redirect(url_for("home"))
    
    return render_template("room.html", room=room, messages=room_codes[room]["messages"])

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    
    if room not in room:
        leave_room(room)
        return
    
    join_room(room)

    send({"name": name, "message": "has entered the room"}, to=room)
    room_codes[room]["members"] += 1

    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    
    leave_room(room)

    if room in room_codes:
        room_codes[room]["members"] -= 1

        if room_codes[room]["members"] <= 0:
            del room_codes[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")

@socketio.on("message")
def message(data):
    room = session.get("room")
    name = session.get("name")

    if room not in room_codes:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    room_codes[room]["messages"].append(content)
    print(f"{name} said: {content['message']}")


if __name__ == "__main__":
    socketio.run(app, debug=True)
