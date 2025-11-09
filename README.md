# Advanced Blog Platform with Django

A full-featured, modern blog platform built with Django featuring user authentication, role-based permissions, rich text editing, and a beautiful gradient-based UI design.

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Core Functionality
- 📝 **Rich Text Editor** - CKEditor integration for beautiful content creation
- 🔐 **User Authentication** - Complete registration, login, and logout system
- 👥 **Role-Based Permissions** - Three user roles (Admin, Author, Reader)
- 💬 **Comment System** - Interactive commenting with moderation capabilities
- 🏷️ **Categories & Tags** - Organize content with categories and tags
- 🔍 **Advanced Search** - Search posts by title, content, and excerpt
- 📄 **Pagination** - Smooth pagination for better UX
- 🖼️ **Image Upload** - Featured images for posts and user avatars
- 📊 **Dashboard** - Author dashboard for managing posts and viewing stats
- 🔔 **Notifications** - Signal-based notifications for post publishing and comments

### UI/UX
- 🎨 **Modern Gradient Design** - Beautiful purple-based gradient theme
- 📱 **Fully Responsive** - Works perfectly on all devices
- ⚡ **Smooth Animations** - Hover effects and transitions
- 🎯 **Intuitive Navigation** - Easy-to-use interface
- 🌈 **Tailwind CSS** - Utility-first CSS framework

### SEO & Performance
- 🔗 **SEO-Friendly URLs** - Slug-based URLs for better SEO
- 🚀 **Optimized Queries** - Database query optimization with select_related and prefetch_related
- 📈 **View Tracking** - Post view counting
- 🗂️ **Database Indexes** - Optimized database performance

## 📋 Requirements

- Python 3.9+
- Django 5.2+
- SQLite (default) or PostgreSQL
- Pillow (for image handling)
- CKEditor (for rich text editing)
- Crispy Forms with Tailwind

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Blog\ App
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Create Sample Data (Optional)

Open Django shell:
```bash
python manage.py shell
```

Create categories and tags:
```python
from blog.models import Category, Tag

# Create categories
categories = ['Technology', 'Lifestyle', 'Travel', 'Food', 'Health']
for cat in categories:
    Category.objects.create(name=cat)

# Create tags
tags = ['Python', 'Django', 'Web Development', 'Tutorial', 'Tips', 'Guide']
for tag in tags:
    Tag.objects.create(name=tag)

exit()
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the blog!

## 👤 User Roles

### Reader (Default)
- View published posts
- Comment on posts
- Search and filter posts

### Author
- All Reader permissions
- Create, edit, and delete own posts
- Manage draft and published posts
- Access author dashboard

### Admin
- All Author permissions
- Manage all posts
- Moderate comments
- Access Django admin panel

## 📁 Project Structure

```
Blog App/
├── advanced_blog/          # Main project directory
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── blog/                  # Blog app
│   ├── models.py         # Post, Category, Tag, Comment models
│   ├── views.py          # Blog views
│   ├── forms.py          # Blog forms
│   ├── admin.py          # Admin customization
│   ├── urls.py           # Blog URL patterns
│   └── signals.py        # Post/comment signals
├── accounts/             # User management app
│   ├── models.py         # Profile model
│   ├── views.py          # Auth views
│   ├── forms.py          # Auth forms
│   ├── admin.py          # User admin customization
│   └── urls.py           # Accounts URL patterns
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── blog/            # Blog templates
│   └── accounts/        # Account templates
├── media/               # Uploaded files
├── static/              # Static files
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel deployment config
└── README.md           # This file
```

## 🎨 Database Schema

### Models Overview

**Post**
- title, slug, content, excerpt
- author (ForeignKey to User)
- category (ForeignKey to Category)
- tags (ManyToMany to Tag)
- status (Draft/Published)
- featured_image, views
- created_at, updated_at

**Category**
- name, slug, description
- created_at

**Tag**
- name, slug
- created_at

**Comment**
- post (ForeignKey to Post)
- user (ForeignKey to User)
- content, approved
- created_at, updated_at

**Profile**
- user (OneToOne to User)
- role (Reader/Author/Admin)
- bio, avatar, website
- twitter, linkedin
- created_at, updated_at

## 🔧 Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Features:
- ✅ Custom list displays with filters
- ✅ Search functionality
- ✅ Bulk actions for comments
- ✅ Auto-populated slugs
- ✅ Rich text editing
- ✅ User profile inline editing

## 📱 Pages

1. **Home** (`/`) - List of published posts with search and pagination
2. **Post Detail** (`/post/<slug>/`) - Full post with comments
3. **Category** (`/category/<slug>/`) - Posts filtered by category
4. **Tag** (`/tag/<slug>/`) - Posts filtered by tag
5. **Create Post** (`/post/create/`) - Create new post (Authors only)
6. **Edit Post** (`/post/<slug>/edit/`) - Edit existing post
7. **Delete Post** (`/post/<slug>/delete/`) - Delete confirmation
8. **Register** (`/accounts/register/`) - User registration
9. **Login** (`/accounts/login/`) - User login
10. **Profile** (`/accounts/profile/`) - User profile
11. **Edit Profile** (`/accounts/profile/edit/`) - Edit profile
12. **Dashboard** (`/accounts/dashboard/`) - Author dashboard

## 🚀 Deployment to Vercel

### Prerequisites
- Vercel account
- Git repository

### Steps

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Update Settings**

The project is already configured for Vercel with:
- `vercel.json` - Vercel configuration
- `build_files.sh` - Build script
- Updated `settings.py` - Production settings
- Updated `wsgi.py` - Vercel handler

3. **Deploy**

```bash
vercel
```

Follow the prompts to deploy your application.

4. **Set Environment Variables** (in Vercel Dashboard)
```
SECRET_KEY=your-secret-key
DEBUG=False
```

5. **Configure Database**

For production, consider using:
- PostgreSQL (Recommended)
- Vercel Postgres
- External database service

### Important Notes for Vercel Deployment

⚠️ **Media Files**: Vercel's serverless functions don't support persistent file storage. For production:
- Use cloud storage (AWS S3, Cloudinary, etc.)
- Configure Django to use remote storage for media files

⚠️ **Database**: SQLite won't persist on Vercel. Use:
- Vercel Postgres
- External PostgreSQL database
- Other cloud database services

## 🛠️ Configuration

### Changing User Roles

Access Django admin:
1. Go to `Users` in admin panel
2. Select a user
3. Scroll to `Profile` section
4. Change the `Role` field
5. Save

### CKEditor Customization

Edit `CKEDITOR_CONFIGS` in `settings.py`:
```python
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
    },
}
```

### Styling Customization

The project uses Tailwind CSS via CDN. Key gradient colors:
```css
.gradient-bg: #667eea to #764ba2 (Purple gradient)
.category-badge: #667eea to #764ba2
.tag-badge: #f093fb to #f5576c
```

## 📸 Screenshots

### Home Page
Beautiful gradient hero section with featured posts and search functionality.

### Post Detail
Rich content display with comments, tags, and related posts.

### Author Dashboard
Comprehensive dashboard showing post statistics and management options.

### Create/Edit Post
Rich text editor with image upload and category/tag selection.

## 🔐 Security Features

- ✅ CSRF protection
- ✅ Password hashing
- ✅ Permission-based access control
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection
- ✅ Secure password validators

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ by Zohaib Karamat

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact via email

## 🙏 Acknowledgments

- Django Documentation
- Tailwind CSS
- CKEditor
- Font Awesome
- Google Fonts (Inter)

---

**Happy Blogging! 🎉**
