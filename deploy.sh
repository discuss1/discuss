#!/bin/bash
set -e

echo "🚀 Starting Django Reddit deployment..."

# Check if in correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "✅ Virtual environment activated"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd static/frontend/reddit-app
npm install --legacy-peer-deps

# Build Angular
echo "🔨 Building Angular application..."
NODE_OPTIONS="--openssl-legacy-provider" npx ng build --configuration production

# Go back to root
cd ../../../

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎉 Deployment complete!"
echo "🌐 Start the server with: python manage.py runserver"
echo "🔗 Access the app at: http://localhost:8000/django_reddit/"