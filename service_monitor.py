#!/usr/bin/env python3
"""
Service Monitor for Frappe LMS
Real-time monitoring of all services with auto-restart capabilities
"""

import subprocess
import sys
import os
import time
import requests
import json
from datetime import datetime

def check_service_port(port, service_name):
    """Check if a service is running on a specific port"""
    try:
        response = requests.get(f"http://127.0.0.1:{port}", timeout=2)
        return True, f"✓ {service_name} (:{port}) - OK"
    except requests.exceptions.ConnectionError:
        return False, f"✗ {service_name} (:{port}) - DOWN"
    except requests.exceptions.Timeout:
        return False, f"⚠ {service_name} (:{port}) - TIMEOUT"
    except Exception as e:
        return False, f"✗ {service_name} (:{port}) - ERROR: {str(e)[:50]}"

def check_mariadb():
    """Check MariaDB service"""
    try:
        result = subprocess.run("sudo service mariadb status", shell=True, capture_output=True, text=True)
        if "active (running)" in result.stdout:
            return True, "✓ MariaDB - RUNNING"
        else:
            return False, "✗ MariaDB - STOPPED"
    except:
        return False, "✗ MariaDB - ERROR"

def check_bench_processes():
    """Check if bench processes are running"""
    try:
        result = subprocess.run("pgrep -f 'bench start'", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            count = len(result.stdout.strip().split('\n'))
            return True, f"✓ Bench Processes - {count} running"
        else:
            return False, "✗ Bench Processes - NONE"
    except:
        return False, "✗ Bench Processes - ERROR"

def check_api_endpoints():
    """Check critical API endpoints"""
    endpoints = {
        "Health": "http://127.0.0.1:8000",
        "LMS": "http://127.0.0.1:8000/lms",
        "API": "http://127.0.0.1:8000/api/method/lms.lms.api.get_user_info"
    }
    
    results = []
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                results.append((True, f"✓ {name} API - OK ({response.status_code})"))
            else:
                results.append((False, f"⚠ {name} API - {response.status_code}"))
        except Exception as e:
            results.append((False, f"✗ {name} API - ERROR"))
    
    return results

def monitor_mode():
    """Continuous monitoring mode"""
    print("🔍 CONTINUOUS MONITORING MODE")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    
    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"📊 FRAPPE LMS SERVICE MONITOR - {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 60)
            
            # Check services
            services = [
                (3306, "MariaDB"),
                (8000, "Web Server"),
                (9000, "Socket.IO"),
                (11000, "Redis Queue"),
                (13000, "Redis Cache")
            ]
            
            all_good = True
            for port, name in services:
                if name == "MariaDB":
                    status, msg = check_mariadb()
                else:
                    status, msg = check_service_port(port, name)
                print(msg)
                if not status:
                    all_good = False
            
            print()
            
            # Check bench processes
            status, msg = check_bench_processes()
            print(msg)
            if not status:
                all_good = False
            
            print()
            
            # Check APIs
            api_results = check_api_endpoints()
            for status, msg in api_results:
                print(msg)
                if not status:
                    all_good = False
            
            print()
            if all_good:
                print("🟢 ALL SYSTEMS OPERATIONAL")
            else:
                print("🔴 ISSUES DETECTED - Run quick_fix.py")
            
            print("\nNext check in 5 seconds... (Ctrl+C to exit)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped.")

def single_check():
    """Single comprehensive check"""
    print("📊 FRAPPE LMS SERVICE STATUS")
    print("=" * 50)
    
    issues = []
    
    # Database check
    status, msg = check_mariadb()
    print(msg)
    if not status:
        issues.append("MariaDB")
    
    # Service checks
    services = [(8000, "Web Server"), (9000, "Socket.IO"), (11000, "Redis Queue"), (13000, "Redis Cache")]
    for port, name in services:
        status, msg = check_service_port(port, name)
        print(msg)
        if not status:
            issues.append(name)
    
    # Process check
    status, msg = check_bench_processes()
    print(msg)
    if not status:
        issues.append("Bench Processes")
    
    print("\n🌐 API ENDPOINTS")
    print("-" * 25)
    api_results = check_api_endpoints()
    for status, msg in api_results:
        print(msg)
        if not status:
            issues.append("API")
    
    print(f"\n📋 SUMMARY")
    print("-" * 20)
    if not issues:
        print("🟢 All services are running properly!")
    else:
        print(f"🔴 Issues found with: {', '.join(set(issues))}")
        print("💡 Run 'python3 quick_fix.py all' to auto-fix common issues")
    
    return len(issues) == 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        monitor_mode()
    else:
        single_check()

if __name__ == "__main__":
    main()
