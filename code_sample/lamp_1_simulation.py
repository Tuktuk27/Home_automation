from flask import Flask, request

app = Flask(__name__)

lamp_1_state = "off"

@app.route("/lamp_1", methods=["GET", "POST"])
def lamp_1():
    global lamp_1_state
    if request.method == "POST":
        action = request.form.get("action")
        print("test")
        print(action)
        if action == "on":
            lamp_1_state = "on"
        elif action == "off":
            lamp_1_state = "off"
    return f"Lamp_1 State: {lamp_1_state}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

