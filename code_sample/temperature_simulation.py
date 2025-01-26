from flask import Flask, request, jsonify

app = Flask(__name__)

temperature_setpoint = 25.0

@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    global temperature_setpoint

    if request.method == "POST":
        temperature_setpoint = float(request.form.get("temperature"))

    return jsonify({"temperature_setpoint": temperature_setpoint})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
