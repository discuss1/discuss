#!/bin/bash
# Quick fix for ModuleNotFoundError: No module named 'dj_rest_auth'

echo "🔧 Fixing dj_rest_auth installation issue..."

# Check if we're in the project directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run ./deploy.sh first"
    exit 1
fi

source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dj-rest-auth specifically
echo "📦 Installing dj-rest-auth..."
pip install dj-rest-auth==4.0.1

# Verify installation
echo "🔍 Verifying installation..."
if python -c "import dj_rest_auth; print('✅ SUCCESS: dj-rest-auth is now installed')"; then
    echo "🎉 Problem fixed! You can now run: python manage.py runserver"
else
    echo "❌ Still having issues. Trying alternative approach..."
    
    # Try installing all auth-related packages
    pip install django-allauth==0.57.2
    pip install djangorestframework==3.15.2
    pip install dj-rest-auth==4.0.1
    
    # Final verification
    if python -c "import dj_rest_auth; print('✅ SUCCESS: dj-rest-auth is now installed')"; then
        echo "🎉 Problem fixed with alternative approach!"
    else
        echo "❌ Unable to fix automatically. Please check the troubleshooting guide."
        echo "📚 See DEPLOYMENT_GUIDE_LINUX_MINT.md section on dj_rest_auth errors"
    fi
fi