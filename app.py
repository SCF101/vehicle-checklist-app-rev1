from flask import Flask, render_template_string, request, redirect
import os
import json
from datetime import datetime

app = Flask(__name__)
SUBMISSIONS_DIR = "submissions"
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vehicle Checklist</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { color: #2c3e50; }
        label { display: block; margin-top: 10px; }
        input[type="text"], textarea { width: 100%%; padding: 8px; margin-top: 5px; }
        .checkbox-group { margin-top: 10px; }
        .checkbox-group label { display: block; }
        button { margin-top: 20px; padding: 10px 20px; }
    </style>
</head>
<body>
    <h2>Daily Vehicle Checklist</h2>
    <form method="POST">
        <label>Full Name: <input type="text" name="full_name" required></label>
        <label>Date: <input type="text" name="date" required></label>
        <label>Vehicle Registration Number: <input type="text" name="vehicle_reg" required></label>
        <label>Odometer Reading: <input type="text" name="odometer" required></label>

        <h3>Exterior Checks</h3>
        <div class="checkbox-group">
            {% for item in exterior_checks %}
                <label><input type="checkbox" name="exterior_checks" value="{{ item }}"> {{ item }}</label>
            {% endfor %}
        </div>

        <h3>Interior Checks</h3>
        <div class="checkbox-group">
            {% for item in interior_checks %}
                <label><input type="checkbox" name="interior_checks" value="{{ item }}"> {{ item }}</label>
            {% endfor %}
        </div>

        <h3>Under the Hood</h3>
        <div class="checkbox-group">
            {% for item in under_hood_checks %}
                <label><input type="checkbox" name="under_hood_checks" value="{{ item }}"> {{ item }}</label>
            {% endfor %}
        </div>

        <h3>Safety Equipment</h3>
        <div class="checkbox-group">
            {% for item in safety_equipment %}
                <label><input type="checkbox" name="safety_equipment" value="{{ item }}"> {{ item }}</label>
            {% endfor %}
        </div>

        <label>Any issues found:<textarea name="issues_found"></textarea></label>
        <label>Action taken:<textarea name="action_taken"></textarea></label>
        <label>Signature: <input type="text" name="signature" required></label>

        <button type="submit">Submit Checklist</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def checklist():
    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name"),
            "date": request.form.get("date"),
            "vehicle_reg": request.form.get("vehicle_reg"),
            "odometer": request.form.get("odometer"),
            "exterior_checks": request.form.getlist("exterior_checks"),
            "interior_checks": request.form.getlist("interior_checks"),
            "under_hood_checks": request.form.getlist("under_hood_checks"),
            "safety_equipment": request.form.getlist("safety_equipment"),
            "issues_found": request.form.get("issues_found"),
            "action_taken": request.form.get("action_taken"),
            "signature": request.form.get("signature")
        }
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{data['vehicle_reg']}.json"
        with open(os.path.join(SUBMISSIONS_DIR, filename), "w") as f:
            json.dump(data, f, indent=4)
        return redirect("/")
    
    return render_template_string(FORM_TEMPLATE,
        exterior_checks=[
            "Tyres", "Lights", "Mirrors", "Windshield & Windows", "Wipers & Washer Fluid",
            "Body Damage", "License Plates"
        ],
        interior_checks=[
            "Seatbelts", "Dashboard Warning Lights", "Horn", "Air Conditioning / Heater", "Cleanliness"
        ],
        under_hood_checks=[
            "Engine Oil Level", "Coolant Level", "Brake Fluid Level", "Battery Condition", "Belts & Hoses"
        ],
        safety_equipment=[
            "Fire Extinguisher", "First Aid Kit", "Emergency Triangle", "Spare Tyre & Jack"
        ]
    )
