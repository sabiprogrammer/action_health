#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'actionhealth.settings')
django.setup()

from journal.models import Journal
from account.models import User, Profile

def create_journals():
    print("Starting journal creation...")

    # Create users
    users_data = [
        {
            'email': 'dr.sarah.johnson@actionhealth.org',
            'full_name': 'Dr. Sarah Johnson',
            'professional_prefix': 'Dr.',
            'membership_level': 'fellow',
        },
        {
            'email': 'prof.michael.chen@actionhealth.org',
            'full_name': 'Prof. Michael Chen',
            'professional_prefix': 'Prof.',
            'membership_level': 'executive',
        },
    ]

    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'staff': False,
                'admin': False,
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.email}")

        # Create profile
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': user_data['full_name'],
                'professional_prefix': user_data['professional_prefix'],
                'membership_level': user_data['membership_level'],
                'country': 'Nigerian',
                'gender': 'female' if 'sarah' in user_data['email'] else 'male'
            }
        )
        users.append(user)

    # Create journals
    journals_data = [
        {
            'title': 'Epidemiological Trends in Non-Communicable Diseases in Urban Nigeria',
            'sub_title': 'A comprehensive analysis of cardiovascular diseases and diabetes prevalence',
            'abstract': 'This study examines the rising prevalence of non-communicable diseases (NCDs) in urban areas of Nigeria, with particular focus on cardiovascular diseases and diabetes.',
            'keywords': 'Epidemiology, Non-communicable diseases, Cardiovascular health, Diabetes',
            'full_journal': '## Introduction\n\nNon-communicable diseases (NCDs) have emerged as a significant public health challenge in Nigeria...',
            'type': 'Research Article',
            'field': 'Epidemiology',
            'reviewed_by': 'Prof. Elizabeth Thompson',
        },
        {
            'title': 'Health Policy Reforms and Universal Health Coverage in West Africa',
            'sub_title': 'Lessons from Ghana and Nigeria healthcare financing systems',
            'abstract': 'This comparative analysis examines health policy reforms aimed at achieving universal health coverage in West Africa.',
            'keywords': 'Health policy, Universal health coverage, Healthcare financing',
            'full_journal': '## Executive Summary\n\nUniversal Health Coverage (UHC) remains a critical goal for West African nations...',
            'type': 'Policy Analysis',
            'field': 'Health Policy and Management',
            'reviewed_by': 'Dr. Robert Mensah',
        },
        {
            'title': 'Maternal and Child Health Outcomes in Rural African Communities',
            'sub_title': 'Addressing malnutrition and infectious diseases in underserved populations',
            'abstract': 'This research investigates maternal and child health challenges in rural African settings, focusing on malnutrition prevention and infectious disease control.',
            'keywords': 'Maternal health, Child health, Malnutrition, Infectious diseases, Rural health',
            'full_journal': '## Background\n\nMaternal and child health remains a critical concern in many African rural communities...',
            'type': 'Research Article',
            'field': 'Maternal and Child Health',
            'reviewed_by': 'Dr. Grace Okafor',
        },
    ]

    for i, journal_data in enumerate(journals_data):
        try:
            journal, created = Journal.objects.get_or_create(
                title=journal_data['title'],
                defaults={
                    'user': users[i % len(users)],
                    'sub_title': journal_data['sub_title'],
                    'abstract': journal_data['abstract'],
                    'keywords': journal_data['keywords'],
                    'full_journal': journal_data['full_journal'],
                    'type': journal_data['type'],
                    'field': journal_data['field'],
                    'reviewed_by': journal_data['reviewed_by'],
                    'is_published': True
                }
            )
            if created:
                print(f"Created journal: {journal.title}")
            else:
                print(f"Journal already exists: {journal.title}")
        except Exception as e:
            print(f"Error creating journal {journal_data['title']}: {e}")

    print("Journal creation complete!")

if __name__ == '__main__':
    create_journals()