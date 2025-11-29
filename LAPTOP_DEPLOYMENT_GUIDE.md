# 🚀 Django Reddit - Laptop Deployment Guide

## 📋 Prerequisites

- Python 3.8+ (recommended: Python 3.10+)
- Node.js 18+ (for Angular frontend)
- Git

## 🔧 Step-by-Step Deployment

### 1. Clone Repository
```bash
git clone https://github.com/discuss1/discuss.git
cd discuss
```

### 2. Create Virtual Environment (RECOMMENDED)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# If you get ModuleNotFoundError for dj_rest_auth, install manually:
pip install dj-rest-auth==6.0.0
pip install django-rest-auth==0.9.5
```

### 4. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Install Node.js Dependencies (for Angular frontend)
```bash
# Install Angular CLI globally
npm install -g @angular/cli@11

# Install project dependencies
npm install
```

### 6. Start Development Servers

#### Backend (Django)
```bash
# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

#### Frontend (Angular) - In a new terminal
```bash
# Start Angular development server
ng serve --host 0.0.0.0 --port 4200
```

## 🌐 Access URLs

- **Frontend**: http://localhost:4200/
- **Backend API**: http://localhost:8000/api/
- **API Documentation**: http://localhost:8000/api/swagger/
- **Django Admin**: http://localhost:8000/admin/

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'dj_rest_auth'

**Solution 1**: Install both packages
```bash
pip install dj-rest-auth==6.0.0
pip install django-rest-auth==0.9.5
```

**Solution 2**: Reinstall all requirements
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

**Solution 3**: Use virtual environment
```bash
# Deactivate current environment
deactivate

# Create fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # Linux/Mac
# OR
fresh_venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Angular Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Use legacy OpenSSL provider if needed (Node.js 18+)
export NODE_OPTIONS="--openssl-legacy-provider"
ng serve
```

## 📦 Technology Stack

- **Backend**: Django 5.1.3
- **Frontend**: Angular 11.2.14
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: Django REST Framework 3.15.2
- **Authentication**: django-allauth + dj-rest-auth

## 🔑 Key Dependencies

### Authentication
- `dj-rest-auth==6.0.0` (new package)
- `django-rest-auth==0.9.5` (legacy compatibility)
- `django-allauth==65.13.1`

### API & Documentation
- `djangorestframework==3.15.2`
- `drf-yasg==1.21.7` (Swagger/OpenAPI)

### Security & CORS
- `django-cors-headers==4.3.1`
- `whitenoise==6.6.0`

## 🎯 Success Indicators

✅ Django server starts without errors
✅ Angular app compiles and serves
✅ API endpoints return HTTP 200
✅ Swagger documentation accessible
✅ Frontend can authenticate users

## 📞 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Ensure virtual environment is activated
3. Verify all dependencies are installed
4. Check Python and Node.js versions
5. Review error logs for specific issues

---
**Last Updated**: November 29, 2025
**Django Version**: 5.1.3 Latest Stable
**Angular Version**: 11.2.14