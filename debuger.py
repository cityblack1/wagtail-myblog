from django.core.management import call_command

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_blog.settings.production')
django.setup()
call_command('runserver')

