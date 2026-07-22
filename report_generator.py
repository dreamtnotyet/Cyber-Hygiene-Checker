"""
Report Generator Module
Creates HTML reports from security check results
"""

import json
import os
from datetime import datetime
import webbrowser

class ReportGenerator:
    def __init__(self):
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
        
    def generate_report(self, results):
        """Generate an HTML report from check results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_report_{timestamp}.html"
        filepath = os.path.join(self.report_dir, filename)
        
        html_content = self._create_html_report(results)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
            
        print(f"✅ Report generated: {filepath}")
        return filepath
        
    def _create_html_report(self, results):
        """Create the HTML content for the report"""
        score = results.get('overall_score', 0)
        
        # Determine score color and emoji
        if score >= 80:
            color = "#4CAF50"
            emoji = "🟢"
            grade = "Excellent! You're a security superstar!"
        elif score >= 60:
            color = "#FFC107"
            emoji = "🟡"
            grade = "Good job! A few improvements could make you even safer."
        elif score >= 40:
            color = "#FF9800"
            emoji = "🟠"
            grade = "Some areas need attention. Don't worry, we'll help!"
        else:
            color = "#f44336"
            emoji = "🔴"
            grade = "Critical improvements needed. Let's fix this now!"
            
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Hygiene Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #333;
        }}
        .score-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .score-circle {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: {color};
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .score-number {{
            font-size: 3em;
            font-weight: bold;
            color: white;
        }}
        .score-label {{
            color: white;
            font-size: 0.9em;
        }}
        .grade-text {{
            font-size: 1.3em;
            color: {color};
            font-weight: bold;
            margin-top: 15px;
        }}
        .check-item {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .check-item.good {{
            border-left-color: #4CAF50;
        }}
        .check-item.warning {{
            border-left-color: #FF9800;
        }}
        .check-item.critical {{
            border-left-color: #f44336;
        }}
        .check-title {{
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
        }}
        .check-status {{
            float: right;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .status-good {{
            background: #4CAF50;
            color: white;
        }}
        .status-fair {{
            background: #FFC107;
            color: #333;
        }}
        .status-poor {{
            background: #FF9800;
            color: white;
        }}
        .status-critical {{
            background: #f44336;
            color: white;
        }}
        .recommendations {{
            margin-top: 20px;
            background: #fff3cd;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #FF9800;
        }}
        .recommendations li {{
            margin: 10px 0;
            list-style: none;
        }}
        .recommendations li::before {{
            content: "💡 ";
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        .footer span {{
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Cyber Hygiene Report</h1>
            <p>Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="score-container">
            <div class="score-circle">
                <div class="score-number">{score}</div>
                <div class="score-label">/ 100</div>
            </div>
            <div class="grade-text">{emoji} {grade}</div>
        </div>
        
        <h2 style="margin-top: 30px;">📊 Detailed Assessment</h2>
"""
        
        # Add each check result
        checks = [
            ('password_health', 'Password Health', results.get('password_health', {})),
            ('email_exposure', 'Email Security', results.get('email_exposure', {})),
            ('browser_security', 'Browser Security', results.get('browser_security', {})),
            ('software_updates', 'Software Updates', results.get('software_updates', {})),
            ('two_factor_usage', 'Two-Factor Authentication', results.get('two_factor_usage', {})),
            ('backup_status', 'Backup Status', results.get('backup_status', {})),
            ('social_media_privacy', 'Social Media Privacy', results.get('social_media_privacy', {}))
        ]
        
        for key, title, data in checks:
            if not data:
                continue
                
            status = data.get('status', 'unknown')
            status_class = {
                'excellent': 'good',
                'good': 'good',
                'fair': 'warning',
                'poor': 'warning',
                'critical': 'critical'
            }.get(status, 'warning')
            
            status_label = {
                'excellent': 'Excellent',
                'good': 'Good',
                'fair': 'Fair',
                'poor': 'Poor',
                'critical': 'Critical'
            }.get(status, 'Unknown')
            
            status_badge = {
                'excellent': 'status-good',
                'good': 'status-good',
                'fair': 'status-fair',
                'poor': 'status-poor',
                'critical': 'status-critical'
            }.get(status, 'status-fair')
            
            html += f"""
        <div class="check-item {status_class}">
            <div class="check-title">
                {title}
                <span class="check-status {status_badge}">{status_label}</span>
            </div>
"""
            
            # Add specific details
            if key == 'password_health':
                strength = data.get('strength', 'unknown')
                if data.get('is_breached'):
                    html += '<p style="color: red;">⚠️ Password may have been exposed in a breach!</p>'
                html += f'<p>Strength: {strength.capitalize()}</p>'
                
            elif key == 'email_exposure':
                if data.get('exposed'):
                    html += '<p style="color: red;">⚠️ Email found in data breaches!</p>'
                    for breach in data.get('breaches', [])[:3]:
                        html += f'<p style="font-size: 0.9em;">• {breach}</p>'
                else:
                    html += '<p>✅ Email not found in known breaches</p>'
                    
            elif key == 'browser_security':
                html += f'<p>Adblocker: {"✅" if data.get("has_adblocker") else "❌"}</p>'
                html += f'<p>Security Extensions: {"✅" if data.get("has_security_extensions") else "❌"}</p>'
                
            elif key == 'software_updates':
                html += f'<p>OS Updates: {"✅" if data.get("os_updated") else "❌"}</p>'
                html += f'<p>App Updates: {"✅" if data.get("apps_updated") else "❌"}</p>'
                
            elif key == 'two_factor_usage':
                html += f'<p>2FA Enabled: {"✅" if data.get("has_2fa") else "❌"}</p>'
                if data.get('has_2fa'):
                    html += f'<p>Important Accounts: {"✅" if data.get("important_accounts_2fa") else "⚠️"}</p>'
                    
            elif key == 'backup_status':
                html += f'<p>Backups: {"✅" if data.get("has_backups") else "❌"}</p>'
                if data.get('has_backups'):
                    html += f'<p>Frequency: {data.get("backup_frequency", "unknown")}</p>'
                    
            elif key == 'social_media_privacy':
                html += f'<p>Privacy Settings: {data.get("privacy_settings", "unknown").capitalize()}</p>'
                html += f'<p>Location Sharing: {"⚠️ On" if data.get("shares_location") else "✅ Off"}</p>'
                
            html += '</div>'
            
        # Add recommendations section
        all_recommendations = []
        for key, title, data in checks:
            if data and 'recommendations' in data:
                all_recommendations.extend(data['recommendations'])
                
        if all_recommendations:
            html += """
        <div class="recommendations">
            <h3>🎯 Recommended Actions</h3>
            <ul>
"""
            for rec in all_recommendations[:10]:  # Limit to top 10
                html += f'                <li>{rec}</li>\n'
            html += """
            </ul>
        </div>
"""
            
        html += f"""
        <div class="footer">
            <p>Generated by <span>Cyber Hygiene Checker</span> | Stay safe online! 🔒</p>
            <p style="font-size: 0.8em; margin-top: 10px;">Disclaimer: This is an educational tool. Always consult security professionals for critical systems.</p>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    def get_priority_issues(self, results):
        """Extract top priority issues from results"""
        issues = []
        
        # Check each category for issues
        password = results.get('password_health', {})
        if password.get('is_breached'):
            issues.append("Your password may be in a data breach. Change it immediately!")
        if password.get('strength') == 'poor':
            issues.append("Your password is weak. Create a strong, unique password.")
            
        email = results.get('email_exposure', {})
        if email.get('exposed'):
            issues.append("Your email was found in data breaches. Enable 2FA and change passwords.")
            
        twofa = results.get('two_factor_usage', {})
        if not twofa.get('has_2fa'):
            issues.append("You're not using Two-Factor Authentication. Enable it on all important accounts.")
            
        backup = results.get('backup_status', {})
        if not backup.get('has_backups'):
            issues.append("You don't have any backups. Start backing up your important files today.")
            
        return issues
        
    def open_last_report(self):
        """Open the most recent report in browser"""
        reports = sorted([f for f in os.listdir(self.report_dir) if f.endswith('.html')])
        if reports:
            latest = os.path.join(self.report_dir, reports[-1])
            print(f"Opening: {latest}")
            webbrowser.open(latest)
        else:
            print("No reports found. Run a security check first.")
