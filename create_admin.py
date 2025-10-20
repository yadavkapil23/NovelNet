#!/usr/bin/env python
"""
Create a new superuser for Django admin
"""
import os
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelnet.settings')
django.setup()

def create_admin():
    User = get_user_model()
    
    # Admin credentials
    username = 'novelnet'
    email = 'infonovelnet@gmail.com'
    password = 'novelnet@2787'
    
    # Remove any existing superusers first
    User.objects.filter(is_superuser=True).update(is_superuser=False, is_staff=False)
    print("Removed all existing superusers")
    
    # Create new superuser
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"Updated existing user '{username}' to superuser")
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Created new superuser '{username}'")
    
    print(f"Admin credentials:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("\nYou can now login to /admin/ with these credentials")
    print("IMPORTANT: Change the password immediately after first login!")

if __name__ == "__main__":
    create_admin()
