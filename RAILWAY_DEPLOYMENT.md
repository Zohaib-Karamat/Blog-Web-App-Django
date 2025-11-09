# 🚂 Railway Deployment Guide for TechPulse Blog

## 📋 Prerequisites
- Railway account (https://railway.app)
- GitHub repository with your code
- PostgreSQL database (Railway provides this)

## 🚀 Deployment Steps

### 1. Push Your Code to GitHub
```bash
cd "e:\Web Developement\Django\Blog App"
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Create New Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `Zohaib-Karamat/Django-Journey`
5. **IMPORTANT**: Set the root directory to `Blog App`

### 3. Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a DATABASE_URL

### 4. Set Environment Variables

In Railway project settings, add these variables:

```env
# Required Variables
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this
ALLOWED_HOSTS=*.railway.app,*.up.railway.app

# Database (automatically provided by Railway)
DATABASE_URL=postgresql://... (already set by Railway)

# Optional: For media files in production
DISABLE_COLLECTSTATIC=0
```

**Generate a new SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Configure Root Directory

In Railway project settings:
- Go to "Settings" tab
- Find "Root Directory" option
- Set it to: `Blog App`
- Save changes

### 6. Deploy

Railway will automatically deploy when you push to GitHub.

To manually trigger deployment:
- Click "Deploy" button in Railway dashboard

## 🔍 Important Notes

### Database Migration
Railway will automatically run:
```bash
python manage.py migrate
```

### Static Files
WhiteNoise will serve static files automatically.

### Media Files (Images)
⚠️ **Important**: Railway's filesystem is ephemeral. For production, you need to use:
- **Cloudinary** (Recommended - Free tier available)
- **AWS S3**
- **Railway Volumes** (Persistent storage)

### Setting Up Cloudinary (Recommended)

1. Sign up at https://cloudinary.com
2. Install package:
```bash
pip install django-cloudinary-storage
```

3. Update settings.py:
```python
INSTALLED_APPS = [
    'cloudinary_storage',
    'cloudinary',
    # ... other apps
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your_cloud_name',
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

## 🐛 Troubleshooting

### Error: "Could not determine how to build the app"
**Solution**: Set Root Directory to `Blog App` in Railway settings

### Error: "Module not found"
**Solution**: Make sure requirements.txt is in the Blog App folder

### Static files not loading
**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

### Database connection error
**Solution**: Check DATABASE_URL is set in Railway environment variables

## 📊 Monitoring

- View logs: Railway Dashboard → Deployments → View Logs
- Check metrics: Railway Dashboard → Metrics tab

## 🔄 Updates

After making changes:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Railway will automatically redeploy.

## 📝 Commands Reference

Run commands in Railway:
```bash
# Access shell
railway shell

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic
```

## ✅ Post-Deployment Checklist

- [ ] Website accessible at *.railway.app URL
- [ ] Database connected (can create users)
- [ ] Static files loading (CSS, JS)
- [ ] Media uploads working (or Cloudinary configured)
- [ ] Admin panel accessible at /admin
- [ ] Can create and view blog posts
- [ ] Authentication working (login/register)

## 🎯 Your Deployment URL

After deployment, your site will be at:
```
https://your-project-name.up.railway.app
```

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Check Railway logs for specific errors

---

🎉 **Happy Deploying!**
