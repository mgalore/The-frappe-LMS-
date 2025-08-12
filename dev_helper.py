#!/usr/bin/env python3
"""
Development Helper Script for Frappe LMS
Quick commands for common development tasks
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description="", show_output=True):
    """Run a shell command"""
    print(f"🚀 {description if description else cmd}")
    try:
        if show_output:
            result = subprocess.run(cmd, shell=True, cwd="/workspaces/The-frappe-LMS-/lms-bench")
            return result.returncode == 0
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/workspaces/The-frappe-LMS-/lms-bench")
            return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def dev_start():
    """Start development environment"""
    print("🔥 Starting Frappe LMS Development Environment")
    print("=" * 50)
    
    # Ensure MariaDB is running
    print("1. Starting MariaDB...")
    os.system("sudo service mariadb start")
    time.sleep(2)
    
    # Start bench in background
    print("2. Starting Frappe services...")
    print("   Note: This will run in the background. Check with 'dev monitor'")
    os.system("cd /workspaces/The-frappe-LMS-/lms-bench && nohup bench start > /tmp/bench.log 2>&1 &")
    time.sleep(5)
    
    print("3. Checking services...")
    os.system("python3 /workspaces/The-frappe-LMS-/service_monitor.py")

def dev_stop():
    """Stop development environment"""
    print("🛑 Stopping Frappe LMS Development Environment")
    print("=" * 50)
    
    # Kill bench processes
    os.system("pkill -f 'bench start'")
    os.system("pkill -f 'redis-server'")
    os.system("pkill -f 'socketio'")
    print("✓ Stopped Frappe services")

def dev_restart():
    """Restart development environment"""
    print("🔄 Restarting Frappe LMS Development Environment")
    print("=" * 50)
    dev_stop()
    time.sleep(3)
    dev_start()

def dev_logs():
    """Show development logs"""
    print("📋 Recent logs from /tmp/bench.log:")
    print("=" * 50)
    try:
        with open("/tmp/bench.log", "r") as f:
            lines = f.readlines()
            for line in lines[-50:]:  # Last 50 lines
                print(line.rstrip())
    except FileNotFoundError:
        print("No log file found. Start services first with 'dev start'")

def dev_reset():
    """Reset development environment (nuclear option)"""
    print("☢️  RESETTING Development Environment")
    print("=" * 50)
    print("⚠️  This will:")
    print("   - Stop all services")
    print("   - Clear all caches")
    print("   - Rebuild assets")
    print("   - Restart MariaDB")
    print()
    
    confirm = input("Are you sure? Type 'yes' to continue: ")
    if confirm.lower() != 'yes':
        print("❌ Reset cancelled")
        return
    
    # Stop services
    dev_stop()
    
    # Reset database
    os.system("sudo service mariadb restart")
    time.sleep(3)
    
    # Clear caches and rebuild
    os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
    run_command("bench clear-cache", "Clearing cache")
    run_command("bench clear-website-cache", "Clearing website cache")
    run_command("bench build", "Rebuilding assets")
    
    print("✅ Reset complete! Run 'dev start' to restart services.")

def dev_test():
    """Run development tests"""
    print("🧪 Running Development Tests")
    print("=" * 50)
    
    os.chdir("/workspaces/The-frappe-LMS-")
    
    print("1. Health Check...")
    os.system("python3 health_check.py")
    
    print("\n2. Service Monitor...")
    os.system("python3 service_monitor.py")

def main():
    if len(sys.argv) < 2:
        print("🛠️  FRAPPE LMS DEVELOPMENT HELPER")
        print("=" * 50)
        print("Usage: python3 dev_helper.py <command>")
        print()
        print("Commands:")
        print("  start     - Start development environment")
        print("  stop      - Stop all services")
        print("  restart   - Restart all services")
        print("  logs      - Show recent logs")
        print("  reset     - Reset environment (nuclear option)")
        print("  test      - Run health checks")
        print("  monitor   - Continuous service monitoring")
        print()
        print("Examples:")
        print("  python3 dev_helper.py start")
        print("  python3 dev_helper.py monitor")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        dev_start()
    elif command == "stop":
        dev_stop()
    elif command == "restart":
        dev_restart()
    elif command == "logs":
        dev_logs()
    elif command == "reset":
        dev_reset()
    elif command == "test":
        dev_test()
    elif command == "monitor":
        os.system("python3 /workspaces/The-frappe-LMS-/service_monitor.py monitor")
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
