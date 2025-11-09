# Database Schema Documentation

## Entity Relationship Diagram

```
┌─────────────────────────┐
│         User            │
│  (Django Auth Model)    │
├─────────────────────────┤
│ id (PK)                 │
│ username                │
│ email                   │
│ password                │
│ first_name              │
│ last_name               │
│ is_staff                │
│ is_active               │
│ date_joined             │
└─────────────────────────┘
         │
         │ 1:1
         ▼
┌─────────────────────────┐
│        Profile          │
├─────────────────────────┤
│ id (PK)                 │
│ user_id (FK) UNIQUE     │
│ role                    │
│ bio                     │
│ avatar                  │
│ website                 │
│ twitter                 │
│ linkedin                │
│ created_at              │
│ updated_at              │
└─────────────────────────┘


         User
         │
         │ 1:N (author)
         ▼
┌─────────────────────────┐
│         Post            │
├─────────────────────────┤
│ id (PK)                 │
│ title                   │
│ slug UNIQUE             │
│ content                 │
│ excerpt                 │
│ author_id (FK)          │───────► User
│ category_id (FK)        │───┐
│ status                  │   │
│ featured_image          │   │
│ views                   │   │
│ created_at ◄─── INDEX   │   │
│ updated_at              │   │
└─────────────────────────┘   │
         │                     │
         │                     │
         │ M:N                 │ 1:N
         ▼                     ▼
┌─────────────────┐    ┌──────────────────┐
│      Tag        │    │    Category      │
├─────────────────┤    ├──────────────────┤
│ id (PK)         │    │ id (PK)          │
│ name UNIQUE     │    │ name UNIQUE      │
│ slug UNIQUE     │    │ slug UNIQUE      │
│ created_at      │    │ description      │
└─────────────────┘    │ created_at       │
                       └──────────────────┘

         Post
         │
         │ 1:N
         ▼
┌─────────────────────────┐
│       Comment           │
├─────────────────────────┤
│ id (PK)                 │
│ post_id (FK)            │───────► Post
│ user_id (FK)            │───────► User
│ content                 │
│ approved                │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
```

## Table Details

### 1. User (Django Default Auth Model)
**Purpose:** Store user authentication information

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| username | String(150) | UNIQUE, NOT NULL | Username for login |
| email | String(254) | | User's email address |
| password | String(128) | NOT NULL | Hashed password |
| first_name | String(150) | | User's first name |
| last_name | String(150) | | User's last name |
| is_staff | Boolean | DEFAULT False | Admin panel access |
| is_active | Boolean | DEFAULT True | Account active status |
| date_joined | DateTime | AUTO NOW ADD | Registration date |

**Relationships:**
- 1:1 with Profile
- 1:N with Post (as author)
- 1:N with Comment (as commenter)

---

### 2. Profile
**Purpose:** Extended user information and role management

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| user_id | Integer | FOREIGN KEY, UNIQUE | Link to User |
| role | String(10) | DEFAULT 'reader' | User role (reader/author/admin) |
| bio | Text | | User biography |
| avatar | ImageField | NULLABLE | Profile picture |
| website | URL | | Personal website |
| twitter | String(100) | | Twitter handle |
| linkedin | String(100) | | LinkedIn username |
| created_at | DateTime | AUTO NOW ADD | Profile creation date |
| updated_at | DateTime | AUTO NOW | Last update time |

**Relationships:**
- 1:1 with User

**Choices:**
- role: 'reader', 'author', 'admin'

**Signals:**
- Auto-created when User is created
- Auto-saved when User is saved

---

### 3. Category
**Purpose:** Organize posts into categories

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| name | String(100) | UNIQUE, NOT NULL | Category name |
| slug | String(100) | UNIQUE, AUTO | URL-friendly name |
| description | Text | | Category description |
| created_at | DateTime | AUTO NOW ADD | Creation date |

**Relationships:**
- 1:N with Post

**Methods:**
- `save()`: Auto-generates slug from name
- `get_absolute_url()`: Returns category URL

---

### 4. Tag
**Purpose:** Tag posts with keywords

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| name | String(50) | UNIQUE, NOT NULL | Tag name |
| slug | String(50) | UNIQUE, AUTO | URL-friendly name |
| created_at | DateTime | AUTO NOW ADD | Creation date |

**Relationships:**
- M:N with Post

**Methods:**
- `save()`: Auto-generates slug from name
- `get_absolute_url()`: Returns tag URL

---

