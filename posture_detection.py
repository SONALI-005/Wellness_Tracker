import cv2
import numpy as np
import time
from threading import Thread
import streamlit as st

class PostureDetector:
    """
    A class for detecting poor posture and eye strain using webcam.
    This is a simplified implementation that would be enhanced with actual AI models in production.
    Modified to work with Streamlit.
    """
    
    def __init__(self):
        self.is_running = False
        self.camera = None
        self.last_posture_check = time.time()
        self.last_eye_strain_check = time.time()
        self.posture_check_interval = 60  # seconds
        self.eye_strain_check_interval = 300  # seconds
        self.callback = None
        
    def start(self, callback=None):
        """Start the posture detection process"""
        if self.is_running:
            return False
            
        self.callback = callback
        self.is_running = True
        
        # In Streamlit, we'll use a different approach for camera access
        # For demo purposes, we'll simulate camera access
        # self.camera = cv2.VideoCapture(0)
        self.camera = True  # Simulate camera being active
        
        # Start detection in a separate thread to not block the main application
        Thread(target=self._detection_loop).start()
        return True
        
    def stop(self):
        """Stop the posture detection process"""
        self.is_running = False
        if self.camera:
            # In a real implementation with OpenCV:
            # self.camera.release()
            self.camera = None
            
    def _detection_loop(self):
        """Main detection loop running in a separate thread"""
        while self.is_running and self.camera:
            # In Streamlit, we'll simulate frame capture
            # ret, frame = self.camera.read()
            frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Dummy frame
            
            current_time = time.time()
            
            # Check posture periodically
            if current_time - self.last_posture_check > self.posture_check_interval:
                posture_result = self._check_posture(frame)
                self.last_posture_check = current_time
                if self.callback and posture_result.get('alert'):
                    self.callback('posture', posture_result)
            
            # Check eye strain periodically
            if current_time - self.last_eye_strain_check > self.eye_strain_check_interval:
                eye_result = self._check_eye_strain(frame)
                self.last_eye_strain_check = current_time
                if self.callback and eye_result.get('alert'):
                    self.callback('eye_strain', eye_result)
                    
            # Don't hog the CPU
            time.sleep(0.1)
            
    def _check_posture(self, frame):
        """
        Check if the user has poor posture
        In a real implementation, this would use computer vision models
        to detect head position, shoulder alignment, etc.
        """
        # Placeholder for actual AI-based posture detection
        # This would analyze the frame for posture issues
        
        # Simulate detection (random for demo purposes)
        import random
        bad_posture = random.random() < 0.3  # 30% chance of detecting bad posture
        
        return {
            'alert': bad_posture,
            'message': 'Your posture needs correction' if bad_posture else 'Posture looks good',
            'confidence': random.uniform(0.7, 0.95)
        }
        
    def _check_eye_strain(self, frame):
        """
        Check for signs of eye strain
        In a real implementation, this would detect:
        - Distance from screen
        - Blink rate
        - Squinting
        """
        # Placeholder for actual AI-based eye strain detection
        
        # Simulate detection (random for demo purposes)
        import random
        eye_strain = random.random() < 0.2  # 20% chance of detecting eye strain
        
        return {
            'alert': eye_strain,
            'message': 'Take a break from the screen' if eye_strain else 'Eye health looks good',
            'confidence': random.uniform(0.7, 0.9)
        }
    
    def simulate_bad_posture(self):
        """
        Simulate a bad posture detection for demo purposes in Streamlit
        """
        posture_result = {
            'alert': True,
            'message': 'Your posture needs correction',
            'confidence': 0.85
        }
        
        if self.callback:
            self.callback('posture', posture_result)
        
        return posture_result
    
    def simulate_eye_strain(self):
        """
        Simulate eye strain detection for demo purposes in Streamlit
        """
        eye_result = {
            'alert': True,
            'message': 'Take a break from the screen',
            'confidence': 0.8
        }
        
        if self.callback:
            self.callback('eye_strain', eye_result)
        
        return eye_result


# Example usage
if __name__ == "__main__":
    def alert_callback(alert_type, data):
        print(f"{alert_type.upper()} ALERT: {data['message']}")
    
    detector = PostureDetector()
    detector.start(callback=alert_callback)
    
    try:
        # Run for 30 seconds as a test
        time.sleep(30)
    finally:
        detector.stop()