# Database Migration Guide: SQLite to PostgreSQL

## Current Status

✅ **PostgreSQL Support**: Already configured in `reddit_clone/settings.py`
✅ **Dependencies**: `psycopg2-binary` and `dj-database-url` installed
✅ **Environment Variables**: Database configuration supports environment-based setup

## Migration Strategy

### 1. Pre-Migration Preparation

#### A. Backup Current Database
```bash
# Create backup of current SQLite database
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# Export data using Django's dumpdata
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude=contenttypes --exclude=auth.Permission \
  --exclude=sessions.session --exclude=admin.logentry \
  > data_backup.json
```

#### B. Environment Configuration
Update `.env` file with PostgreSQL settings:
```env
# Database Configuration
ENVIRONMENT=production
DATABASE_URL=postgresql://username:password@localhost:5432/reddit_clone

# Alternative individual settings
DB_NAME=reddit_clone
DB_USER=reddit_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. PostgreSQL Setup

#### A. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Docker (recommended for development)
docker run --name reddit-postgres \
  -e POSTGRES_DB=reddit_clone \
  -e POSTGRES_USER=reddit_user \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  -d postgres:13
```

#### B. Create Database and User
```sql
-- Connect to PostgreSQL as superuser
sudo -u postgres psql

-- Create database and user
CREATE DATABASE reddit_clone;
CREATE USER reddit_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE reddit_clone TO reddit_user;
ALTER USER reddit_user CREATEDB;

-- Exit PostgreSQL
\q
```

### 3. Migration Process

#### A. Test Connection
```bash
# Test PostgreSQL connection
python manage.py dbshell
```

#### B. Run Migrations
```bash
# Create fresh migrations (if needed)
python manage.py makemigrations

# Apply migrations to PostgreSQL
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### C. Data Migration
```bash
# Load data from backup
python manage.py loaddata data_backup.json

# Alternative: Use Django's database routing for gradual migration
# (Advanced option for large datasets)
```

### 4. Verification Steps

#### A. Data Integrity Checks
```bash
# Check record counts
python manage.py shell -c "
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import PostComment

print(f'Users: {User.objects.count()}')
print(f'Posts: {Post.objects.count()}')
print(f'Comments: {PostComment.objects.count()}')
"

# Run tests to verify functionality
python manage.py test
```

#### B. Application Testing
```bash
# Start development server
python manage.py runserver

# Test key functionality:
# - User registration/login
# - Post creation/viewing
# - Comment functionality
# - Voting system
```

### 5. Performance Optimization

#### A. Database Indexes
```sql
-- Add indexes for frequently queried fields
CREATE INDEX CONCURRENTLY idx_posts_created_at ON posts_post(created_at);
CREATE INDEX CONCURRENTLY idx_posts_author ON posts_post(author_id);
CREATE INDEX CONCURRENTLY idx_comments_post ON comments_postcomment(post_id);
CREATE INDEX CONCURRENTLY idx_votes_post ON posts_postvote(post_id);
```

#### B. Connection Pooling
Add to `settings.py`:
```python
# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 60
DATABASES['default']['OPTIONS'] = {
    'MAX_CONNS': 20,
    'MIN_CONNS': 5,
}
```

### 6. Production Deployment

#### A. Environment Variables
```env
# Production settings
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@db-host:5432/reddit_clone

# Security settings
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CORS settings
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### B. Database Security
```sql
-- Revoke unnecessary privileges
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO reddit_user;
GRANT CREATE ON SCHEMA public TO reddit_user;

-- Enable SSL (recommended for production)
ALTER SYSTEM SET ssl = on;
SELECT pg_reload_conf();
```

### 7. Monitoring and Maintenance

#### A. Database Monitoring
```bash
# Monitor database size
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT pg_size_pretty(pg_database_size('reddit_clone'))\")
print(f'Database size: {cursor.fetchone()[0]}')
"

# Monitor active connections
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT count(*) FROM pg_stat_activity')
print(f'Active connections: {cursor.fetchone()[0]}')
"
```

#### B. Regular Maintenance
```bash
# Database vacuum and analyze (weekly)
python manage.py dbshell -c "VACUUM ANALYZE;"

# Update statistics (daily)
python manage.py dbshell -c "ANALYZE;"
```

### 8. Rollback Plan

#### A. Emergency Rollback
```bash
# Switch back to SQLite
export DATABASE_URL=""
export ENVIRONMENT="development"

# Restore from backup
cp db.sqlite3.backup.YYYYMMDD_HHMMSS db.sqlite3

# Restart application
python manage.py runserver
```

#### B. Data Sync Back to SQLite
```bash
# Export from PostgreSQL
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude=contenttypes --exclude=auth.Permission \
  > postgres_backup.json

# Switch to SQLite and load data
export DATABASE_URL=""
python manage.py migrate
python manage.py loaddata postgres_backup.json
```

## Migration Checklist

### Pre-Migration
- [ ] Create SQLite backup
- [ ] Export data using dumpdata
- [ ] Set up PostgreSQL server
- [ ] Create database and user
- [ ] Update environment variables
- [ ] Test PostgreSQL connection

### Migration
- [ ] Run Django migrations
- [ ] Load data from backup
- [ ] Create superuser account
- [ ] Verify data integrity
- [ ] Run test suite

### Post-Migration
- [ ] Performance testing
- [ ] Add database indexes
- [ ] Configure connection pooling
- [ ] Set up monitoring
- [ ] Document rollback procedure
- [ ] Update deployment scripts

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check PostgreSQL service status
   - Verify host/port configuration
   - Check firewall settings

2. **Authentication Failed**
   - Verify username/password
   - Check pg_hba.conf configuration
   - Ensure user has proper privileges

3. **Migration Errors**
   - Check for custom SQL in migrations
   - Verify foreign key constraints
   - Review data type compatibility

4. **Performance Issues**
   - Add missing indexes
   - Optimize query patterns
   - Configure connection pooling
   - Monitor slow queries

### Support Resources
- Django Database Documentation
- PostgreSQL Official Documentation
- Django Migration Best Practices
- Database Performance Tuning Guides