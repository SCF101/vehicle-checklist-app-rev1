from flask import Flask, render_template_string, request, redirect
import os
import json
from datetime import datetime

app = Flask(__name__)

FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vehicle Checklist</title>
</head>
<body>
    <h1>Daily Vehicle Checklist</h1>
    <form method="POST">
        <h2>Driver Information</h2>
        Name: <input type="text" name="name"><br>
        Date: <input type="date" name="date"><br>
        Vehicle Registration Number: <input type="text" name="vehicle_reg"><br>
        Odometer Reading: <input type="text" name="odometer"><br>

        <h2>Exterior Checks</h2>
        {% for item in exterior %}
            <input type="checkbox" name="exterior" value="{{ item }}"> {{ item }}<br>
        {% endfor %}

        <h2>Interior Checks</h2>
        {% for item in interior %}
            <input type="checkbox" name="interior" value="{{ item }}"> {{ item }}<br>
        {% endfor %}

        <h2>Under the Hood</h2>
        {% for item in hood %}
            <input type="checkbox" name="hood" value="{{ item }}"> {{ item }}<br>
        {% endfor %}

        <h2>Safety Equipment</h2>
        {% for item in safety %}
            <input type="checkbox" name="safety" value="{{ item }}"> {{ item }}<br>
        {% endfor %}

        <h2>Additional Notes</h2>
        Issues Found: <textarea name="issues"></textarea><br>
        Action Taken: <textarea name="action"></textarea><br>
        Signature: <input type="text" name="signature"><br>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def checklist():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "date": request.form.get("date"),
            "vehicle_reg": request.form.get("vehicle_reg"),
            "odometer": request.form.get("odometer"),
            "exterior": request.form.getlist("exterior"),
            "interior": request.form.getlist("interior"),
            "hood": request.form.getlist("hood"),
            "safety": request.form.getlist("safety"),
            "issues": request.form.get("issues"),
            "action": request.form.get("action"),
            "signature": request.form.get("signature")
        }
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"submissions/checklist_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return redirect("/")
    
    return render_template_string(FORM_TEMPLATE,
        exterior=["Tyres", "Lights", "Mirrors", "Windshield & Windows", "Wipers & Washer Fluid", "Body Damage", "License Plates"],
        interior=["Seatbelts", "Dashboard Warning Lights", "Horn", "Air Conditioning / Heater", "Cleanliness"],
        hood=["Engine Oil Level", "Coolant Level", "Brake Fluid Level", "Battery Condition", "Belts & Hoses"],
        safety=["Fire Extinguisher", "First Aid Kit", "Emergency Triangle", "Spare Tyre & Jack"]
    )

if __name__ == "__main__":
    app.run(debug=True)
