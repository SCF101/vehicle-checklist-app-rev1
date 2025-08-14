import os
import json
from flask import Flask, request, render_template_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
os.makedirs("submissions", exist_ok=True)

form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Vehicle Checklist</title>
</head>
<body>
    <h2>Daily Vehicle Checklist</h2>
    <form method="POST">
        <label>Full Name:</label><br>
        <input type="text" name="full_name" required><br><br>

        <label>Date:</label><br>
        <input type="date" name="date" required><br><br>

        <label>Vehicle Registration Number:</label><br>
        <input type="text" name="vehicle_reg" required><br><br>

        <label>Checklist Items:</label><br>
        <input type="checkbox" name="tyres"> Tyres<br>
        <input type="checkbox" name="lights"> Lights<br>
        <input type="checkbox" name="mirrors"> Mirrors<br>
        <input type="checkbox" name="windows"> Windows<br>
        <input type="checkbox" name="wipers"> Wipers<br><br>

        <label>Notes:</label><br>
        <textarea name="notes" rows="4" cols="50"></textarea><br><br>

        <input type="submit" value="Submit Checklist">
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
            "tyres": "checked" if request.form.get("tyres") else "unchecked",
            "lights": "checked" if request.form.get("lights") else "unchecked",
            "mirrors": "checked" if request.form.get("mirrors") else "unchecked",
            "windows": "checked" if request.form.get("windows") else "unchecked",
            "wipers": "checked" if request.form.get("wipers") else "unchecked",
            "notes": request.form.get("notes")
        }

        filename = f"submissions/{data['full_name'].replace(' ', '_')}_{data['date']}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        # Send email notification
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        email_recipient = os.getenv("EMAIL_RECIPIENT")

        if sendgrid_api_key and email_recipient:
            message = Mail(
                from_email='noreply@vehiclechecklist.com',
                to_emails=email_recipient,
                subject='New Vehicle Checklist Submitted',
                plain_text_content=(
                    f"Checklist submitted by {data['full_name']} on {data['date']} "
                    f"for vehicle {data['vehicle_reg']}.
Notes: {data['notes']}"
                )
            )
            try:
                sg = SendGridAPIClient(sendgrid_api_key)
                sg.send(message)
            except Exception as e:
                print(f"SendGrid error: {e}")

        return "Checklist submitted successfully!"

    return render_template_string(form_html)

if __name__ == "__main__":
    app.run(debug=True)
