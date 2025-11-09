from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import time


class Command(BaseCommand):
    help = 'Creates admin user with known credentials'

    def handle(self, *args, **options):
        username = 'zohaib'
        email = 'zohaib@admin.com'
        password = 'zohaib123'
        
        self.stdout.write(self.style.WARNING('Starting create_admin command...'))
        
        try:
            # Delete existing user if exists
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(self.style.WARNING(f'Deleted existing user: {username}'))
            
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Created superuser: {username}'))
            
            # Wait for signal to create profile
            time.sleep(0.5)
            
            # Create or update profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'admin',
                    'bio': 'Administrator of the blog'
                }
            )
            if not created:
                profile.role = 'admin'
                profile.save()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Profile set to admin role'))
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS('🎉 ADMIN USER CREATED SUCCESSFULLY!'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating admin: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
