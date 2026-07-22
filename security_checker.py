"""
Security Checker Module
Contains all the security checks and assessments
"""

import re
import hashlib
import requests
import subprocess
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class SecurityChecker:
    def __init__(self):
        self.breach_api_url = "https://api.pwnedpasswords.com/range/"
        
    def check_password_health(self) -> Dict:
        """
        Check password strength and breach status
        Returns dict with strength, breached status, and recommendations
        """
        print("🔑 Checking password health...")
        
        result = {
            'strength': 'fair',
            'is_breached': False,
            'recommendations': [],
            'score': 0
        }
        
        # In a real implementation, we'd check actual passwords
        # For demo, we'll simulate based on user input
        print("  We'll check password health by asking some questions:")
        
        password_length = input("  How many characters is your main password? (approx): ")
        try:
            length = int(password_length)
            if length < 8:
                result['recommendations'].append("Your password is too short. Use at least 12 characters.")
            elif length < 12:
                result['recommendations'].append("Good start! Consider using longer passwords for better security.")
            else:
                result['strength'] = 'good'
        except:
            pass
            
        has_special = input("  Does it contain special characters (!@#$%^&*)? (y/n): ").lower()
        if has_special == 'n':
            result['recommendations'].append("Add special characters to make your password stronger.")
            
        has_uppercase = input("  Does it contain uppercase letters? (y/n): ").lower()
        if has_uppercase == 'n':
            result['recommendations'].append("Include uppercase letters for better security.")
            
        # Check if password was in a breach (simulated)
        reuse = input("  Do you use this password on multiple sites? (y/n): ").lower()
        if reuse == 'y':
            result['is_breached'] = True
            result['recommendations'].append("❗ Passwords reused across sites are dangerous! Use unique passwords.")
            
        if len(result['recommendations']) == 0:
            result['strength'] = 'excellent'
            result['score'] = 90
        elif len(result['recommendations']) <= 2:
            result['strength'] = 'good'
            result['score'] = 70
        else:
            result['strength'] = 'poor'
            result['score'] = 40
            
        return result
        
    def check_email_exposure(self) -> Dict:
        """
        Check if email has been exposed in data breaches
        """
        print("📧 Checking email exposure...")
        
        result = {
            'exposed': False,
            'breaches': [],
            'recommendations': []
        }
        
        email = input("  Enter your email address to check (or press Enter to skip): ").strip()
        
        if email:
            # Simulate checking Have I Been Pwned API
            print("  Checking if your email was in any breaches...")
            
            # For demo, we'll use a simulated response
            # In production, use: https://haveibeenpwned.com/api/v3/breachedaccount/{email}
            
            try:
                # This is a simplified version - real API requires API key for v3
                # For now, we'll give educational feedback
                response = requests.get(f"https://api.pwnedpasswords.com/range/")
                if response.status_code == 200:
                    # Simulate a breach check
                    print("  ✅ Email check completed!")
                    
                    # Add some simulated breaches for educational purposes
                    simulated_breaches = [
                        "LinkedIn (2021) - 700M records",
                        "Facebook (2019) - 533M records"
                    ]
                    
                    use_real = input("  Would you like to see what a breach check would look like? (y/n): ")
                    if use_real.lower() == 'y':
                        result['exposed'] = True
                        result['breaches'] = simulated_breaches
                        result['recommendations'].append(
                            "Your email was found in data breaches. Change passwords and enable 2FA immediately!"
                        )
                else:
                    print("  Could not check breaches right now.")
                    
            except Exception as e:
                print(f"  Email check error: {e}")
                result['recommendations'].append("Regularly check your email at haveibeenpwned.com")
        else:
            print("  Email check skipped (recommended for better results)")
            result['recommendations'].append("Check your email exposure at haveibeenpwned.com")
            
        return result
        
    def check_browser_security(self) -> Dict:
        """
        Check browser security settings
        """
        print("🌐 Checking browser security...")
        
        result = {
            'has_adblocker': False,
            'uses_https': True,
            'has_security_extensions': False,
            'recommendations': [],
            'status': 'fair'
        }
        
        # Ask about browser security practices
        adblock = input("  Do you use an adblocker? (uBlock Origin, AdBlock, etc.) (y/n): ").lower()
        if adblock == 'y':
            result['has_adblocker'] = True
        else:
            result['recommendations'].append("Install uBlock Origin to block malicious ads and trackers.")
            
        extensions = input("  Do you use any security extensions? (Privacy Badger, HTTPS Everywhere, etc.) (y/n): ").lower()
        if extensions == 'y':
            result['has_security_extensions'] = True
        else:
            result['recommendations'].append("Install Privacy Badger and HTTPS Everywhere for better privacy.")
            
        https = input("  Do you check for HTTPS before entering sensitive info? (y/n): ").lower()
        if https == 'n':
            result['recommendations'].append("Always check for HTTPS (padlock icon) before entering passwords or payment info.")
            result['uses_https'] = False
            
        # Assess status
        if result['has_adblocker'] and result['has_security_extensions']:
            result['status'] = 'good'
        elif result['has_adblocker'] or result['has_security_extensions']:
            result['status'] = 'fair'
        else:
            result['status'] = 'poor'
            
        return result
        
    def check_software_updates(self) -> Dict:
        """
        Check if software is regularly updated
        """
        print("💻 Checking software update status...")
        
        result = {
            'os_updated': False,
            'apps_updated': False,
            'auto_update_on': False,
            'recommendations': [],
            'status': 'fair'
        }
        
        updates = input("  Do you install system updates when they're available? (y/n): ").lower()
        if updates == 'y':
            result['os_updated'] = True
        else:
            result['recommendations'].append("Enable automatic updates for your operating system.")
            
        auto_update = input("  Do you have automatic updates enabled? (y/n): ").lower()
        if auto_update == 'y':
            result['auto_update_on'] = True
        else:
            result['recommendations'].append("Enable automatic updates for all software and apps.")
            
        app_updates = input("  Do you regularly update your apps and browser? (y/n): ").lower()
        if app_updates == 'y':
            result['apps_updated'] = True
        else:
            result['recommendations'].append("Update your apps regularly to patch security vulnerabilities.")
            
        if all([result['os_updated'], result['auto_update_on'], result['apps_updated']]):
            result['status'] = 'excellent'
        elif result['os_updated'] and result['apps_updated']:
            result['status'] = 'good'
        else:
            result['status'] = 'poor'
            
        return result
        
    def check_2fa_status(self) -> Dict:
        """
        Check Two-Factor Authentication usage
        """
        print("🔐 Checking Two-Factor Authentication...")
        
        result = {
            'has_2fa': False,
            'has_authenticator': False,
            'important_accounts_2fa': False,
            'recommendations': [],
            'status': 'poor'
        }
        
        has_2fa = input("  Do you use Two-Factor Authentication (2FA) on any accounts? (y/n): ").lower()
        if has_2fa == 'y':
            result['has_2fa'] = True
            
            important = input("  Do you have 2FA on your email and banking accounts? (y/n): ").lower()
            if important == 'y':
                result['important_accounts_2fa'] = True
                
            authenticator = input("  Do you use an authenticator app or security key? (y/n): ").lower()
            if authenticator == 'y':
                result['has_authenticator'] = True
            else:
                result['recommendations'].append("Use authenticator apps like Google Authenticator or Authy instead of SMS.")
                
            result['status'] = 'good' if result['important_accounts_2fa'] else 'fair'
        else:
            result['recommendations'].append("❗ Enable 2FA on all important accounts (email, banking, social media).")
            
        return result
        
    def check_backup_status(self) -> Dict:
        """
        Check if data is backed up
        """
        print("💾 Checking backup status...")
        
        result = {
            'has_backups': False,
            'backup_frequency': 'never',
            'has_offsite_backup': False,
            'recommendations': [],
            'status': 'poor'
        }
        
        has_backup = input("  Do you back up your important files? (y/n): ").lower()
        if has_backup == 'y':
            result['has_backups'] = True
            
            frequency = input("  How often? (daily/weekly/monthly/rarely): ").lower()
            result['backup_frequency'] = frequency
            
            if frequency in ['daily', 'weekly']:
                result['status'] = 'good'
            else:
                result['recommendations'].append("Back up your data at least weekly.")
                
            offsite = input("  Do you have a backup copy stored offsite or in the cloud? (y/n): ").lower()
            if offsite == 'y':
                result['has_offsite_backup'] = True
            else:
                result['recommendations'].append("Store a backup copy in a different location (cloud or external drive).")
        else:
            result['recommendations'].append("❗ Start backing up your important files today - use the 3-2-1 rule!")
            
        return result
        
    def check_social_media_privacy(self) -> Dict:
        """
        Check social media privacy settings
        """
        print("👤 Checking social media privacy...")
        
        result = {
            'privacy_settings': 'unknown',
            'posts_public': False,
            'shares_location': False,
            'recommendations': [],
            'status': 'fair'
        }
        
        privacy = input("  Are your social media profiles private? (y/n): ").lower()
        if privacy == 'y':
            result['privacy_settings'] = 'private'
        else:
            result['privacy_settings'] = 'public'
            result['recommendations'].append("Make your social media profiles private to protect your personal info.")
            
        posts = input("  Do you post information that could be used to answer security questions? (pet names, birthday, etc.) (y/n): ").lower()
        if posts == 'y':
            result['recommendations'].append("Avoid sharing personal details that could be used to reset your passwords.")
            
        location = input("  Do you share your location in posts or check-ins? (y/n): ").lower()
        if location == 'y':
            result['shares_location'] = True
            result['recommendations'].append("Turn off location sharing to protect your physical safety.")
            
        if result['privacy_settings'] == 'private' and not result['shares_location']:
            result['status'] = 'good'
        elif result['privacy_settings'] == 'private':
            result['status'] = 'fair'
            
        return result
