# 🚀 Django Reddit - Quick Deployment

A Reddit-like social platform built with Django (backend) and Angular 11 (frontend).

## ⚡ Quick Start for Linux Mint 22.1

### Option 1: Automated Deployment
```bash
git clone https://github.com/discuss1/discuss.git
cd discuss
./deploy.sh
python manage.py runserver
```

### Option 2: Manual Setup
See the complete guide: **[DEPLOYMENT_GUIDE_LINUX_MINT.md](./DEPLOYMENT_GUIDE_LINUX_MINT.md)**

## 🌐 Access the Application

After deployment, open your browser to:
- **Main App**: http://localhost:8000/django_reddit/
- **Admin Panel**: http://localhost:8000/admin/

## 📋 Requirements

- **Node.js 18.x** (for Angular 11)
- **Python 3.12+** (for Django)
- **Git** (for cloning)
- **Linux Mint 22.1** (Ubuntu 24.04 base)

## 🔧 Current Versions

- **Angular**: 11.2.14 (upgraded from 10.2.5)
- **Django**: 3.2.25 LTS (stable and compatible)
- **Node.js**: 18.x (required for Angular 11)
- **dj-rest-auth**: 4.0.1 (compatible with Django 3.2)

## 📚 Documentation

- **[Complete Deployment Guide](./DEPLOYMENT_GUIDE_LINUX_MINT.md)** - Detailed step-by-step instructions
- **[Troubleshooting](./DEPLOYMENT_GUIDE_LINUX_MINT.md#-troubleshooting)** - Common issues and solutions

## 🎯 Features

- ✅ User authentication and registration
- ✅ Create and manage communities
- ✅ Post creation and voting system
- ✅ Real-time updates
- ✅ Search functionality
- ✅ Responsive design with Angular Material

---

**Need help?** Check the [deployment guide](./DEPLOYMENT_GUIDE_LINUX_MINT.md) for detailed instructions and troubleshooting.