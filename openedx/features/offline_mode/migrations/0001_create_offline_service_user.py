"""Create the account the ZIP builder renders as. Not part of the upstream draft."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations


def forwards(apps, schema_editor):
    User = get_user_model()
    username = settings.OFFLINE_SERVICE_WORKER_USERNAME
    # auth_user.email is unique in this database, so each account needs its own placeholder.
    user, _created = User.objects.get_or_create(
        username=username,
        defaults={"email": username + "@fake.email"},
    )
    user.is_active = True
    user.is_staff = False
    user.is_superuser = False
    user.set_unusable_password()
    user.save()


def backwards(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(username=settings.OFFLINE_SERVICE_WORKER_USERNAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.RunPython(forwards, backwards),
    ]
