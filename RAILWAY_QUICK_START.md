# 🚀 Quick Railway Setup

## The Error You Saw
Railway couldn't find your Django app because your repo has multiple projects in folders.

## ✅ Solution - Set Root Directory

### In Railway Dashboard:

1. **Go to your project settings**
2. **Find "Root Directory" or "Source"**
3. **Set to:** `Blog App`
4. **Save**

That's it! Railway will now:
- ✅ Find your Django project
- ✅ Install dependencies from requirements.txt
- ✅ Run migrations automatically
- ✅ Start your app with Gunicorn

## 🎯 Required Environment Variables

Add in Railway:

```
DEBUG=False
SECRET_KEY=generate-a-new-secret-key
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 What We Added

✅ **Procfile** - Tells Railway how to start app
✅ **nixpacks.toml** - Build configuration
✅ **railway.json** - Deployment settings  
✅ **start.sh** - Startup script
✅ **requirements.txt** - Updated with production packages
✅ **settings.py** - Production-ready configuration

## 🔗 Database

Railway will automatically provide PostgreSQL.
No manual setup needed!

## 📝 Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create Railway project from GitHub repo
- [ ] Set Root Directory to `Blog App`
- [ ] Add PostgreSQL database
- [ ] Set environment variables
- [ ] Deploy!

## 🌐 Your URL

After deployment:
```
https://your-project-name.up.railway.app
```

## 🎉 That's It!

Your Django blog is production-ready for Railway!
