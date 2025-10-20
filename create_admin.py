
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
    
    # Create or update the requested superuser, without altering others
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
    print(f"Email: {email or '(none)'}")
    print(f"Password: {password}")
    print("\nYou can now login to /admin/ with these credentials")
    print("IMPORTANT: Change the password immediately after first login!")

if __name__ == "__main__":
    create_admin()
