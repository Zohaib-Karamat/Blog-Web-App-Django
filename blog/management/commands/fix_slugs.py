from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post


class Command(BaseCommand):
    help = 'Fix any posts with missing or duplicate slugs'

    def handle(self, *args, **kwargs):
        posts_fixed = 0
        
        # Fix posts with empty slugs
        posts_without_slugs = Post.objects.filter(slug='')
        for post in posts_without_slugs:
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Post.objects.filter(slug=slug).exclude(pk=post.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            
            post.slug = slug
            post.save()
            posts_fixed += 1
            self.stdout.write(self.style.SUCCESS(f'Fixed slug for post: {post.title} -> {slug}'))
        
        if posts_fixed == 0:
            self.stdout.write(self.style.SUCCESS('No posts needed slug fixes'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully fixed {posts_fixed} post(s)'))
