#!/usr/bin/env python3
"""
MySQL Setup Script for Django Blog Application
This script helps you set up MySQL database for the Django blog application.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            return result.stdout
        else:
            print(f"❌ Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def check_mysql_installation():
    """Check if MySQL is installed and accessible"""
    print("🔍 Checking MySQL installation...")
    
    # Check if mysql command is available
    result = run_command("mysql --version", "Checking MySQL version")
    if result:
        print(f"MySQL version: {result.strip()}")
        return True
    
    print("❌ MySQL not found. Please install MySQL first.")
    print("\n📋 MySQL Installation Options:")
    print("1. Download from: https://dev.mysql.com/downloads/mysql/")
    print("2. Or use Chocolatey: choco install mysql")
    print("3. Or use XAMPP: https://www.apachefriends.org/")
    return False

def create_database():
    """Create the MySQL database"""
    print("\n🗄️  Creating MySQL database...")
    
    # Get database credentials from user
    print("Please enter your MySQL credentials:")
    username = input("MySQL Username (default: root): ").strip() or "root"
    password = input("MySQL Password (leave empty if none): ").strip()
    
    # Create database SQL
    create_db_sql = """
    CREATE DATABASE IF NOT EXISTS django_blog_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
    """
    
    # Run the SQL command
    if password:
        command = f'mysql -u {username} -p{password} -e "{create_db_sql}"'
    else:
        command = f'mysql -u {username} -e "{create_db_sql}"'
    
    result = run_command(command, "Creating database 'django_blog_db'")
    if result:
        print("✅ Database created successfully!")
        return username, password
    else:
        print("❌ Failed to create database.")
        return None, None

def update_django_settings(username, password):
    """Update Django settings.py with MySQL credentials"""
    print("\n⚙️  Updating Django settings...")
    
    settings_file = "django_blog/settings.py"
    
    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Create MySQL configuration
    mysql_config = f'''# Option 1: MySQL Database (Recommended for production)
# Uncomment and configure the MySQL settings below if you have MySQL installed
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog_db',
        'USER': '{username}',
        'PASSWORD': '{password}',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {{
            'charset': 'utf8mb4',
        }},
    }}
}}

# Option 2: SQLite Database (Default for development)
# This will work immediately without additional setup
# DATABASES = {{
#     'default': {{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }}
# }}'''
    
    # Replace the database configuration
    import re
    pattern = r'# Option 1: MySQL Database.*?# Option 2: SQLite Database.*?DATABASES = \{.*?\}'
    replacement = mysql_config
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write updated settings
    with open(settings_file, 'w') as f:
        f.write(new_content)
    
    print("✅ Django settings updated with MySQL configuration!")

def run_migrations():
    """Run Django migrations"""
    print("\n🔄 Running Django migrations...")
    
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Applying migrations"),
    ]
    
    for command, description in commands:
        result = run_command(command, description)
        if not result:
            print(f"❌ Failed to {description.lower()}")
            return False
    
    print("✅ Migrations completed successfully!")
    return True

def main():
    """Main setup function"""
    print("🚀 MySQL Setup for Django Blog Application")
    print("=" * 50)
    
    # Check MySQL installation
    if not check_mysql_installation():
        print("\n💡 Alternative: You can continue with SQLite for development.")
        print("   The application is already configured to use SQLite by default.")
        return
    
    # Create database
    username, password = create_database()
    if not username:
        return
    
    # Update Django settings
    update_django_settings(username, password)
    
    # Run migrations
    if run_migrations():
        print("\n🎉 MySQL setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Admin: http://localhost:8000/admin/")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main() 