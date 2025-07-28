#!/usr/bin/env python3
"""
Script to fix multiple active duty log sessions for the same guard
"""

import sqlite3
from datetime import datetime

def fix_multiple_active_sessions():
    """Fix multiple active duty log sessions by closing older ones"""
    conn = sqlite3.connect('security_portal.db')
    cursor = conn.cursor()
    
    # Find guards with multiple active sessions
    cursor.execute('''
        SELECT guard_id, COUNT(*) as active_count
        FROM duty_logs 
        WHERE logout_time IS NULL 
        GROUP BY guard_id 
        HAVING COUNT(*) > 1
    ''')
    
    guards_with_multiple_active = cursor.fetchall()
    
    if not guards_with_multiple_active:
        print("No guards with multiple active sessions found.")
        conn.close()
        return 0
    
    print(f"Found {len(guards_with_multiple_active)} guards with multiple active sessions:")
    
    total_fixed = 0
    
    for guard_id, active_count in guards_with_multiple_active:
        print(f"\nGuard ID {guard_id} has {active_count} active sessions")
        
        # Get all active sessions for this guard, ordered by login time (newest first)
        cursor.execute('''
            SELECT id, login_time 
            FROM duty_logs 
            WHERE guard_id = ? AND logout_time IS NULL 
            ORDER BY login_time DESC
        ''', (guard_id,))
        
        active_sessions = cursor.fetchall()
        
        # Keep the most recent session active, close the others
        for i, (session_id, login_time) in enumerate(active_sessions):
            if i == 0:  # Keep the first (most recent) session active
                print(f"  Keeping session {session_id} (login: {login_time}) as active")
                continue
            
            # Close older sessions
            try:
                # Parse login time to calculate a reasonable logout time
                if 'T' in login_time:
                    login_dt = datetime.fromisoformat(login_time.replace('T', ' '))
                else:
                    login_dt = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
                
                # Set logout time to 1 minute after login (minimal session)
                logout_dt = login_dt.replace(minute=login_dt.minute + 1)
                logout_time_str = logout_dt.strftime('%Y-%m-%d %H:%M:%S')
                duration_minutes = 1  # Minimal 1-minute session
                
                cursor.execute('''
                    UPDATE duty_logs 
                    SET logout_time = ?, duration_minutes = ?
                    WHERE id = ?
                ''', (logout_time_str, duration_minutes, session_id))
                
                print(f"  Closed session {session_id} (login: {login_time}) with 1-minute duration")
                total_fixed += 1
                
            except Exception as e:
                print(f"  Error closing session {session_id}: {e}")
                continue
    
    conn.commit()
    conn.close()
    
    print(f"\nFixed {total_fixed} overlapping active sessions.")
    return total_fixed

def verify_fix():
    """Verify that the fix worked by checking for remaining multiple active sessions"""
    conn = sqlite3.connect('security_portal.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT guard_id, COUNT(*) as active_count
        FROM duty_logs 
        WHERE logout_time IS NULL 
        GROUP BY guard_id 
        HAVING COUNT(*) > 1
    ''')
    
    remaining_issues = cursor.fetchall()
    conn.close()
    
    if remaining_issues:
        print(f"WARNING: {len(remaining_issues)} guards still have multiple active sessions!")
        return False
    else:
        print("✅ All guards now have at most one active session.")
        return True

if __name__ == '__main__':
    print("=== Fixing Multiple Active Duty Sessions ===\n")
    fixed_count = fix_multiple_active_sessions()
    print("\n=== Verification ===")
    verify_fix()
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} overlapping active sessions.")
    else:
        print("\n✅ No issues found to fix.")
