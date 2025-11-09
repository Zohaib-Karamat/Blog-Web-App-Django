# 🔧 Troubleshooting Guide

Common issues and their solutions.

## 🐛 Installation Issues

### Issue: `pip install` fails
**Solutions:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Use specific Python version
python3.9 -m pip install -r requirements.txt

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

### Issue: Virtual environment not activating
**Windows:**
```bash
# PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Issue: CKEditor security warning
**Solution:**
This is informational. For production, consider upgrading to CKEditor 5:
```bash
pip install django-ckeditor-5
```

---

## 🗄️ Database Issues

### Issue: `no such table` error
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Migrations conflict
**Solution:**
```bash
# Reset migrations (DEVELOPMENT ONLY!)
python manage.py migrate --run-syncdb
# Or delete db.sqlite3 and recreate
```

### Issue: Database locked
**Solutions:**
1. Close DB browser/viewer
2. Restart development server
3. Check for zombie processes
```bash
# Windows
tasklist | findstr python
taskkill /F /PID [pid]

# Linux/Mac
ps aux | grep python
kill -9 [pid]
```

---

## 🎨 Template Issues

### Issue: Template not found
**Check:**
1. Template exists in correct location
2. App in `INSTALLED_APPS`
3. `'APP_DIRS': True` in `TEMPLATES`
4. Correct template name in view

**Solution:**
```python
# In views.py
return render(request, 'blog/home.html', context)
# Not: 'home.html' or 'templates/blog/home.html'
```

### Issue: Static files not loading
**Solutions:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**In development:**
```python
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Issue: Images not displaying
**Check:**
1. `MEDIA_URL` and `MEDIA_ROOT` in settings
2. Media files routes in urls.py
3. Image file uploaded correctly
4. File permissions

**Solution:**
```python
# urls.py (development)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔐 Authentication Issues

### Issue: Can't login as admin
**Solution:**
```bash
# Create new superuser
python manage.py createsuperuser

# Or change password
python manage.py changepassword admin
```

### Issue: Permission denied errors
**Check:**
1. User logged in
2. User has correct role
3. `@login_required` decorator
4. Permission checks in views

**Example fix:**
```python
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if not request.user.profile.is_author:
        messages.error(request, 'Author permission required')
        return redirect('blog:home')
    # ...
```

### Issue: Profile not created for new user
**Solution:**
Check signals are connected:
```python
# accounts/apps.py
class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        import accounts.signals  # If you have signals
```

---

## 📝 Form Issues

### Issue: Form not saving
**Debug checklist:**
1. Form validation (`form.is_valid()`)
2. Print errors (`print(form.errors)`)
3. CSRF token in template
4. Correct form method (POST)

**Example debug:**
```python
if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save()
    else:
        print(form.errors)  # Debug line
```

### Issue: Image upload fails
**Check:**
1. Form has `enctype="multipart/form-data"`
2. View handles `request.FILES`
3. Pillow installed
4. MEDIA settings configured

**Template:**
```html
<form method="post" enctype="multipart/form-data">
```

**View:**
```python
form = PostForm(request.POST, request.FILES)
```

---

## 🔍 Search & Filter Issues

### Issue: Search returns no results
**Debug:**
```python
# Print query
print(f"Search query: {query}")

# Check database
posts = Post.objects.filter(
    title__icontains=query
)
print(f"Found {posts.count()} posts")
```

### Issue: Pagination not working
**Check:**
1. Paginator setup correct
2. `page` parameter in URL
3. Template has pagination links

**Example:**
```python
from django.core.paginator import Paginator

