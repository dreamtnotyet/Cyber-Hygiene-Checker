"""
Score Tracker Module
Saves and displays historical security scores
"""

import json
import os
from datetime import datetime

class ScoreTracker:
    def __init__(self):
        self.history_file = "history/scores.json"
        os.makedirs("history", exist_ok=True)
        
    def save_score(self, score):
        """Save a score to history"""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
            
        history.append({
            'date': datetime.now().isoformat(),
            'score': score
        })
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    def show_history(self):
        """Display score history"""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                
            if not history:
                print("\n📊 No score history yet. Run a security check first!")
                return
                
            print("\n" + "="*60)
            print("📊 SECURITY SCORE HISTORY")
            print("="*60)
            
            for entry in history[-10:]:  # Show last 10 entries
                date = datetime.fromisoformat(entry['date'])
                score = entry['score']
                
                # Color code
                if score >= 80:
                    emoji = "🟢"
                elif score >= 60:
                    emoji = "🟡"
                elif score >= 40:
                    emoji = "🟠"
                else:
                    emoji = "🔴"
                    
                print(f"{emoji} {date.strftime('%B %d, %Y')}: {score}/100")
                
            # Show trend
            if len(history) >= 2:
                scores = [h['score'] for h in history]
                if scores[-1] > scores[0]:
                    print(f"\n📈 Trending UP! (+{scores[-1] - scores[0]} points)")
                elif scores[-1] < scores[0]:
                    print(f"\n📉 Trending DOWN! ({scores[-1] - scores[0]} points)")
                else:
                    print("\n➖ No change in overall score")
                    
        except FileNotFoundError:
            print("\n📊 No score history yet. Run a security check first!")
