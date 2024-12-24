from django.db import migrations
import os


def create_superuser(apps, schema_editor):

    User = apps.get_model('auth', 'User')


    superuser_username = os.getenv('SUPER_USER', 'admin')
    superuser_email = os.getenv('SUPER_USER_EMAIL', 'admin@example.com')
    superuser_password = os.getenv('SUPER_USER_PASSWORD', 'adminpassword')


    if not User.objects.filter(username=superuser_username).exists():
        User.objects.create_superuser(
            username=superuser_username,
            email=superuser_email,
            password=superuser_password,
        )
        print(f"Superuser '{superuser_username}' created successfully.")
    else:
        print(f"Superuser '{superuser_username}' already exists.")


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_created_at'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

