
import os
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelnet.settings')
django.setup()

def create_admin():
    User = get_user_model()
    
    # Admin credentials (as requested)
    username = 'admin'
    email = ''
    password = 'admin123'
    
    # Remove ALL existing superusers first to ensure only one admin
    existing_superusers = User.objects.filter(is_superuser=True)
    for user in existing_superusers:
        user.is_superuser = False
        user.is_staff = False
        user.save()
        print(f"Removed superuser status from: {user.username}")
    
    # Create or update the single admin user
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"Updated existing user '{username}' to be the ONLY superuser")
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Created new superuser '{username}' as the ONLY admin")
    
    print(f"\n=== SINGLE ADMIN CREDENTIALS ===")
    print(f"Username: {username}")
    print(f"Email: {email or '(none)'}")
    print(f"Password: {password}")
    print(f"\nAdmin has FULL ACCESS to:")
    print(f"- All database tables")
    print(f"- User management (create, edit, delete users)")
    print(f"- All app data (books, reviews, clubs, etc.)")
    print(f"- Django admin interface at /admin/")
    print(f"\nIMPORTANT: This is the ONLY admin account!")
    print(f"IMPORTANT: Change the password immediately after first login!")

if __name__ == "__main__":
    create_admin()
