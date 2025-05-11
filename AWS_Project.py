import streamlit as st
import os
import json
from datetime import datetime, timedelta
import time
import random
from posture_detection import PostureDetector
from wellness_tracker import WellnessTracker

# Set page configuration
st.set_page_config(
    page_title="Developer Wellness Tracker",
    page_icon="🧘‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user data
if 'settings' not in st.session_state:
    st.session_state.settings = {
        "posture_alerts": True,
        "eye_strain_alerts": True,
        "microbreak_interval": 30,  # minutes
        "focus_session_length": 50,  # minutes
        "daily_work_limit": 8,  # hours
        "burnout_threshold": 70  # percentage
    }

if 'stats' not in st.session_state:
    st.session_state.stats = {
        "posture_corrections": 0,
        "breaks_taken": 0,
        "focus_sessions": 0,
        "last_break_time": None,
    }

if 'wellness_tracker' not in st.session_state:
    st.session_state.wellness_tracker = WellnessTracker()

if 'posture_detector' not in st.session_state:
    st.session_state.posture_detector = None

# Navigation
def navigation():
    st.sidebar.title("Developer Wellness")
    page = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Settings"])
    return page

# Home page
def home_page():
    st.title("Developer Wellness Tracker")
    st.subheader("Stay healthy while coding")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Features
        - 🧘‍♂️ Posture detection and alerts
        - 👁️ Eye strain prevention
        - ⏱️ Microbreak reminders
        - 🎯 Focus session tracking
        - 🔥 Burnout risk calculation
        """)
        
        if st.button("Start Focus Session"):
            result = st.session_state.wellness_tracker.start_focus_session()
            st.session_state.stats["focus_sessions"] += 1
            st.success(result["message"])
            
        if st.button("Take a Break"):
            result = st.session_state.wellness_tracker.take_break()
            st.session_state.stats["breaks_taken"] += 1
            st.session_state.stats["last_break_time"] = datetime.now().isoformat()
            st.success(result["message"])
    
    with col2:
        st.markdown("### Wellness Status")
        
        # Get break recommendation
        break_rec = st.session_state.wellness_tracker.get_break_recommendation()
        
        if break_rec["should_break"]:
            st.warning(f"⚠️ Break overdue by {break_rec['minutes_overdue']:.1f} minutes!")
            st.info(f"Suggestion: {break_rec['exercise_suggestion']}")
        else:
            st.info(f"Next break in {break_rec['next_break_in']:.1f} minutes")
        
        # Get burnout risk
        burnout_risk = st.session_state.wellness_tracker.calculate_burnout_risk()
        
        risk_color = "green"
        if burnout_risk["burnout_risk"] > 30:
            risk_color = "yellow"
        if burnout_risk["burnout_risk"] > 60:
            risk_color = "orange"
        if burnout_risk["burnout_risk"] > 80:
            risk_color = "red"
            
        st.markdown(f"**Burnout Risk:** <span style='color:{risk_color};'>{burnout_risk['burnout_risk']}%</span>", unsafe_allow_html=True)
        st.markdown(f"*{burnout_risk['message']}*")
        
        # Focus recovery suggestion
        if st.button("Get Focus Recovery Suggestion"):
            suggestion = st.session_state.wellness_tracker.get_focus_recovery_suggestion()
            st.info(f"**{suggestion['title']}**: {suggestion['description']}")

# Dashboard page
def dashboard_page():
    st.title("Wellness Dashboard")
    
    # Get stats
    stats = st.session_state.wellness_tracker.get_stats()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Focus Sessions", st.session_state.stats["focus_sessions"])
    with col2:
        st.metric("Breaks Taken", st.session_state.stats["breaks_taken"])
    with col3:
        st.metric("Posture Corrections", st.session_state.stats["posture_corrections"])
    with col4:
        st.metric("Burnout Risk", f"{stats['burnout_risk']:.0f}%")
    
    # Session details
    st.subheader("Session Details")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Session Duration:** {stats['session_duration']:.2f} hours")
        st.markdown(f"**Average Focus Duration:** {stats['avg_focus_duration']:.2f} minutes")
    
    with col2:
        st.markdown(f"**Total Interruptions:** {stats['total_interruptions']}")
        last_break = "Never" if not st.session_state.stats["last_break_time"] else datetime.fromisoformat(st.session_state.stats["last_break_time"]).strftime("%H:%M:%S")
        st.markdown(f"**Last Break:** {last_break}")
    
    # Posture detection section
    st.subheader("Posture Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.posture_detector is None or not st.session_state.posture_detector.is_running:
            if st.button("Start Posture Detection"):
                # In a real implementation, this would use the webcam
                # For this demo, we'll just simulate it
                st.session_state.posture_detector = PostureDetector()
                
                def alert_callback(alert_type, data):
                    if alert_type == "posture" and data.get('alert'):
                        st.session_state.stats["posture_corrections"] += 1
                
                st.session_state.posture_detector.start(callback=alert_callback)
                st.success("Posture detection started!")
        else:
            if st.button("Stop Posture Detection"):
                st.session_state.posture_detector.stop()
                st.session_state.posture_detector = None
                st.success("Posture detection stopped!")
    
    with col2:
        # Simulate posture detection for demo purposes
        if st.button("Simulate Bad Posture"):
            st.session_state.stats["posture_corrections"] += 1
            st.warning("Bad posture detected! Please sit up straight.")

# Settings page
def settings_page():
    st.title("Settings")
    
    with st.form("settings_form"):
        st.subheader("Alert Settings")
        posture_alerts = st.checkbox("Enable Posture Alerts", value=st.session_state.settings["posture_alerts"])
        eye_strain_alerts = st.checkbox("Enable Eye Strain Alerts", value=st.session_state.settings["eye_strain_alerts"])
        
        st.subheader("Time Settings")
        microbreak_interval = st.slider("Microbreak Interval (minutes)", 
                                       min_value=15, max_value=60, 
                                       value=st.session_state.settings["microbreak_interval"])
        
        focus_session_length = st.slider("Focus Session Length (minutes)", 
                                        min_value=25, max_value=90, 
                                        value=st.session_state.settings["focus_session_length"])
        
        daily_work_limit = st.slider("Daily Work Limit (hours)", 
                                    min_value=4, max_value=12, 
                                    value=st.session_state.settings["daily_work_limit"])
        
        burnout_threshold = st.slider("Burnout Risk Threshold (%)", 
                                     min_value=50, max_value=90, 
                                     value=st.session_state.settings["burnout_threshold"])
        
        submitted = st.form_submit_button("Save Settings")
        
        if submitted:
            # Update session state
            st.session_state.settings.update({
                "posture_alerts": posture_alerts,
                "eye_strain_alerts": eye_strain_alerts,
                "microbreak_interval": microbreak_interval,
                "focus_session_length": focus_session_length,
                "daily_work_limit": daily_work_limit,
                "burnout_threshold": burnout_threshold
            })
            
            # Update wellness tracker settings
            st.session_state.wellness_tracker.update_settings({
                "microbreak_interval": microbreak_interval,
                "focus_session_length": focus_session_length,
                "daily_work_limit": daily_work_limit,
                "burnout_threshold": burnout_threshold
            })
            
            st.success("Settings saved successfully!")

# Main app
def main():
    page = navigation()
    
    if page == "Home":
        home_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()