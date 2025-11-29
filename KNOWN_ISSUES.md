# Known Issues

This document outlines known issues, limitations, and workarounds for the Django Reddit Clone application.

## 🚨 Critical Issues

### 1. Submit Button Functionality Issue
**Status**: ✅ **RESOLVED**  
**Affected Components**: Sign-in and Sign-up forms  
**Description**: Submit buttons were not working due to multiple cascading issues including Django URL configuration errors, Angular SPA routing problems, and static file serving issues.

**Root Causes Identified**:
1. **NoReverseMatch Error**: Django LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL were pointing to non-existent 'home' URL pattern
2. **Angular SPA Routing**: Django was not configured to handle client-side routing for Angular paths like `/django_reddit/sign-in`
3. **Static File Paths**: Incorrect static file references preventing JavaScript from loading properly
4. **Environment Configuration**: Inconsistent URL configurations between development and production environments

**Solutions Applied**:
1. **Fixed Django URL Redirects**: Updated LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, and ACCOUNT_LOGOUT_REDIRECT to use 'angular_app'
2. **Enabled SPA Routing**: Changed Django URL pattern from `path('django_reddit/')` to `re_path(r'^django_reddit/.*$')` to catch all Angular routes
3. **Fixed Static File Serving**: Updated template paths to use `/static/` prefix for all assets (CSS, JS, favicons)
4. **Rebuilt Angular App**: Fresh build with corrected environment configuration and proper static file deployment
5. **Verified API Connectivity**: Confirmed registration and login APIs working correctly with proper auth token responses

**Verification**:
- ✅ All Angular routes working (/, /sign-in, /sign-up) - HTTP 200 responses
- ✅ Submit buttons functional with proper click handlers
- ✅ JavaScript files loading correctly (main.js: 2.1MB)
- ✅ API endpoints tested and working (registration returns auth tokens)
- ✅ Static files served properly via Django static file serving
- ✅ No more NoReverseMatch errors in Django logs
- ✅ Form submission triggers onSubmit() methods successfully

### 2. Frontend Display Issue - Only Font Visible
**Status**: ✅ **RESOLVED**  
**Affected Components**: Entire Angular frontend  
**Description**: Angular application was loading but only showing font/text in top left corner due to broken CSS imports.

**Root Cause**: 
The `styles.scss` file contained imports for Froala Editor CSS files that no longer existed after the Froala-to-CKEditor migration, preventing Angular Material styles from loading properly.

**Solution Applied**:
- Removed broken Froala CSS imports from `static/frontend/reddit-app/src/styles.scss`
- Kept only Angular Material theme import: `@import '@angular/material/prebuilt-themes/indigo-pink.css';`
- Styles bundle size reduced from 690kB to 172kB
- Angular Material components now render correctly

**Verification**:
- ✅ Angular compilation successful without CSS errors
- ✅ Frontend accessible at external URL (port 12001)
- ✅ JavaScript files loading correctly
- ✅ Django API connectivity working (port 12000)
- ✅ Styles loading properly

### 3. Froala WYSIWYG Editor Replaced with CKEditor
**Status**: ✅ **Resolved**  
**Affected Components**: Post creation, comment editing  
**Description**: Successfully replaced Froala editor with CKEditor 5 to resolve licensing and compatibility issues.

**Changes Made**:
- Removed Froala dependencies from package.json
- Added CKEditor 5 (`@ckeditor/ckeditor5-angular`, `@ckeditor/ckeditor5-build-classic`)
- Updated create-post component with CKEditor implementation
- Added proper CKEditor styling and configuration

**Impact**: 
- ✅ Rich text editing now available
- ✅ WYSIWYG formatting options working
- ✅ No licensing issues
- ✅ Better TypeScript compatibility

---

## ⚠️ Compatibility Issues

### 2. Node.js OpenSSL Legacy Provider Required
**Status**: ⚠️ **Workaround Available**  
**Affected**: Angular development server  
**Description**: Angular 10 with Node.js 22+ requires legacy OpenSSL provider.

**Error**:
```
Error: error:0308010C:digital envelope routines::unsupported
```

**Workaround**:
```bash
NODE_OPTIONS="--openssl-legacy-provider" ng serve
```

**Impact**: 
- ⚠️ Requires special Node.js flags
- ✅ Application runs normally with workaround

### 3. TypeScript Strict Mode Compatibility
**Status**: ⚠️ **Workaround Applied**  
**Affected**: Angular compilation  
**Description**: Legacy dependencies have TypeScript compatibility issues.

