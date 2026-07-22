"""
Utility functions for the Cyber Hygiene Checker
"""

import re
import hashlib

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password):
    """Hash a password for checking against breach databases"""
    return hashlib.sha1(password.encode()).hexdigest().upper()

def get_time_since_last_check():
    """Get days since last security check"""
    # Implementation would read from config
    return 0

def display_security_tips():
    """Display random security tips"""
    tips = [
        "Use unique passwords for every account",
        "Enable 2FA everywhere possible",
        "Keep all software updated",
        "Be cautious of phishing emails",
        "Use a VPN on public WiFi",
        "Regularly backup your data",
        "Review social media privacy settings",
        "Use a password manager"
    ]
    import random
    return random.choice(tips)
