# Quick Start Guide

Get your Advanced Blog running in minutes!

## 🚀 Super Quick Setup

### 1. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```
Enter your desired username, email, and password when prompted.

### 5. Load Sample Data (Optional but Recommended)
```bash
python manage.py setup_sample_data
```

This will create:
- 5 categories (Technology, Lifestyle, Travel, Food, Health)
- 9 tags
- 5 sample blog posts
- 2 additional users (author1 and reader1)

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Access the Application

**Main Site:** http://127.0.0.1:8000/
**Admin Panel:** http://127.0.0.1:8000/admin/

## 👥 Test Accounts

After running `setup_sample_data`, you can login with:

| Role | Username | Password | Capabilities |
|------|----------|----------|--------------|
| Admin | admin | (your password) | Full access to everything |
| Author | author1 | author123 | Create/edit posts, access dashboard |
| Reader | reader1 | reader123 | Comment on posts |

## 📝 First Steps

### As an Admin:
1. Login at `/admin/`
2. Verify categories and tags
3. Review sample posts
4. Promote users to authors

### As an Author:
1. Login at `/accounts/login/`
2. Visit Dashboard
3. Create your first post
4. Add featured image, tags, and category

### As a Reader:
1. Register at `/accounts/register/`
2. Browse posts
3. Leave comments
4. Search for content

## 🎨 Customization Tips

### Change Site Colors
Edit `templates/base.html` and modify the gradient colors:
```css
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Add More Categories
```bash
python manage.py shell
```
```python
from blog.models import Category
Category.objects.create(name='Your Category', description='Description here')
exit()
```

### Change Posts Per Page
Edit `blog/views.py` in the `home` function:
```python
paginator = Paginator(posts, 12)  # Change from 9 to 12
```

## 🐛 Common Issues

### CKEditor Warning
The warning about CKEditor 4.22.1 is informational. For production, consider upgrading to CKEditor 5.

### Port Already in Use
```bash
python manage.py runserver 8080  # Use different port
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Locked Error
Close any database viewers or restart the server.

## 📚 Next Steps

1. **Customize Templates** - Modify files in `templates/`
2. **Add More Features** - Extend models in `blog/models.py`
3. **Style Changes** - Update CSS in `templates/base.html`
4. **Deploy** - Follow `DEPLOYMENT.md` for Vercel deployment

## 🔗 Useful URLs

- **Home:** `/`
- **Admin:** `/admin/`
- **Create Post:** `/post/create/`
- **Dashboard:** `/accounts/dashboard/`
- **Profile:** `/accounts/profile/`
- **Login:** `/accounts/login/`
- **Register:** `/accounts/register/`

## 💡 Pro Tips

1. **Always activate virtual environment** before running commands
2. **Run migrations** after model changes: `python manage.py makemigrations && python manage.py migrate`
3. **Collect static files** before deployment: `python manage.py collectstatic`
4. **Use search** to find posts quickly
5. **Tag posts properly** for better organization

## 🆘 Getting Help

- Check `README.md` for detailed documentation
- Review `DEPLOYMENT.md` for deployment instructions
- Check Django documentation: https://docs.djangoproject.com/

---

**Happy Blogging! 🎉**
