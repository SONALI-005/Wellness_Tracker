from datetime import datetime, timedelta
import random

class WellnessTracker:
    def __init__(self):
        self.focus_sessions = []
        self.breaks = []
        self.settings = {
            "microbreak_interval": 30,
            "focus_session_length": 50,
            "daily_work_limit": 8,
            "burnout_threshold": 70
        }
        self.session_start = datetime.now()
        self.total_interruptions = 0

    def start_focus_session(self):
        now = datetime.now()
        self.focus_sessions.append(now)
        return {"message": f"Focus session started at {now.strftime('%H:%M:%S')}"}

    def take_break(self):
        now = datetime.now()
        self.breaks.append(now)
        return {"message": f"Break taken at {now.strftime('%H:%M:%S')}"}

    def get_break_recommendation(self):
        now = datetime.now()
        last_break = self.breaks[-1] if self.breaks else self.session_start
        minutes_since_last_break = (now - last_break).total_seconds() / 60
        interval = self.settings["microbreak_interval"]

        if minutes_since_last_break > interval:
            return {
                "should_break": True,
                "minutes_overdue": minutes_since_last_break - interval,
                "exercise_suggestion": random.choice([
                    "Stretch your arms and shoulders",
                    "Do 5 squats",
                    "Walk around for 2 minutes",
                    "Look away from the screen and blink for 20 seconds"
                ])
            }
        else:
            return {
                "should_break": False,
                "next_break_in": interval - minutes_since_last_break
            }

    def calculate_burnout_risk(self):
        now = datetime.now()
        hours_worked_today = (now - self.session_start).total_seconds() / 3600
        ratio = hours_worked_today / self.settings["daily_work_limit"]
        burnout_risk = min(100, int(ratio * 100))

        message = "You're doing great!"
        if burnout_risk > 80:
            message = "High burnout risk! Please take a long break."
        elif burnout_risk > 60:
            message = "You're working hard. Consider pausing soon."
        elif burnout_risk > 30:
            message = "Stay balanced. Take microbreaks regularly."

        return {"burnout_risk": burnout_risk, "message": message}

    def get_focus_recovery_suggestion(self):
        suggestions = [
            {"title": "Box Breathing", "description": "Inhale for 4s, hold for 4s, exhale for 4s, hold for 4s. Repeat for 2 minutes."},
            {"title": "Quick Walk", "description": "Take a 5-minute brisk walk to reset your mind."},
            {"title": "Eye Exercise", "description": "Look at something 20 feet away for 20 seconds."},
            {"title": "Mini Meditation", "description": "Close your eyes and focus on your breath for 2 minutes."}
        ]
        return random.choice(suggestions)

    def get_stats(self):
        now = datetime.now()
        session_duration = (now - self.session_start).total_seconds() / 3600
        avg_focus_duration = self._average_focus_duration()
        burnout = self.calculate_burnout_risk()

        return {
            "session_duration": session_duration,
            "avg_focus_duration": avg_focus_duration,
            "burnout_risk": burnout["burnout_risk"],
            "total_interruptions": self.total_interruptions
        }

    def _average_focus_duration(self):
        if len(self.focus_sessions) < 2:
            return self.settings["focus_session_length"]
        total = 0
        for i in range(1, len(self.focus_sessions)):
            total += (self.focus_sessions[i] - self.focus_sessions[i - 1]).total_seconds()
        return (total / (len(self.focus_sessions) - 1)) / 60

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
