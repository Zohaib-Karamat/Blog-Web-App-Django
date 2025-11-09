# Deployment Guide for Advanced Blog

This guide will help you deploy your Advanced Blog platform to Vercel.

## Prerequisites

- [Vercel Account](https://vercel.com/signup)
- [Git](https://git-scm.com/)
- [Vercel CLI](https://vercel.com/cli) (optional but recommended)

## Deployment Steps

### 1. Prepare Your Project

The project is already configured for Vercel deployment with:
- ✅ `vercel.json` - Vercel configuration file
- ✅ `build_files.sh` - Build script for collecting static files
- ✅ `requirements.txt` - Python dependencies
- ✅ Updated `wsgi.py` - Vercel serverless handler
- ✅ `.gitignore` - Git ignore file

### 2. Important Configuration Changes for Production

Before deploying, update `advanced_blog/settings.py`:

```python
# Update ALLOWED_HOSTS with your Vercel domain
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'your-custom-domain.com', 'localhost', '127.0.0.1']

# Set DEBUG to False for production
DEBUG = False

# Use environment variables for sensitive data
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-z)$p=58hao6xd)@zc855pl901qv1tphut+(34b1#*+@p%x!_1p')
```

### 3. Database Considerations

⚠️ **Important**: SQLite doesn't work well with Vercel's serverless architecture.

**Recommended Options:**

#### Option A: Vercel Postgres (Recommended)
```bash
# Install Vercel Postgres
vercel postgres create

# Connect to your project
vercel postgres connect
```

Update `settings.py`:
```python
import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

#### Option B: External PostgreSQL
Use services like:
- [ElephantSQL](https://www.elephantsql.com/)
- [Supabase](https://supabase.com/)
- [Railway](https://railway.app/)
- [AWS RDS](https://aws.amazon.com/rds/)

### 4. Media Files (Images)

⚠️ **Important**: Vercel's serverless functions don't support persistent file storage.

**Recommended Solutions:**

#### Option A: Cloudinary (Easiest)
```bash
pip install django-cloudinary-storage
```

Update `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
    # ...
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

#### Option B: AWS S3
```bash
pip install django-storages boto3
```

Update `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'storages',
    # ...
]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### 5. Deploy to Vercel

#### Method 1: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd "Blog App"
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name? advanced-blog (or your choice)
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Method 2: Using Vercel Dashboard

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/advanced-blog.git
git push -u origin main
```

2. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Configure build settings (usually auto-detected)
   - Click "Deploy"

### 6. Environment Variables

Set these in Vercel Dashboard (Settings → Environment Variables):

**Required:**
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url
```

**For Cloudinary:**
```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**For AWS S3:**
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### 7. Post-Deployment Setup

After successful deployment:

```bash
# Run migrations
vercel env pull .env.local
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Setup sample data (optional)
python manage.py setup_sample_data

# Collect static files (if needed)
python manage.py collectstatic --noinput
```

### 8. Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Navigate to "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. Update `ALLOWED_HOSTS` in `settings.py`

## Vercel Configuration Details

### vercel.json Explained

```json
{
  "version": 2,
  "builds": [
    {
      "src": "advanced_blog/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/media/(.*)",
      "dest": "/media/$1"
    },
    {
      "src": "/(.*)",
      "dest": "advanced_blog/wsgi.py"
    }
  ]
}
```

- **builds**: Defines how to build your application
- **routes**: Defines URL routing (static files, media, and application)

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Ensure `python manage.py collectstatic` runs successfully
   - Check `STATIC_ROOT` and `STATIC_URL` in settings.py
   - Verify routes in `vercel.json`

2. **Database connection errors**
   - Verify `DATABASE_URL` environment variable
   - Check database connection from local environment
   - Ensure database allows connections from Vercel IPs

3. **Import errors**
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility

4. **Media files not persisting**
   - Remember: Vercel is serverless and doesn't persist files
   - Use Cloudinary or S3 for media storage

5. **Build timeout**
   - Reduce `maxLambdaSize` if needed
   - Optimize dependencies in requirements.txt

### Useful Commands

```bash
# View deployment logs
vercel logs

# List all deployments
vercel ls

# Remove a deployment
vercel remove [deployment-url]

# Environment variables
vercel env ls
vercel env add
vercel env rm
```

## Performance Optimization

1. **Enable Caching**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
    }
}
```

2. **Optimize Database Queries**
   - Use `select_related()` and `prefetch_related()`
   - Add database indexes
   - Monitor query performance

3. **CDN for Static Files**
   - Use Cloudflare
   - Enable Vercel's Edge Caching

## Security Checklist

- ✅ Set `DEBUG = False` in production
- ✅ Use strong `SECRET_KEY`
- ✅ Configure `ALLOWED_HOSTS`
- ✅ Enable HTTPS (automatic on Vercel)
- ✅ Set up CSRF protection
- ✅ Use environment variables for secrets
- ✅ Enable security middleware
- ✅ Regular dependency updates

## Monitoring

### Vercel Analytics
Enable analytics in your project settings to monitor:
- Page views
- Performance metrics
- Geographic distribution
- Error rates

### Application Monitoring
Consider using:
- [Sentry](https://sentry.io/) - Error tracking
- [New Relic](https://newrelic.com/) - APM
- [LogRocket](https://logrocket.com/) - Session replay

## Costs

### Free Tier Includes:
- Unlimited deployments
- 100GB bandwidth
- Custom domains
- Automatic HTTPS

### Paid Features:
- Team collaboration
- Advanced analytics
- Priority support
- Increased limits

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Community Discord](https://discord.gg/vercel)

---

**Good luck with your deployment! 🚀**

Need help? Check the troubleshooting section or create an issue in the repository.
