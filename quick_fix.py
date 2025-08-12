#!/usr/bin/env python3
"""
Quick Fix Script for Frappe LMS
Automatically fixes common issues based on health check results
"""

import subprocess
import sys
import time
import requests
import os

def run_command(cmd, description=""):
    """Run a shell command and return result"""
    print(f"⚡ Running: {description if description else cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Success: {description}")
            return True, result.stdout
        else:
            print(f"✗ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, str(e)

def check_port(port):
    """Check if a port is open"""
    try:
        response = requests.get(f"http://127.0.0.1:{port}", timeout=3)
        return True
    except:
        return False

def fix_mariadb():
    """Fix MariaDB issues"""
    print("\n🔧 FIXING MARIADB")
    print("=" * 50)
    
    # Check if MariaDB is running
    success, _ = run_command("sudo service mariadb status", "Check MariaDB status")
    if not success:
        print("Starting MariaDB...")
        run_command("sudo service mariadb start", "Start MariaDB")
        time.sleep(3)
    
    # Check if we can connect to database
    os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
    success, _ = run_command("bench --site lms.local execute \"frappe.db.sql('SELECT 1')\"", "Test database connection")
    if not success:
        print("Database connection failed - attempting to fix...")
        run_command("bench --site lms.local migrate", "Run database migration")
        run_command("bench --site lms.local execute \"frappe.db.sql('SELECT 1')\"", "Verify database connection")

def fix_cache_issues():
    """Clear all caches and rebuild"""
    print("\n🔧 FIXING CACHE & BUILD ISSUES")
    print("=" * 50)
    
    os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
    
    # Clear caches
    run_command("bench clear-cache", "Clear Frappe cache")
    run_command("bench clear-website-cache", "Clear website cache")
    
    # Rebuild assets
    run_command("bench build", "Rebuild assets")
    
def fix_permissions():
    """Fix file permissions"""
    print("\n🔧 FIXING PERMISSIONS")
    print("=" * 50)
    
    os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
    run_command("bench set-config allow_tests true", "Allow tests")
    run_command("bench setup requirements", "Setup requirements")

def restart_services():
    """Restart all Frappe services"""
    print("\n🔧 RESTARTING SERVICES")
    print("=" * 50)
    
    # Kill any hanging processes
    run_command("pkill -f 'bench start'", "Kill existing bench processes")
    time.sleep(2)
    
    # Restart MariaDB
    run_command("sudo service mariadb restart", "Restart MariaDB")
    time.sleep(3)
    
    print("✓ Services restart initiated. Run 'bench start' to start LMS services.")

def main():
    print("🚀 FRAPPE LMS QUICK FIX")
    print("=" * 50)
    print("This script will attempt to fix common issues automatically.")
    print()
    
    if len(sys.argv) > 1:
        fix_type = sys.argv[1].lower()
    else:
        print("Available fixes:")
        print("  python3 quick_fix.py all       - Run all fixes")
        print("  python3 quick_fix.py db        - Fix database issues")
        print("  python3 quick_fix.py cache     - Clear cache and rebuild")
        print("  python3 quick_fix.py perms     - Fix permissions")
        print("  python3 quick_fix.py restart   - Restart services")
        print()
        fix_type = input("Enter fix type (or 'all'): ").lower()
    
    start_time = time.time()
    
    if fix_type == "all":
        fix_mariadb()
        fix_cache_issues()
        fix_permissions()
        restart_services()
    elif fix_type == "db":
        fix_mariadb()
    elif fix_type == "cache":
        fix_cache_issues()
    elif fix_type == "perms":
        fix_permissions()
    elif fix_type == "restart":
        restart_services()
    else:
        print(f"❌ Unknown fix type: {fix_type}")
        return
    
    elapsed = time.time() - start_time
    print(f"\n✅ QUICK FIX COMPLETE - {elapsed:.1f}s")
    print("Run health_check.py to verify fixes.")

if __name__ == "__main__":
    main()