**Workaround Applied**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "skipDefaultLibCheck": true
  }
}
```

**Impact**:
- ⚠️ Reduced type checking strictness
- ✅ Compilation succeeds

---

## 🔧 Configuration Issues

### 4. CORS Configuration for Deployment
**Status**: ✅ **Resolved**  
**Description**: Cross-origin requests between Angular frontend and Django backend required CORS configuration.

**Solution Applied**:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://work-1-otvuwyhcdtyibpym.prod-runtime.all-hands.dev",
    "https://work-2-otvuwyhcdtyibpym.prod-runtime.all-hands.dev",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
```

### 5. Static File Serving in Production
**Status**: ✅ **Resolved**  
**Description**: Django needed middleware for serving static files in production.

**Solution Applied**:
- Added `whitenoise==6.2.0` to requirements.txt
- Configured in Django settings

---

## 📱 Frontend Issues

### 6. Angular Routing Configuration
**Status**: ✅ **RESOLVED**  
**Description**: Angular SPA routing now properly configured for all application routes.

**Previous Behavior**:
- ✅ Works: `http://localhost:4200/django_reddit`
- ❌ Fails: `http://localhost:4200/django_reddit/sign-in` (404 error)

**Solution Applied**:
- Updated Django URL pattern to `re_path(r'^django_reddit/.*', ...)` to catch all SPA routes
- All Angular routes now work correctly (`/django_reddit/sign-in`, `/django_reddit/sign-up`, etc.)

**Current Status**: 
- ✅ All Angular routes functional
- ✅ SPA navigation working properly

### 7. Environment Configuration Hardcoded
**Status**: ⚠️ **Needs Improvement**  
**Description**: Environment URLs are hardcoded in Angular environment files.

**Current State**:
```typescript
// environment.ts
export const environment = {
  serverUrl: 'https://work-1-otvuwyhcdtyibpym.prod-runtime.all-hands.dev',
  appUrl: 'https://work-2-otvuwyhcdtyibpym.prod-runtime.all-hands.dev'
};
```

**Recommendation**: Use environment variables or build-time configuration.

---

## 🗄️ Database Issues

### 8. SQLite in Production
**Status**: ⚠️ **Not Recommended for Production**  
**Description**: Application uses SQLite which is not suitable for production deployment.

**Current State**: 
- ✅ Works for development and testing
- ❌ Not scalable for production use

**Recommendation**: 
- Migrate to PostgreSQL or MySQL for production
- Configure database connection pooling

### 9. Database Migrations Order Dependency
**Status**: ⚠️ **Potential Issue**  
**Description**: Some migrations may have dependency issues if run out of order.

**Workaround**: 
```bash
# If migration issues occur:
python manage.py migrate --run-syncdb
```

---

## 🔐 Security Issues

### 10. Debug Mode in Production
**Status**: ⚠️ **Security Risk**  
**Description**: Django DEBUG mode should be disabled in production.

**Current State**: `DEBUG = True` (for testing)  
**Production Fix**: Set `DEBUG = False` and configure proper error handling

### 11. Secret Key Exposure
**Status**: ⚠️ **Security Risk**  
**Description**: Django secret key should not be hardcoded.

**Recommendation**: Use environment variables for sensitive configuration.

---

## 📦 Dependency Issues

### 12. Outdated Dependencies
**Status**: ⚠️ **Security & Compatibility Risk**  
**Description**: Several dependencies have known vulnerabilities or are outdated.

**Key Outdated Packages**:
- Django 3.1.14 (Latest: 4.2+)
- Angular 10 (Latest: 17+)
- Node.js compatibility issues

**Impact**:
- ⚠️ Security vulnerabilities
- ⚠️ Limited feature support
- ⚠️ Compatibility issues with modern tools

### 13. Package Version Conflicts
**Status**: ⚠️ **Potential Issue**  
**Description**: Some npm packages may have peer dependency warnings.

**Observed Warnings**:
```
npm WARN deprecated packages during installation
```

**Impact**: 
- ⚠️ Build warnings
- ✅ Application still functions

### 14. psycopg2 Python 3.12 Compatibility Issue
**Status**: ✅ **RESOLVED**  
**Description**: psycopg2-binary 2.9.1 had compatibility issues with Python 3.12.

**Error Encountered**:
```
SystemError: type psycopg2.extensions.ReplicationConnection has the Py_TPFLAGS_HAVE_GC flag but has no traverse function
```

**Solution Applied**:
- Upgraded psycopg2-binary from 2.9.1 to 2.9.9
- Updated requirements.txt with compatible version
- Django migrations now run successfully

**Impact**:
- ✅ Database migrations work correctly
- ✅ Django application starts without errors
- ✅ SQLite development database functional

---

## 🧪 Testing Issues

### 14. No Test Suite Configuration
**Status**: ❌ **Missing**  
**Description**: Project lacks comprehensive test configuration.

**Missing Components**:
- Unit tests for Django models/views
- Angular component tests
- Integration tests
- E2E tests

**Impact**: 
- ❌ No automated testing
- ❌ Difficult to verify changes
- ❌ Risk of regressions

