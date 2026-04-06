#!/usr/bin/env python
import os
import sys
import json
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'actionhealth.settings')
django.setup()

from journal.models import Journal
from account.models import User, Profile

def create_journals_from_json():
    print("Loading journal data...")
    try:
        with open('journals_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: journals_data.json not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    print(f"Found {len(data)} authors to process")

    for author_data in data:
        print(f"Processing author: {author_data['full_name']}")

        # Create or get user
        user, created = User.objects.get_or_create(
            email=author_data['email'],
            defaults={
                'staff': False,
                'admin': False,
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  Created user: {user.email}")

        # Create or update profile
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': author_data['full_name'],
                'professional_prefix': author_data['professional_prefix'],
                'membership_level': author_data['membership_level'],
                'country': 'Nigerian',
                'gender': 'female' if 'sarah' in author_data['email'] else 'male'
            }
        )

        # Create journals for this author
        for journal_data in author_data['journals']:
            try:
                journal = Journal.objects.create(
                    user=user,
                    title=journal_data['title'],
                    sub_title=journal_data.get('sub_title', ''),
                    abstract=journal_data['abstract'],
                    keywords=journal_data.get('keywords', ''),
                    full_journal=journal_data['full_journal'],
                    type=journal_data.get('type', 'Research Article'),
                    field=journal_data['field'],
                    reviewed_by=journal_data.get('reviewed_by', ''),
                    contributor_id_number=journal_data.get('contributor_id_number', ''),
                    special_note=journal_data.get('special_note', ''),
                    is_published=True
                )
                print(f"  Created journal: {journal.title}")
            except Exception as e:
                print(f"  Error creating journal {journal_data['title']}: {e}")

    print("Journal creation complete!")

if __name__ == '__main__':
    create_journals_from_json()