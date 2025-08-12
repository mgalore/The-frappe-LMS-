#!/usr/bin/env python3

import frappe
from frappe.utils import getdate

def create_users():
    # Connect to the site
    frappe.connect()
    
    # Create Admin User
    try:
        admin_user = frappe.new_doc("User")
        admin_user.email = "admin@lms.local"
        admin_user.first_name = "Admin"
        admin_user.last_name = "User"
        admin_user.new_password = "admin123"
        admin_user.user_type = "System User"
        admin_user.birth_date = getdate("1990-01-01")
        admin_user.insert(ignore_permissions=True)
        
        # Add admin roles
        admin_user.add_roles("System Manager", "LMS Admin")
        print(f"✅ Created admin user: {admin_user.email}")
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
    
    # Create Student User  
    try:
        student_user = frappe.new_doc("User")
        student_user.email = "student@lms.local"
        student_user.first_name = "John"
        student_user.last_name = "Student"
        student_user.new_password = "student123"
        student_user.user_type = "Website User"
        student_user.birth_date = getdate("1995-05-15")
        student_user.insert(ignore_permissions=True)
        
        # Add student role
        student_user.add_roles("LMS Student")
        print(f"✅ Created student user: {student_user.email}")
    except Exception as e:
        print(f"❌ Error creating student user: {str(e)}")
        
    # Create Evaluator User
    try:
        evaluator_user = frappe.new_doc("User")
        evaluator_user.email = "evaluator@lms.local"  
        evaluator_user.first_name = "Jane"
        evaluator_user.last_name = "Evaluator"
        evaluator_user.new_password = "evaluator123"
        evaluator_user.user_type = "System User"
        evaluator_user.birth_date = getdate("1988-03-20")
        evaluator_user.insert(ignore_permissions=True)
        
        # Add evaluator roles
        evaluator_user.add_roles("LMS Student", "Batch Evaluator")
        print(f"✅ Created evaluator user: {evaluator_user.email}")
    except Exception as e:
        print(f"❌ Error creating evaluator user: {str(e)}")
    
    frappe.db.commit()
    print("\n🎉 All users created successfully!")
    print("\n📋 Login Credentials:")
    print("=" * 50)
    print("ADMIN USER:")
    print("Email: admin@lms.local")
    print("Password: admin123")
    print("Roles: System Manager, LMS Admin")
    print("\nSTUDENT USER:")
    print("Email: student@lms.local")
    print("Password: student123") 
    print("Roles: LMS Student")
    print("\nEVALUATOR USER:")
    print("Email: evaluator@lms.local")
    print("Password: evaluator123")
    print("Roles: LMS Student, Batch Evaluator")
    print("=" * 50)

if __name__ == "__main__":
    create_users()
