#!/usr/bin/env python3
"""
Django Reddit - Dependency Checker
Verifies all required packages are installed correctly
"""

import sys
import importlib
import subprocess

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name.replace('-', '_')
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - MISSING ({e})")
        return False

def check_django_apps():
    """Check Django-specific apps"""
    django_apps = [
        ('django', 'django'),
        ('djangorestframework', 'rest_framework'),
        ('dj-rest-auth', 'dj_rest_auth'),
        ('django-allauth', 'allauth'),
        ('django-cors-headers', 'corsheaders'),
        ('django-filter', 'django_filters'),
        ('django-guardian', 'guardian'),
        ('drf-yasg', 'drf_yasg'),
        ('Pillow', 'PIL'),
        ('psycopg2-binary', 'psycopg2'),
    ]
    
    print("🔍 Checking Django Dependencies...")
    print("-" * 40)
    
    all_good = True
    for package, import_name in django_apps:
        if not check_package(package, import_name):
            all_good = False
    
    return all_good

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def check_django_settings():
    """Check if Django settings can be loaded"""
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reddit_clone.settings')
        import django
        django.setup()
        print("✅ Django settings loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False

def main():
    """Main dependency check"""
    print("🚀 Django Reddit - Dependency Checker")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Django Dependencies", check_django_apps),
        ("Django Settings", check_django_settings),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}")
        print("-" * 30)
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Your environment is ready.")
        print("\nNext steps:")
        print("1. python manage.py migrate")
        print("2. python manage.py runserver")
    else:
        print("⚠️  SOME CHECKS FAILED!")
        print("\nTo fix missing dependencies:")
        print("pip install -r requirements.txt")
        print("\nFor dj_rest_auth specifically:")
        print("pip install dj-rest-auth==6.0.0")
        print("pip install django-rest-auth==0.9.5")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())