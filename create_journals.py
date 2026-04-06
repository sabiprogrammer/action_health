import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'actionhealth.settings')
django.setup()

from journal.models import Journal
from account.models import User, Profile

print("Starting journal creation...")

# Create a test journal
user, created = User.objects.get_or_create(
    email='test@example.com',
    defaults={
        'staff': False,
        'admin': False,
        'is_active': True
    }
)
if created:
    user.set_password('password123')
    user.save()

profile, _ = Profile.objects.get_or_create(
    user=user,
    defaults={
        'full_name': 'Test Author',
        'professional_prefix': 'Dr.',
        'membership_level': 'fellow',
        'country': 'Nigerian',
        'gender': 'male'
    }
)

journal = Journal.objects.create(
    user=user,
    title='Test Journal on Public Health',
    sub_title='A test journal entry',
    abstract='This is a test abstract for the journal.',
    keywords='test, public health',
    full_journal='This is the full content of the test journal.',
    type='Research Article',
    field='Public Health',
    is_published=True
)

print(f"Created journal: {journal.title}")
print("Journal creation complete!")