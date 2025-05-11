from flask import Flask, render_template, request, jsonify, session
import os
import json
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# In-memory storage for user data (in a real app, use a database)
user_data = {
    "settings": {
        "posture_alerts": True,
        "eye_strain_alerts": True,
        "microbreak_interval": 30,  # minutes
        "focus_session_length": 50,  # minutes
    },
    "stats": {
        "posture_corrections": 0,
        "breaks_taken": 0,
        "focus_sessions": 0,
        "last_break_time": None,
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user_data=user_data)

@app.route('/settings')
def settings():
    return render_template('settings.html', settings=user_data["settings"])

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    if request.method == 'POST':
        data = request.json
        user_data["settings"].update(data)
        return jsonify({"status": "success"})
    return jsonify(user_data["settings"])

@app.route('/api/stats', methods=['GET', 'POST'])
def api_stats():
    if request.method == 'POST':
        data = request.json
        user_data["stats"].update(data)
        return jsonify({"status": "success"})
    return jsonify(user_data["stats"])

@app.route('/api/posture-alert', methods=['POST'])
def posture_alert():
    # In a real app, this would process webcam data or receive processed results
    data = request.json
    if data.get('bad_posture', False):
        user_data["stats"]["posture_corrections"] += 1
    return jsonify({"status": "success"})

@app.route('/api/break-taken', methods=['POST'])
def break_taken():
    user_data["stats"]["breaks_taken"] += 1
    user_data["stats"]["last_break_time"] = datetime.now().isoformat()
    return jsonify({"status": "success"})

@app.route('/api/focus-session', methods=['POST'])
def focus_session():
    user_data["stats"]["focus_sessions"] += 1
    return jsonify({"status": "success"})

@app.route('/api/ide-activity', methods=['POST'])
def ide_activity():
    # Process IDE activity data for burnout detection
    # This would integrate with IDE extensions in a real app
    data = request.json
    # Process and store activity data
    return jsonify({"status": "success", "burnout_risk": calculate_burnout_risk(data)})

def calculate_burnout_risk(activity_data):
    # Simple algorithm to calculate burnout risk
    # In a real app, this would be more sophisticated
    hours = activity_data.get('hours_active', 0)
    intensity = activity_data.get('typing_intensity', 0)
    late_night = activity_data.get('late_night_coding', False)
    
    risk = min(100, hours * 5 + intensity * 3 + (30 if late_night else 0))
    return risk

if __name__ == '__main__':
    app.run(debug=True)