### 5. Post
**Purpose:** Store blog post content

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| title | String(200) | NOT NULL | Post title |
| slug | String(200) | UNIQUE, AUTO | URL-friendly title |
| content | RichTextField | NOT NULL | Post content (HTML) |
| excerpt | Text(300) | | Brief description |
| author_id | Integer | FOREIGN KEY | Link to User |
| category_id | Integer | FOREIGN KEY, NULL | Link to Category |
| status | String(10) | DEFAULT 'draft' | Publication status |
| featured_image | ImageField | NULLABLE | Post thumbnail |
| views | Integer | DEFAULT 0 | View counter |
| created_at | DateTime | AUTO NOW ADD, INDEX | Creation date |
| updated_at | DateTime | AUTO NOW | Last update time |

**Relationships:**
- N:1 with User (author)
- N:1 with Category
- M:N with Tag
- 1:N with Comment

**Choices:**
- status: 'draft', 'published'

**Indexes:**
- created_at (descending)
- status

**Methods:**
- `save()`: Auto-generates slug from title
- `get_absolute_url()`: Returns post URL
- `comment_count`: Property returning approved comments count

**Signals:**
- Triggers notification when published

---

### 6. Comment
**Purpose:** Store user comments on posts

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Auto-incrementing ID |
| post_id | Integer | FOREIGN KEY | Link to Post |
| user_id | Integer | FOREIGN KEY | Link to User |
| content | Text | NOT NULL | Comment text |
| approved | Boolean | DEFAULT True | Moderation status |
| created_at | DateTime | AUTO NOW ADD | Comment date |
| updated_at | DateTime | AUTO NOW | Last edit time |

**Relationships:**
- N:1 with Post
- N:1 with User

**Signals:**
- Triggers notification when created

---

## Join Tables (Many-to-Many)

### Post_Tags (Auto-generated by Django)
**Purpose:** Link posts to tags

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | PRIMARY KEY |
| post_id | Integer | FOREIGN KEY to Post |
| tag_id | Integer | FOREIGN KEY to Tag |

---

## Sample Data

### Categories (5 default)
1. Technology
2. Lifestyle
3. Travel
4. Food
5. Health

### Tags (9 default)
1. Python
2. Django
3. Web Development
4. Tutorial
5. Tips
6. Guide
7. Beginner
8. Advanced
9. Best Practices

### User Roles
- **Admin:** Full control, user management
- **Author:** Create/edit posts, dashboard
- **Reader:** View posts, comment

---

## Database Queries Examples

### Get all published posts with author and category
```python
posts = Post.objects.filter(
    status='published'
).select_related(
    'author', 'category'
).prefetch_related(
    'tags'
)
```

### Get posts by category
```python
posts = Post.objects.filter(
    category__slug='technology',
    status='published'
)
```

### Get user's posts
```python
posts = Post.objects.filter(
    author=user
).order_by('-created_at')
```

### Get approved comments for a post
```python
comments = Comment.objects.filter(
    post=post,
    approved=True
).select_related('user')
```

### Search posts
```python
from django.db.models import Q

posts = Post.objects.filter(
    Q(title__icontains=query) |
    Q(content__icontains=query)
)
```

---

## Performance Optimization

### Indexes
- ✅ `created_at` on Post (for ordering)
- ✅ `status` on Post (for filtering)
- ✅ `slug` on all models (for lookups)

### Query Optimization
- ✅ `select_related()` for ForeignKey relationships
- ✅ `prefetch_related()` for ManyToMany relationships
- ✅ Limited pagination (9 posts per page)

### Caching Opportunities
- Category list (rarely changes)
- Tag cloud (rarely changes)
- Popular posts (can be cached for 1 hour)

---

## Data Integrity

### Cascading Rules
- **User deleted** → Profile CASCADE
- **User deleted** → Posts CASCADE
- **User deleted** → Comments CASCADE
- **Post deleted** → Comments CASCADE
- **Category deleted** → Posts SET_NULL

### Validation
- Unique slugs enforced at database level
- Email format validation
- Password strength validation
- Image file type validation

---

## Statistics Queries

### Dashboard Metrics
```python
total_posts = Post.objects.filter(author=user).count()
published = Post.objects.filter(author=user, status='published').count()
drafts = Post.objects.filter(author=user, status='draft').count()
```

### Popular Categories
```python
from django.db.models import Count

popular = Category.objects.annotate(
    post_count=Count('posts')
).filter(
    post_count__gt=0
).order_by('-post_count')[:5]
```

---

**Database Type:** SQLite (Development) / PostgreSQL (Production Recommended)

**ORM:** Django ORM

**Migrations:** Managed by Django migrations system
