#!/usr/bin/env python3
"""
Script to fix incorrect duration calculations in the duty_logs table
"""

import sqlite3
from datetime import datetime

def fix_duty_log_durations():
    """Fix incorrect duration calculations in existing duty log entries"""
    conn = sqlite3.connect('security_portal.db')
    cursor = conn.cursor()
    
    # Get all duty logs with logout times and duration
    cursor.execute('''
        SELECT id, login_time, logout_time, duration_minutes 
        FROM duty_logs 
        WHERE logout_time IS NOT NULL AND duration_minutes IS NOT NULL
    ''')
    
    records = cursor.fetchall()
    fixed_count = 0
    
    print(f"Found {len(records)} duty log entries to check...")
    
    for record in records:
        log_id, login_time_str, logout_time_str, current_duration = record
        
        try:
            # Parse login and logout times
            if 'T' in login_time_str:
                login_time = datetime.fromisoformat(login_time_str.replace('T', ' '))
            else:
                login_time = datetime.strptime(login_time_str, '%Y-%m-%d %H:%M:%S')
                
            if 'T' in logout_time_str:
                logout_time = datetime.fromisoformat(logout_time_str.replace('T', ' '))
            else:
                logout_time = datetime.strptime(logout_time_str, '%Y-%m-%d %H:%M:%S')
            
            # Calculate correct duration
            duration_seconds = (logout_time - login_time).total_seconds()
            correct_duration = max(0, int(duration_seconds / 60))
            
            # Only update if duration is significantly different (more than 1 minute off)
            if abs(current_duration - correct_duration) > 1:
                cursor.execute('''
                    UPDATE duty_logs 
                    SET duration_minutes = ? 
                    WHERE id = ?
                ''', (correct_duration, log_id))
                
                print(f"Fixed log ID {log_id}: {current_duration} min -> {correct_duration} min")
                fixed_count += 1
                
        except Exception as e:
            print(f"Error processing log ID {log_id}: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\nFixed {fixed_count} duty log entries with incorrect durations.")
    return fixed_count

if __name__ == '__main__':
    fix_duty_log_durations()
