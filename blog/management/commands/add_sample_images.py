from django.core.management.base import BaseCommand
from blog.models import Post
import urllib.request
import tempfile
from django.core.files import File


class Command(BaseCommand):
    help = 'Add sample images from Unsplash to posts without featured images'

    def handle(self, *args, **kwargs):
        # Category-based Unsplash images for variety
        category_images = {
            'Technology': 'https://images.unsplash.com/photo-1593720213428-28a5b9e94613?w=1200&h=800&fit=crop',  # Code/Programming
            'Lifestyle': 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1200&h=800&fit=crop',  # Workspace/Lifestyle
            'Travel': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&h=800&fit=crop',  # Travel/Adventure
            'Food': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=1200&h=800&fit=crop',  # Food/Healthy
            'Health': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1200&h=800&fit=crop',  # Wellness/Health
        }
        
        # Default fallback images
        default_images = [
            'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200&h=800&fit=crop',  # Writing/Blog
            'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1200&h=800&fit=crop',  # Article/Writing
        ]

        posts_updated = 0
        
        # Get all posts without featured images
        posts = Post.objects.filter(featured_image='')
        
        self.stdout.write(f'Found {posts.count()} posts without images')
        
        for idx, post in enumerate(posts):
            try:
                # Determine which image to use based on category
                if post.category and post.category.name in category_images:
                    image_url = category_images[post.category.name]
                else:
                    image_url = default_images[idx % len(default_images)]
                
                # Download image from Unsplash
                self.stdout.write(f'Downloading image for post ID: {post.id}')
                
                # Use standard library tempfile
                img_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                req = urllib.request.Request(
                    image_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    img_temp.write(response.read())
                    img_temp.flush()
                
                # Create a proper filename
                filename = f"{post.slug}.jpg"
                
                # Open the temp file and save to post
                with open(img_temp.name, 'rb') as f:
                    post.featured_image.save(filename, File(f), save=True)
                
                posts_updated += 1
                
                self.stdout.write(self.style.SUCCESS(f'Added image to post ID: {post.id}'))
                
                # Clean up temp file
                import os
                try:
                    os.unlink(img_temp.name)
                except:
                    pass
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to add image to post ID {post.id}: {str(e)}'))
        
        if posts_updated == 0:
            self.stdout.write(self.style.WARNING('No posts needed images'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\nSuccessfully added images to {posts_updated} post(s)'))
