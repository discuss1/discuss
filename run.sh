#!/bin/bash

# Kill any existing Python servers
pkill -f "python serve_frontend.py" || true
pkill -f "python serve_backend.py" || true
pkill -f "python manage.py runserver" || true

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install psycopg2-binary==2.9.9
else
    source venv/bin/activate
fi

# Apply migrations
python manage.py migrate

# Create a superuser if it doesn't exist
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Start the backend server
python serve_backend.py &
BACKEND_PID=$!

# Start the frontend server
python serve_frontend.py &
FRONTEND_PID=$!

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID; echo 'Servers stopped.'" EXIT

# Print URLs
echo "Backend running at: https://work-1-nzwyroghofseggzd.prod-runtime.all-hands.dev"
echo "Frontend running at: https://work-2-nzwyroghofseggzd.prod-runtime.all-hands.dev/django_reddit/"

# Keep the script running
wait $BACKEND_PID $FRONTEND_PID