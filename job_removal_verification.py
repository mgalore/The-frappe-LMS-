#!/usr/bin/env python3
"""
Script to verify that Jobs functionality has been completely removed from Frappe LMS.
"""

import os
import sys
import subprocess

def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def search_in_files(directory, pattern):
    """Search for a pattern in files within a directory."""
    try:
        result = subprocess.run(
            ["grep", "-r", "-i", pattern, directory],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except:
        return ""

def main():
    print("🔍 Verifying Jobs functionality removal from Frappe LMS...")
    print("=" * 60)
    
    base_path = "/workspaces/The-frappe-LMS-/lms-bench/apps/lms"
    issues_found = 0
    
    # 1. Check if job directory was removed
    job_dir = f"{base_path}/lms/job"
    if check_file_exists(job_dir):
        print("❌ ISSUE: Job directory still exists at lms/job")
        issues_found += 1
    else:
        print("✅ Job directory successfully removed")
    
    # 2. Check if Job module is in modules.txt
    modules_file = f"{base_path}/lms/modules.txt"
    if check_file_exists(modules_file):
        with open(modules_file, 'r') as f:
            content = f.read()
            if "Job" in content:
                print("❌ ISSUE: 'Job' still found in modules.txt")
                issues_found += 1
            else:
                print("✅ Job module removed from modules.txt")
    
    # 3. Check for job-related Vue components
    frontend_path = f"{base_path}/frontend/src"
    job_files = [
        "pages/Jobs.vue",
        "pages/JobDetail.vue", 
        "pages/JobForm.vue",
        "components/JobCard.vue",
        "components/Modals/JobApplicationModal.vue"
    ]
    
    for file_path in job_files:
        full_path = f"{frontend_path}/{file_path}"
        if check_file_exists(full_path):
            print(f"❌ ISSUE: Job component still exists: {file_path}")
            issues_found += 1
        else:
            print(f"✅ Job component removed: {file_path}")
    
    # 4. Check router.js for job routes
    router_file = f"{frontend_path}/router.js"
    if check_file_exists(router_file):
        with open(router_file, 'r') as f:
            content = f.read()
            if "job-opening" in content.lower() or "jobdetail" in content or "jobform" in content:
                print("❌ ISSUE: Job routes still found in router.js")
                issues_found += 1
            else:
                print("✅ Job routes removed from router.js")
    
    # 5. Check API file for job methods
    api_file = f"{base_path}/lms/lms/api.py"
    if check_file_exists(api_file):
        with open(api_file, 'r') as f:
            content = f.read()
            if "get_job_details" in content or "get_job_opportunities" in content:
                print("❌ ISSUE: Job API methods still found in api.py")
                issues_found += 1
            else:
                print("✅ Job API methods removed from api.py")
    
    # 6. Check for job references in CSS
    css_file = f"{base_path}/lms/public/css/style.css"
    if check_file_exists(css_file):
        with open(css_file, 'r') as f:
            content = f.read()
            if ".job-" in content:
                print("❌ ISSUE: Job CSS classes still found in style.css")
                issues_found += 1
            else:
                print("✅ Job CSS classes removed from style.css")
    
    # 7. Check components.d.ts
    components_file = f"{frontend_path}/../components.d.ts"
    if check_file_exists(components_file):
        with open(components_file, 'r') as f:
            content = f.read()
            if "JobCard" in content or "JobApplication" in content:
                print("❌ ISSUE: Job component references still found in components.d.ts")
                issues_found += 1
            else:
                print("✅ Job component references removed from components.d.ts")
    
    print("=" * 60)
    
    if issues_found == 0:
        print("🎉 SUCCESS: Jobs functionality has been completely removed!")
        print("✨ The LMS should now work without any job-related features.")
    else:
        print(f"⚠️  FOUND {issues_found} ISSUES that need to be addressed.")
        
    return issues_found

if __name__ == "__main__":
    sys.exit(main())
