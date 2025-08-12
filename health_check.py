#!/usr/bin/env python3
"""
Frappe LMS Health Check Script
Run this script to quickly check if all services and APIs are working correctly
"""

import requests
import subprocess
import json
import time
import sys
import os
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "SUCCESS":
        print(f"{Colors.GREEN}✓ [{timestamp}] {message}{Colors.ENDC}")
    elif status == "ERROR":
        print(f"{Colors.RED}✗ [{timestamp}] {message}{Colors.ENDC}")
    elif status == "WARNING":
        print(f"{Colors.YELLOW}⚠ [{timestamp}] {message}{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}ℹ [{timestamp}] {message}{Colors.ENDC}")

def check_service_port(port, service_name):
    """Check if a service is running on the specified port"""
    try:
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        if f":{port} " in result.stdout:
            print_status(f"{service_name} is running on port {port}", "SUCCESS")
            return True
        else:
            print_status(f"{service_name} is NOT running on port {port}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error checking {service_name}: {str(e)}", "ERROR")
        return False

def check_mariadb():
    """Check if MariaDB is running"""
    try:
        # First check if MariaDB service is running
        result = subprocess.run("sudo service mariadb status", shell=True, capture_output=True, text=True)
        if "active (running)" not in result.stdout:
            return False, "MariaDB service is not running"
        
        # Then check if we can connect to the database
        os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
        result = subprocess.run('bench --site lms.local execute "frappe.db.sql(\'SELECT 1\')"', 
                              shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "MariaDB is running and accessible"
        else:
            return False, f"MariaDB running but database connection failed"
            
    except subprocess.TimeoutExpired:
        return False, "MariaDB connection timeout"
    except Exception as e:
        return False, f"MariaDB check failed: {str(e)[:50]}"

def check_api_endpoint(url, endpoint_name, expected_status=200):
    """Check if an API endpoint is accessible"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print_status(f"{endpoint_name} API is accessible", "SUCCESS")
            return True
        else:
            print_status(f"{endpoint_name} API returned status {response.status_code}", "WARNING")
            return False
    except requests.exceptions.ConnectionError:
        print_status(f"{endpoint_name} API is not accessible (Connection Error)", "ERROR")
        return False
    except requests.exceptions.Timeout:
        print_status(f"{endpoint_name} API timeout", "ERROR")
        return False
    except Exception as e:
        print_status(f"Error checking {endpoint_name} API: {str(e)}", "ERROR")
        return False

def check_lms_apis(base_url):
    """Check critical LMS API endpoints"""
    apis_to_check = [
        ("/api/method/lms.lms.api.get_user_info", "User Info"),
        ("/api/method/lms.lms.api.get_lms_setting", "LMS Settings"),
        ("/api/method/lms.lms.api.get_sidebar_settings", "Sidebar Settings"),
        ("/api/method/lms.lms.utils.get_courses", "Courses"),
        ("/api/method/frappe.client.get_count", "Database Count"),
    ]
    
    success_count = 0
    for endpoint, name in apis_to_check:
        if check_api_endpoint(f"{base_url}{endpoint}", name):
            success_count += 1
    
    return success_count, len(apis_to_check)

def check_frontend_build():
    """Check if frontend assets exist and are recent"""
    frontend_path = "/workspaces/The-frappe-LMS-/lms-bench/apps/lms/lms/public/frontend"
    
    if not os.path.exists(frontend_path):
        print_status("Frontend build directory not found", "ERROR")
        return False
    
    # Check for key files
    key_files = ["index.html", "sw.js"]
    missing_files = []
    
    for file in key_files:
        file_path = os.path.join(frontend_path, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print_status(f"Missing frontend files: {', '.join(missing_files)}", "ERROR")
        return False
    else:
        print_status("Frontend build files are present", "SUCCESS")
        return True

def run_bench_command(command, description):
    """Run a bench command and check if it succeeds"""
    try:
        os.chdir("/workspaces/The-frappe-LMS-/lms-bench")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print_status(f"{description} - Success", "SUCCESS")
            return True
        else:
            print_status(f"{description} - Failed: {result.stderr[:100]}...", "ERROR")
            return False
    except subprocess.TimeoutExpired:
        print_status(f"{description} - Timeout", "ERROR")
        return False
    except Exception as e:
        print_status(f"{description} - Error: {str(e)}", "ERROR")
        return False

def main():
    print(f"{Colors.BOLD}{'='*60}")
    print("🏥 FRAPPE LMS HEALTH CHECK")
    print(f"{'='*60}{Colors.ENDC}")
    print_status("Starting health check...")
    
    # Track overall health
    total_checks = 0
    passed_checks = 0
    
    print(f"\n{Colors.BOLD}1. SERVICE CHECKS{Colors.ENDC}")
    print("-" * 20)
    
    # Check database
    total_checks += 1
    db_status, db_msg = check_mariadb()
    if db_status:
        passed_checks += 1
    
    # Check services
    services = [
        (8000, "Web Server"),
        (9000, "Socket.IO"),
        (11000, "Redis Queue"),
        (13000, "Redis Cache")
    ]
    
    for port, service in services:
        total_checks += 1
        if check_service_port(port, service):
            passed_checks += 1
    
    print(f"\n{Colors.BOLD}2. API CHECKS{Colors.ENDC}")
    print("-" * 20)
    
    base_url = "http://127.0.0.1:8000"
    
    # Check main page
    total_checks += 1
    if check_api_endpoint(f"{base_url}/lms", "LMS Main Page"):
        passed_checks += 1
    
    # Check LMS APIs
    api_success, api_total = check_lms_apis(base_url)
    total_checks += api_total
    passed_checks += api_success
    
    print(f"\n{Colors.BOLD}3. BUILD CHECKS{Colors.ENDC}")
    print("-" * 20)
    
    # Check frontend build
    total_checks += 1
    if check_frontend_build():
        passed_checks += 1
    
    # Check for syntax errors in hooks
    total_checks += 1
    if run_bench_command("python -m py_compile apps/lms/lms/hooks.py", "Hooks syntax check"):
        passed_checks += 1
    
    print(f"\n{Colors.BOLD}4. OVERALL HEALTH{Colors.ENDC}")
    print("-" * 20)
    
    health_percentage = (passed_checks / total_checks) * 100
    
    if health_percentage >= 90:
        print_status(f"System Health: {health_percentage:.1f}% ({passed_checks}/{total_checks}) - EXCELLENT", "SUCCESS")
    elif health_percentage >= 70:
        print_status(f"System Health: {health_percentage:.1f}% ({passed_checks}/{total_checks}) - GOOD", "WARNING")
    else:
        print_status(f"System Health: {health_percentage:.1f}% ({passed_checks}/{total_checks}) - NEEDS ATTENTION", "ERROR")
    
    print(f"\n{Colors.BOLD}{'='*60}")
    print("🏁 HEALTH CHECK COMPLETE")
    print(f"{'='*60}{Colors.ENDC}")
    
    # Exit with appropriate code
    if health_percentage >= 70:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