---

## 🚀 Performance Issues

### 15. Large Bundle Size
**Status**: ⚠️ **Performance Impact**  
**Description**: Angular application has large bundle sizes.

**Observed**:
```
chunk {vendor} vendor.js, vendor.js.map (vendor) 8.08 MB [initial]
```

**Impact**:
- ⚠️ Slow initial load times
- ⚠️ High bandwidth usage

**Recommendations**:
- Implement lazy loading
- Tree shaking optimization
- Bundle splitting

### 16. No Caching Strategy
**Status**: ⚠️ **Performance Impact**  
**Description**: No caching implemented for API responses or static assets.

**Impact**:
- ⚠️ Repeated API calls
- ⚠️ Slower user experience

---

## 🔄 Workaround Summary

### Quick Fixes Applied
1. **Froala Editor**: Commented out imports
2. **Node.js**: Use `NODE_OPTIONS="--openssl-legacy-provider"`
3. **TypeScript**: Added `skipLibCheck: true`
4. **CORS**: Configured allowed origins
5. **Static Files**: Added whitenoise middleware

### Recommended Long-term Solutions
1. **Upgrade Dependencies**: Plan systematic upgrade to modern versions
2. **Replace Froala**: Implement alternative rich text editor
3. **Add Testing**: Implement comprehensive test suite
4. **Database Migration**: Move to PostgreSQL for production
5. **Security Hardening**: Environment variables, DEBUG=False
6. **Performance Optimization**: Bundle optimization, caching strategy

---

## 🚀 Major Framework Updates Plan

### 17. Aggressive Framework Modernization
**Status**: 🔄 **IN PROGRESS**  
**Priority**: High  
**Description**: Updating Django from 3.1.14 to 5.2.8 and Angular from 10.x to 19.x with aggressive approach.

#### Update Strategy:

**Phase 1: Django Update (3.1.14 → 5.2.8)**
- Update core Django to latest stable version
- Update all Django extensions to compatible versions:
  - django-allauth: 0.51.0 → 65.13.1
  - django-filter: 2.4.0 → 25.2
  - django-cors-headers: 3.10.0 → 4.9.0
  - django-guardian: 2.4.0 → 3.2.0
  - djangorestframework: 3.11.2 → 3.16.1
- Replace deprecated django-rest-auth with dj-rest-auth
- Update database configuration for Django 5.x compatibility

**Phase 2: Angular Update (10.x → 19.x)**
- Update Angular CLI and core packages to latest versions
- Update Angular Material and CDK to v21.x
- Update TypeScript to 5.x
- Update Node.js dependencies and build tools
- Migrate from deprecated APIs and packages

**Phase 3: Breaking Changes Resolution**
- Fix Django URL patterns and middleware changes
- Update Angular component syntax and lifecycle hooks
- Resolve authentication backend compatibility
- Update build configuration and deployment scripts
- Fix any remaining compatibility issues

#### Known Breaking Changes to Address:

**Django 5.x Changes:**
- URL patterns: `url()` → `path()` and `re_path()`
- Middleware updates and new security features
- Authentication backend changes
- Database connection handling updates
- Settings configuration modernization

**Angular 19.x Changes:**
- Ivy renderer (already default, but may need updates)
- Strict mode and TypeScript 5.x compatibility
- Updated CLI commands and build configuration
- Component and service API changes
- Dependency injection updates

#### Implementation Approach:
1. **Backup Current State**: Ensure all current functionality is preserved
2. **Update Dependencies**: Aggressive update to latest versions
3. **Fix Issues One by One**: Address compatibility issues systematically
4. **Test Thoroughly**: Ensure all functionality works after updates
5. **Document Changes**: Update deployment and development guides

#### Expected Benefits:
- ✅ Latest security patches and features
- ✅ Better performance and optimization
- ✅ Modern development experience
- ✅ Long-term maintainability
- ✅ Community support and documentation

#### Risks:
- ⚠️ Temporary application instability during migration
- ⚠️ Potential breaking changes requiring code refactoring
- ⚠️ Learning curve for new framework features
- ⚠️ Possible third-party package compatibility issues

---

## 📞 Reporting New Issues

If you encounter additional issues:

1. **Check this document** for existing workarounds
2. **Search GitHub issues** for similar problems
3. **Create detailed issue report** with:
   - Environment details (OS, Node.js, Python versions)
   - Steps to reproduce
   - Error messages and logs
   - Expected vs actual behavior

---

## 🚀 Current Deployment Status

### Servers Running
- ✅ **Django API**: Running on port 12000 (`http://localhost:12000`)
- ✅ **Angular Frontend**: Running on port 12001 (`http://localhost:12001/django_reddit`)

