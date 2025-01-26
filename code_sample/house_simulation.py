from flask import Flask, request, jsonify

app = Flask(__name__)

house_state = "unlocked"

@app.route("/house", methods=["GET", "POST"])
def house():
    global house_state

    if request.method == "POST":
        action = request.form.get("action")
        if action == "lock":
            house_state = "locked"
        elif action == "unlock":
            house_state = "unlocked"

    return jsonify({"house_state": house_state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
