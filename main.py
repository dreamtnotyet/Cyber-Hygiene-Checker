#!/usr/bin/env python3
"""
Cyber Hygiene Checker - Your Personal Security Assistant
A beginner-friendly tool to assess and improve your online security
"""

import json
import sys
from datetime import datetime
from security_checker import SecurityChecker
from report_generator import ReportGenerator
from score_tracker import ScoreTracker
import os

class CyberHygieneChecker:
    def __init__(self):
        self.checker = SecurityChecker()
        self.reporter = ReportGenerator()
        self.tracker = ScoreTracker()
        self.results = {}
        
    def run_full_check(self):
        """Run all security checks"""
        print("\n" + "="*60)
        print("🔒 CYBER HYGIENE CHECKER")
        print("="*60)
        print("\nChecking your digital security posture...\n")
        
        # Run all checks
        self.results = {
            'password_health': self.checker.check_password_health(),
            'email_exposure': self.checker.check_email_exposure(),
            'browser_security': self.checker.check_browser_security(),
            'software_updates': self.checker.check_software_updates(),
            'two_factor_usage': self.checker.check_2fa_status(),
            'backup_status': self.checker.check_backup_status(),
            'social_media_privacy': self.checker.check_social_media_privacy()
        }
        
        # Calculate overall score
        self.results['overall_score'] = self._calculate_score()
        
        # Save to history
        self.tracker.save_score(self.results['overall_score'])
        
        # Generate report
        self.reporter.generate_report(self.results)
        
        # Display summary
        self._display_summary()
        
    def _calculate_score(self):
        """Calculate overall security score (0-100)"""
        weights = {
            'password_health': 25,
            'two_factor_usage': 20,
            'browser_security': 15,
            'email_exposure': 15,
            'software_updates': 10,
            'backup_status': 10,
            'social_media_privacy': 5
        }
        
        score = 0
        for check, weight in weights.items():
            if check not in self.results:
                continue
            data = self.results[check]
            if isinstance(data, dict):
                if 'status' in data:
                    status = data['status'].lower()
                    status_score = {
                        'excellent': weight,
                        'good': weight * 0.75,
                        'fair': weight * 0.5,
                        'poor': weight * 0.25,
                        'critical': 0
                    }
                    score += status_score.get(status, weight * 0.5)
                elif 'has_2fa' in data:
                    if data.get('has_2fa') and data.get('important_accounts_2fa'):
                        score += weight
                    elif data.get('has_2fa'):
                        score += weight * 0.5
                elif 'has_backups' in data:
                    if data.get('has_backups') and data.get('has_offsite_backup'):
                        score += weight
                    elif data.get('has_backups'):
                        score += weight * 0.5
                elif 'has_adblocker' in data:
                    if data.get('has_adblocker') and data.get('has_security_extensions'):
                        score += weight
                    elif data.get('has_adblocker') or data.get('has_security_extensions'):
                        score += weight * 0.6
                    else:
                        score += weight * 0.3
                elif 'exposed' in data:
                    if not data.get('exposed'):
                        score += weight
                    else:
                        score += weight * 0.2
                elif 'os_updated' in data:
                    if data.get('os_updated') and data.get('apps_updated'):
                        score += weight
                    elif data.get('os_updated') or data.get('apps_updated'):
                        score += weight * 0.6
                    else:
                        score += weight * 0.2
                elif 'privacy_settings' in data:
                    if data.get('privacy_settings') == 'private' and not data.get('shares_location'):
                        score += weight
                    elif data.get('privacy_settings') == 'private':
                        score += weight * 0.6
                    else:
                        score += weight * 0.3
                else:
                    score += weight * 0.5
            elif isinstance(data, bool):
                score += weight if data else 0
            elif isinstance(data, str):
                status_score = {
                    'excellent': weight,
                    'good': weight * 0.75,
                    'fair': weight * 0.5,
                    'poor': weight * 0.25,
                    'critical': 0
                }
                score += status_score.get(data.lower(), weight * 0.5)
            elif isinstance(data, (int, float)):
                score += (data / 100) * weight
        return round(score)
        
    def _display_summary(self):
        """Display quick summary in terminal"""
        score = self.results['overall_score']
        
        # Color-coded score
        if score >= 80:
            emoji = "🟢"
            grade = "Excellent!"
        elif score >= 60:
            emoji = "🟡"
            grade = "Good, but room for improvement"
        elif score >= 40:
            emoji = "🟠"
            grade = "Needs attention"
        else:
            emoji = "🔴"
            grade = "Critical - Take action now!"
            
        print("\n" + "="*60)
        print(f"{emoji} SECURITY SCORE: {score}/100 - {grade}")
        print("="*60)
        
        # Show top issues
        issues = self.reporter.get_priority_issues(self.results)
        if issues:
            print("\n⚠️  TOP PRIORITY ISSUES:")
            for issue in issues[:3]:
                print(f"   • {issue}")
        else:
            print("\n✅ No critical issues found! Great job!")
            
        print(f"\n📄 Full report saved to: reports/security_report_{datetime.now().strftime('%Y%m%d')}.html")
        print(f"📊 Score history saved to: history/scores.json")
        print("\n💡 Tip: Run this weekly to track your security progress!\n")

def main():
    checker = CyberHygieneChecker()
    
    print("")
    print("    ╔═══════════════════════════════════════╗")
    print("    ║   Cyber Hygiene Checker v1.0         ║")
    print("    ║   Your Personal Security Assistant   ║")
    print("    ╚═══════════════════════════════════════╝")
    print("")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Run full security check")
        print("2. View historical scores")
        print("3. View last report")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            checker.run_full_check()
        elif choice == '2':
            checker.tracker.show_history()
        elif choice == '3':
            checker.reporter.open_last_report()
        elif choice == '4':
            print("\n👋 Stay safe online! Remember to check regularly.\n")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