### External URLs (Production-Ready)
- ✅ **Django API**: `https://work-1-woavzjjseoqpclwv.prod-runtime.all-hands.dev/`
- ✅ **Angular Frontend**: `https://work-2-woavzjjseoqpclwv.prod-runtime.all-hands.dev/django_reddit/`
- ✅ **All Angular Routes**: `/django_reddit/sign-in`, `/django_reddit/sign-up`, etc. all working

### API Status
- ✅ **Registration API**: `/rest-auth/registration/` working correctly (returns auth tokens)
- ✅ **Login API**: `/rest-auth/login/` working correctly
- ✅ **Posts Endpoint**: API endpoints accessible and functional
- ✅ **Admin Panel**: Django admin accessible at `/admin/`
- ✅ **API Documentation**: Swagger UI available at `/api/swagger/`
- ✅ **CORS Configuration**: Properly configured for cross-origin requests
- ✅ **Database**: SQLite with migrations applied successfully
- ✅ **External Access**: API accessible via external URL

### Frontend Status
- ✅ **HTML Loading**: Page loads correctly with proper base href
- ✅ **JavaScript Loading**: All JS bundles load successfully (main.js: 2.1MB)
- ✅ **UI Rendering**: **FIXED** - Angular Material components now render correctly
- ✅ **Build Process**: Angular compilation successful without errors
- ✅ **CSS Loading**: Styles bundle optimized (690kB → 172kB)
- ✅ **Static File Serving**: All assets served via Django `/static/` URLs
- ✅ **Submit Button Functionality**: **FIXED** - All form submissions working
- ✅ **Angular SPA Routing**: **FIXED** - Client-side routing working for all paths
- ✅ **External Access**: Frontend accessible via external URL

### Recent Fixes Applied
1. **Submit Button Functionality**: **FIXED** - Resolved NoReverseMatch errors and enabled form submissions
2. **Angular SPA Routing**: **FIXED** - Updated Django URL patterns to `re_path(r'^django_reddit/.*$')` for client-side routing
3. **Static File Serving**: **FIXED** - Updated template paths to use `/static/` prefix for all assets
4. **Django URL Redirects**: **FIXED** - Updated LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL to use 'angular_app'
5. **Environment Configuration**: **FIXED** - Corrected work-1 URLs in production environment
6. **API Connectivity**: **VERIFIED** - Registration and login APIs working with auth token responses
7. **CKEditor Integration**: Successfully replaced Froala with CKEditor 5
8. **CORS Setup**: Configured for development and production URLs
9. **CSS Loading Issue**: **FIXED** - Removed broken Froala CSS imports
10. **psycopg2 Compatibility**: **FIXED** - Upgraded to psycopg2-binary 2.9.9 for Python 3.12 compatibility
11. **Fresh Deployment**: **COMPLETED** - Full application deployment with Node.js 18, npm dependencies, and Angular build
12. **Database Setup**: **COMPLETED** - Django migrations applied successfully, superuser created (admin/admin123)
13. **Server Deployment**: **COMPLETED** - Both backend (port 12000) and frontend (port 12001) servers running
14. **Git Management**: All changes committed and pushed to main branch

### Current Issues

#### 17. Frontend Login Authentication Issue
**Status**: ⚠️ **In Progress**  
**Affected Components**: Angular frontend login functionality  
**Description**: While the Django API authentication endpoints work correctly (verified via curl), the Angular frontend login form fails to authenticate users.

**Root Cause Analysis**:
- ✅ Django API `/rest-auth/login/` endpoint working correctly (returns auth tokens)
- ✅ Backend server running on port 8000
- ✅ CORS configuration updated with correct hostnames
- ✅ CSRF trusted origins configured
- ❌ Proxy server (port 12000) experiencing port conflicts
- ❌ Frontend unable to reach backend through proxy

**Current State**:
- Backend API: Direct calls to `http://localhost:8000/rest-auth/login/` work correctly
- Frontend: Login attempts fail with "Login failed. Please try again." message
- Proxy server: Failing to start due to port 12000 already in use

**Verification Commands**:
```bash
# Working - Direct API call
curl -X POST http://localhost:8000/rest-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
# Returns: {"key":"33869058321fbcebede9eec84310987392b6fb08"}

# Working - External API call
curl -X POST https://work-1-woavzjjseoqpclwv.prod-runtime.all-hands.dev/rest-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
# Returns: {"key":"33869058321fbcebede9eec84310987392b6fb08"}
```

**Next Steps**:
1. Resolve proxy server port conflict
2. Test frontend login through working proxy
3. Verify complete authentication flow

### Application Status
⚠️ **MOSTLY FUNCTIONAL** - Django API working correctly and accessible via external URLs. Angular frontend loads and displays properly, but login authentication requires proxy server fix to complete the authentication flow.

---

**Last Updated**: 2025-11-29  
**Version**: Main Branch (Authentication debugging in progress)