paginator = Paginator(posts, 9)
page_number = request.GET.get('page', 1)
page_obj = paginator.get_page(page_number)
```

---

## 🎭 UI/UX Issues

### Issue: Tailwind styles not working
**Solutions:**
1. Check CDN link in base.html
2. Clear browser cache
3. Hard refresh (Ctrl+F5)

**CDN should be:**
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### Issue: Responsive design broken
**Check:**
1. Viewport meta tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
2. Responsive classes (`md:`, `lg:`)
3. Test in different browsers

### Issue: Gradients not showing
**Check browser support:**
```css
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Fallback */
    background: #667eea;
}
```

---

## 🚀 Deployment Issues (Vercel)

### Issue: Build fails on Vercel
**Common causes:**
1. Missing dependencies
```bash
pip freeze > requirements.txt
```
2. Python version mismatch
```json
// vercel.json
"runtime": "python3.9"
```
3. Build script errors
```bash
chmod +x build_files.sh
```

### Issue: Static files 404 on production
**Solutions:**
1. Run collectstatic
```bash
python manage.py collectstatic --noinput
```
2. Check vercel.json routes
3. Verify STATIC_ROOT and STATIC_URL

### Issue: Database connection fails
**Check:**
1. DATABASE_URL environment variable
2. Database allows external connections
3. Correct database credentials
4. Database is PostgreSQL (not SQLite)

### Issue: Media files not persisting
**Solution:**
Vercel is serverless - use cloud storage:
```bash
# Install Cloudinary
pip install django-cloudinary-storage

# Configure in settings.py
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### Issue: 502 Bad Gateway
**Common causes:**
1. Code error in production
2. Database not configured
3. Missing environment variables
4. Build timeout

**Debug:**
```bash
# Check Vercel logs
vercel logs

# Test locally with production settings
DEBUG=False python manage.py runserver
```

---

## ⚡ Performance Issues

### Issue: Slow page load
**Solutions:**
1. Optimize queries
```python
# Use select_related
posts = Post.objects.select_related('author', 'category')

# Use prefetch_related
posts = posts.prefetch_related('tags')
```

2. Add database indexes
```python
class Meta:
    indexes = [
        models.Index(fields=['-created_at']),
    ]
```

3. Enable caching
4. Optimize images
5. Use CDN for static files

### Issue: Too many database queries
**Debug with Django Debug Toolbar:**
```bash
pip install django-debug-toolbar
```

**Or count queries:**
```python
from django.db import connection
# ... your code ...
print(f"Query count: {len(connection.queries)}")
```

---

## 🔧 Development Issues

### Issue: Server won't start
**Check:**
1. Port already in use
```bash
python manage.py runserver 8080  # Different port
```

2. Syntax errors
```bash
python manage.py check
```

3. Import errors
```bash
python manage.py shell
>>> import blog.models
```

### Issue: Changes not reflecting
**Solutions:**
1. Restart development server
2. Clear browser cache (Ctrl+Shift+R)
3. Check you're editing correct file
4. Run migrations if models changed

---

## 📱 Common Error Messages

### `ImportError: No module named ...`
**Solution:**
```bash
pip install [module-name]
# Or
pip install -r requirements.txt
```

### `CSRF verification failed`
**Solutions:**
1. Add `{% csrf_token %}` in form
2. Check CSRF_TRUSTED_ORIGINS
3. Clear cookies

### `TypeError: 'NoneType' object is not iterable`
**Debug:**
1. Check query returns results
2. Handle None cases
```python
posts = Post.objects.filter(...) or []
```

### `IntegrityError: NOT NULL constraint failed`
**Solution:**
Required field missing value:
```python
# Ensure all required fields provided
post = Post.objects.create(
    title='Test',
    content='Content',
    author=request.user  # Required!
)
```

---

## 🆘 Getting More Help

### Debug Mode
Enable detailed errors:
```python
# settings.py (DEVELOPMENT ONLY!)
DEBUG = True
```

### Django Shell
Test code interactively:
```bash
python manage.py shell
```

```python
>>> from blog.models import Post
>>> Post.objects.all()
>>> # Test your code here
```

### Check Configuration
```bash
python manage.py check
python manage.py check --deploy  # Production checks
```

### View SQL Queries
```python
print(Post.objects.filter(status='published').query)
```

### Logs
Check server console for error messages.

---

## 📚 Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Vercel Docs:** https://vercel.com/docs
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/django
- **Django Forum:** https://forum.djangoproject.com/

---

## 💬 Still Stuck?

1. **Read error message carefully** - it often tells you exactly what's wrong
2. **Google the error** - someone else likely had same issue
3. **Check documentation** - official docs are comprehensive
4. **Ask for help** - Django community is helpful
5. **Create minimal example** - isolate the problem

---

**Remember:**
- Read error messages completely
- Check the obvious first
- Test in isolation
- Use print() for debugging
- Keep calm and debug on! 🐛

**Happy debugging!** 🔧
