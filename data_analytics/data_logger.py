import pandas as pd
import os
import datetime

class DataLogger:
    def __init__(self, log_dir='/home/ubuntu/minecraft_ai_bot/data_analytics/'):
        self.log_dir = log_dir
        self.log_file = os.path.join(self.log_dir, 'bot_data.csv')
        self.excel_file = os.path.join(self.log_dir, 'bot_analytics.xlsx')
        self.data_buffer = []
        os.makedirs(self.log_dir, exist_ok=True)

    def log_activity(self, timestamp, pos, action, goal, inventory_size, health):
        log_entry = {
            'timestamp': timestamp,
            'x': pos['x'],
            'y': pos['y'],
            'z': pos['z'],
            'action': action,
            'goal': goal,
            'inventory_size': inventory_size,
            'health': health
        }
        self.data_buffer.append(log_entry)
        
        # Save to CSV periodically
        if len(self.data_buffer) >= 10:
            self.save_to_csv()

    def save_to_csv(self):
        df = pd.DataFrame(self.data_buffer)
        if os.path.exists(self.log_file):
            df.to_csv(self.log_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.log_file, index=False)
        self.data_buffer = []
        print(f"Logged {len(df)} activities to {self.log_file}")

    def generate_spreadsheet(self):
        if not os.path.exists(self.log_file):
            return
        
        df = pd.read_csv(self.log_file)
        # Create an Excel file with some basic analytics
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Action summary
            action_summary = df['action'].value_counts().reset_index()
            action_summary.columns = ['Action', 'Count']
            action_summary.to_excel(writer, sheet_name='Action Summary', index=False)
            
            # Goal summary
            goal_summary = df['goal'].value_counts().reset_index()
            goal_summary.columns = ['Goal', 'Count']
            goal_summary.to_excel(writer, sheet_name='Goal Summary', index=False)

        print(f"Spreadsheet analytics generated at {self.excel_file}")
