from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Comment


@receiver(post_save, sender=Post)
def post_published_notification(sender, instance, created, **kwargs):
    """
    Send notification when a post is published
    """
    if instance.status == 'published' and not created:
        # In production, you would send actual emails
        # For now, we'll just print a notification
        print(f'Post "{instance.title}" has been published!')
        
        # Example email sending (configure EMAIL settings in production)
        # subject = f'New Post Published: {instance.title}'
        # message = f'Check out the new post: {instance.title}'
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    """
    Notify post author when someone comments on their post
    """
    if created:
        print(f'New comment on "{instance.post.title}" by {instance.user.username}')
        
        # Example: notify post author
        # if instance.user != instance.post.author:
        #     subject = f'New comment on your post: {instance.post.title}'
        #     message = f'{instance.user.username} commented: {instance.content[:100]}'
        #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.post.author.email])
