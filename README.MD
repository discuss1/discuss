# Django Reddit Clone

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.1.14-brightgreen?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/Django_Rest_Framework-3.11.2-red?style=flat&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Angular](https://img.shields.io/badge/Angular-10-blueviolet?style=flat&logo=angular&logoColor=white)](https://angular.io/)

A **full-stack Reddit clone** built with **Django REST Framework** backend and **Angular** frontend. This application provides a complete social media platform with user authentication, community features, and real-time interactions.

## 🚀 Features

- **User Authentication**: Sign up, log in, and manage accounts securely.
- **Create & Interact with Posts**: Standalone and group-based posts with threaded discussions.
- **Community Features**: Users can create and join groups (public, private, or restricted).
- **Engagement Mechanisms**: Upvote/downvote system for posts and comments.
- **Social Interaction**: Follow users and posts.
- **Content Moderation**: Report inappropriate content.
- **Bookmarks & Saves**: Users can save their favorite posts.
- **Invites & Membership Requests**: Manage group access through invites and requests.


## 📸 Screenshots

![Django Reddit Sign In Page](screenshots/image01.png?raw=true "Django Reddit Sign In")

![Django Reddit Feed](screenshots/image02.png?raw=true "Django Reddit Feed")

![Django Reddit Group](screenshots/image03.png?raw=true "Django Reddit Group")

![Django Reddit User Feed](screenshots/image04.png?raw=true "Django Reddit User Feed")

<br>

## 🔧 Requirements

### Backend
- Python 3.8+
- Django 3.1.14
- Django REST Framework 3.11.2
- SQLite (default) or PostgreSQL

### Frontend
- Node.js 14+ (with legacy OpenSSL provider support)
- Angular 10
- Angular CLI

## ⚙️ Quick Start

### 1. Clone and Setup Backend
```bash
git clone https://github.com/sherrlock1/discuss.git
cd discuss

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate sample data (optional)
python manage.py shell
# Run the sample data creation commands (see Management Commands section)

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

### 2. Setup Frontend
```bash
# Navigate to frontend directory
cd static/frontend/reddit-app

# Install Angular dependencies
npm install

# Start Angular development server
NODE_OPTIONS="--openssl-legacy-provider" ng serve --host 0.0.0.0 --port 4200
```

### 3. Access the Application
- **Frontend**: http://localhost:4200/django_reddit
- **Backend API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/

## 🚀 Deployment Configuration

The application is configured for deployment with the following features:

### Backend (Django)
- **CORS Headers**: Configured for cross-origin requests
- **Static Files**: Whitenoise middleware for serving static files
- **Database**: SQLite with sample data populated
- **API Documentation**: Available at `/api/swagger/` and `/api/redoc/`

### Frontend (Angular)
- **Environment Configuration**: Separate development and production environments
- **TypeScript**: Configured with compatibility flags for legacy dependencies
- **Build Optimization**: Production-ready build configuration

### Sample Data Included
- **Users**: admin/admin123, user1-3/password123
- **Posts**: Sample posts with comments and votes
- **Groups**: Various public and private communities
- **Tags**: Categorized content tags

## 📝 API Documentation

The API documentation is available via **Swagger**:

- **Swagger UI:** `http://localhost:8000/api/swagger/`
- **Redoc:** `http://localhost:8000/api/redoc/`

## 📈 Management Commands

### Populate Sample Data
```python
# Run in Django shell: python manage.py shell
from django.contrib.auth.models import User
from apps.posts.models import Post
from apps.groups.models import Group
from apps.tags.models import Tag
from apps.reports.models import ReportType

# Create sample users
for i in range(1, 4):
    User.objects.get_or_create(
        username=f'user{i}',
        defaults={'email': f'user{i}@example.com', 'first_name': f'User{i}', 'last_name': 'Test'}
    )

# Create sample tags
tags = ['Technology', 'Science', 'Programming', 'News', 'Discussion']
for tag_name in tags:
    Tag.objects.get_or_create(name=tag_name)

# Create sample groups
Group.objects.get_or_create(
    name='Django Developers',
    defaults={'description': 'Community for Django developers', 'group_type': 'public'}
)

# Create report types
report_types = ['Spam', 'Harassment', 'Inappropriate Content', 'Copyright Violation']
for report_type in report_types:
    ReportType.objects.get_or_create(name=report_type)
```

## ⚙️ Environment Configuration

### Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:4200`

### Production
- Configure `ALLOWED_HOSTS` in `settings.py`
- Update `environment.ts` with production URLs
- Set `DEBUG=False` for production

## 🔧 Troubleshooting

### Common Issues

1. **Angular Compilation Errors**
   ```bash
   # Use legacy OpenSSL provider for Node.js compatibility
   NODE_OPTIONS="--openssl-legacy-provider" ng serve
   ```

2. **TypeScript Errors**
   - The project includes `skipLibCheck: true` in `tsconfig.json` for compatibility
   - Froala editor is temporarily disabled due to type conflicts

3. **CORS Issues**
   - Backend is configured with `django-cors-headers`
   - Frontend URLs are whitelisted in Django settings

4. **Database Issues**
   ```bash
   # Reset database if needed
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```


## 🏗️ Project Structure

```
discuss/
├── apps/                          # Django apps
│   ├── bookmarks/                # Bookmark functionality
│   ├── comments/                 # Comment system
│   ├── core/                     # Core utilities
│   ├── followers/                # User following system
│   ├── groups/                   # Community groups
│   ├── posts/                    # Post management
│   ├── profiles/                 # User profiles
│   ├── reports/                  # Content reporting
│   └── tags/                     # Content tagging
├── reddit_clone/                 # Django project settings
├── static/frontend/reddit-app/   # Angular frontend
│   ├── src/app/                  # Angular components
│   ├── src/environments/         # Environment configs
│   └── package.json              # Node.js dependencies
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management script
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [API Documentation](#-api-documentation)
3. Open an issue on GitHub

---

### 🎉 **Happy Coding!** 🚀

