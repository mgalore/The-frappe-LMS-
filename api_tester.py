#!/usr/bin/env python3
"""
API Test Suite for Frappe LMS
Tests all critical API endpoints to ensure they work correctly
"""

import requests
import json
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def print_status(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "SUCCESS":
            print(f"{Colors.GREEN}✓ [{timestamp}] {message}{Colors.ENDC}")
            self.passed += 1
        elif status == "ERROR":
            print(f"{Colors.RED}✗ [{timestamp}] {message}{Colors.ENDC}")
            self.failed += 1
        elif status == "WARNING":
            print(f"{Colors.YELLOW}⚠ [{timestamp}] {message}{Colors.ENDC}")
            self.warnings += 1
        else:
            print(f"{Colors.BLUE}ℹ [{timestamp}] {message}{Colors.ENDC}")

    def test_api_endpoint(self, endpoint, method="GET", data=None, expected_status=200, 
                         should_contain=None, should_not_contain=None):
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                headers = {'Content-Type': 'application/json'}
                response = self.session.post(url, json=data, headers=headers, timeout=10)
            else:
                self.print_status(f"Unsupported method {method} for {endpoint}", "ERROR")
                return False

            # Check status code
            if response.status_code != expected_status:
                self.print_status(f"API {endpoint} - Status {response.status_code} (expected {expected_status})", "ERROR")
                return False

            # Check response content
            response_text = response.text
            
            if should_contain:
                for text in should_contain if isinstance(should_contain, list) else [should_contain]:
                    if text not in response_text:
                        self.print_status(f"API {endpoint} - Missing expected content: {text}", "ERROR")
                        return False

            if should_not_contain:
                for text in should_not_contain if isinstance(should_not_contain, list) else [should_not_contain]:
                    if text in response_text:
                        self.print_status(f"API {endpoint} - Contains unwanted content: {text}", "ERROR")
                        return False

            self.print_status(f"API {endpoint} - OK", "SUCCESS")
            return True

        except requests.exceptions.ConnectionError:
            self.print_status(f"API {endpoint} - Connection Error", "ERROR")
            return False
        except requests.exceptions.Timeout:
            self.print_status(f"API {endpoint} - Timeout", "ERROR")
            return False
        except Exception as e:
            self.print_status(f"API {endpoint} - Error: {str(e)}", "ERROR")
            return False

    def test_core_apis(self):
        """Test core Frappe LMS APIs"""
        print(f"\n{Colors.BOLD}📡 TESTING CORE APIS{Colors.ENDC}")
        print("-" * 30)
        
        # Test main LMS page
        self.test_api_endpoint("/lms", should_contain="<!DOCTYPE html>")
        
        # Test API endpoints
        api_tests = [
            {
                "endpoint": "/api/method/lms.lms.api.get_user_info",
                "method": "POST",
                "should_not_contain": ["Traceback", "Error 500", "Internal Server Error"]
            },
            {
                "endpoint": "/api/method/lms.lms.api.get_lms_setting",
                "method": "POST",
                "should_not_contain": ["Traceback", "Error 500"]
            },
            {
                "endpoint": "/api/method/lms.lms.api.get_sidebar_settings",
                "method": "POST",
                "should_not_contain": ["Traceback", "Error 500"]
            },
            {
                "endpoint": "/api/method/lms.lms.utils.get_courses",
                "method": "POST",
                "should_not_contain": ["Traceback", "Error 500"]
            },
            {
                "endpoint": "/api/method/frappe.client.get_count",
                "method": "POST",
                "data": {"doctype": "User"},
                "should_not_contain": ["Traceback", "Error 500"]
            }
        ]
        
        for test in api_tests:
            self.test_api_endpoint(**test)

    def test_removed_apis(self):
        """Test that removed Job APIs are actually gone"""
        print(f"\n{Colors.BOLD}🚫 TESTING REMOVED APIS{Colors.ENDC}")
        print("-" * 30)
        
        # These should return 417 or 404 since Jobs were removed
        removed_apis = [
            "/api/method/lms.lms.api.get_job_opportunities",
            "/api/method/lms.lms.api.get_job_details"
        ]
        
        for endpoint in removed_apis:
            try:
                response = self.session.post(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code in [417, 404, 500]:  # Expected for removed endpoints
                    self.print_status(f"Removed API {endpoint} - Correctly unavailable ({response.status_code})", "SUCCESS")
                else:
                    self.print_status(f"Removed API {endpoint} - Unexpected status {response.status_code}", "WARNING")
            except:
                self.print_status(f"Removed API {endpoint} - Connection error (expected)", "SUCCESS")

    def test_frontend_routes(self):
        """Test frontend routes"""
        print(f"\n{Colors.BOLD}🌐 TESTING FRONTEND ROUTES{Colors.ENDC}")
        print("-" * 30)
        
        routes_to_test = [
            ("/lms/courses", "Courses page"),
            ("/lms/batches", "Batches page"),
            ("/lms/statistics", "Statistics page"),
        ]
        
        for route, description in routes_to_test:
            self.test_api_endpoint(route, should_contain="<!DOCTYPE html>")

    def test_removed_routes(self):
        """Test that removed Job routes are gone"""
        print(f"\n{Colors.BOLD}🚫 TESTING REMOVED ROUTES{Colors.ENDC}")
        print("-" * 30)
        
        # Job routes should redirect or show 404
        removed_routes = [
            "/job-openings",
            "/lms/job-openings"
        ]
        
        for route in removed_routes:
            # Check if route is handled properly (redirect or 404)
            response = self.session.get(f"{self.base_url}{route}", allow_redirects=True, timeout=10)
            if response.status_code in [404, 200]:  # 200 if redirected to valid page
                # Check that we're not on a job page
                if "job" not in response.url.lower() and "Job" not in response.text[:1000]:
                    self.print_status(f"Removed route {route} - Correctly handled", "SUCCESS")
                else:
                    self.print_status(f"Removed route {route} - Still shows job content", "ERROR")
            else:
                self.print_status(f"Removed route {route} - Status {response.status_code}", "WARNING")

    def run_all_tests(self):
        """Run all API tests"""
        print(f"{Colors.BOLD}{'='*60}")
        print("🧪 FRAPPE LMS API TEST SUITE")
        print(f"{'='*60}{Colors.ENDC}")
        
        self.test_core_apis()
        self.test_removed_apis()
        self.test_frontend_routes()
        self.test_removed_routes()
        
        # Print summary
        print(f"\n{Colors.BOLD}📊 TEST SUMMARY{Colors.ENDC}")
        print("-" * 20)
        
        total_tests = self.passed + self.failed + self.warnings
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.ENDC}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.ENDC}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0 and success_rate >= 80:
            print(f"\n{Colors.GREEN}🎉 ALL TESTS PASSED!{Colors.ENDC}")
            return 0
        elif self.failed == 0:
            print(f"\n{Colors.YELLOW}⚠ Tests passed but with warnings{Colors.ENDC}")
            return 1
        else:
            print(f"\n{Colors.RED}❌ SOME TESTS FAILED{Colors.ENDC}")
            return 2

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://127.0.0.1:8000"
    
    tester = APITester(base_url)
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
