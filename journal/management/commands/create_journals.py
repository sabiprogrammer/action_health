from django.core.management.base import BaseCommand
from journal.models import Journal
from account.models import User, Profile

class Command(BaseCommand):
    help = 'Create sample journals'

    def handle(self, *args, **options):
        self.stdout.write('Starting journal creation...')

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
                self.stdout.write(f'Created user: {user.email}')

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
        ]

        for i, journal_data in enumerate(journals_data):
            try:
                journal = Journal.objects.create(
                    user=users[i % len(users)],
                    title=journal_data['title'],
                    sub_title=journal_data['sub_title'],
                    abstract=journal_data['abstract'],
                    keywords=journal_data['keywords'],
                    full_journal=journal_data['full_journal'],
                    type=journal_data['type'],
                    field=journal_data['field'],
                    reviewed_by=journal_data['reviewed_by'],
                    is_published=True
                )
                self.stdout.write(f'Created journal: {journal.title}')
            except Exception as e:
                self.stdout.write(f'Error creating journal {journal_data["title"]}: {e}')

        self.stdout.write('Journal creation complete!')