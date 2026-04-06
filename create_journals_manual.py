#!/usr/bin/env python
"""
Manual Journal Creation Script
Run this script to create journals for the Action Health website.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'actionhealth.settings')
django.setup()

from journal.models import Journal
from account.models import User, Profile

def main():
    print("=== Action Health Journal Creation Script ===")
    print("Creating journals with different authors...\n")

    # Create users
    users_data = [
        {
            'email': 'dr.sarah.johnson@actionhealth.org',
            'name': 'Dr. Sarah Johnson',
            'prefix': 'Dr.',
            'level': 'fellow',
            'gender': 'female'
        },
        {
            'email': 'prof.michael.chen@actionhealth.org',
            'name': 'Prof. Michael Chen',
            'prefix': 'Prof.',
            'level': 'executive',
            'gender': 'male'
        }
    ]

    users = []
    for user_info in users_data:
        # Create user
        user, created = User.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'is_active': True,
                'staff': False,
                'admin': False
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✓ Created user: {user_info['email']}")

        # Create profile
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': user_info['name'],
                'professional_prefix': user_info['prefix'],
                'membership_level': user_info['level'],
                'country': 'Nigerian',
                'gender': user_info['gender']
            }
        )
        if profile_created:
            print(f"✓ Created profile for: {user_info['name']}")

        users.append(user)

    # Create journals
    journals_data = [
        {
            'user': users[0],
            'title': 'Epidemiological Trends in Non-Communicable Diseases in Urban Nigeria',
            'sub_title': 'A comprehensive analysis of cardiovascular diseases and diabetes prevalence',
            'abstract': 'This study examines the rising prevalence of non-communicable diseases (NCDs) in urban areas of Nigeria, with particular focus on cardiovascular diseases and diabetes. Using data from multiple health facilities across Lagos and Abuja, we analyze trends over the past decade and identify key risk factors contributing to the NCD burden.',
            'keywords': 'Epidemiology, Non-communicable diseases, Cardiovascular health, Diabetes, Urban health',
            'full_journal': '''## Introduction

Non-communicable diseases (NCDs) have emerged as a significant public health challenge in Nigeria, particularly in urban areas where lifestyle changes and environmental factors contribute to increased disease burden. This study provides a comprehensive epidemiological analysis of NCD trends in major Nigerian cities.

## Methodology

Data was collected from 15 health facilities across Lagos and Abuja over a 10-year period (2014-2024). The study included:
- Retrospective analysis of patient records
- Cross-sectional surveys of risk factors
- Demographic and socioeconomic data collection

## Key Findings

### Cardiovascular Diseases
- Prevalence increased by 35% in urban areas
- Hypertension affects 28% of adults aged 30-60
- Stroke incidence rose by 42% in the study period

### Diabetes Mellitus
- Type 2 diabetes prevalence: 12.5% in urban populations
- Prediabetes affects 18% of the population
- Strong correlation with obesity and sedentary lifestyle

### Risk Factors
- Obesity: 45% of urban adults
- Physical inactivity: 62% report sedentary lifestyle
- Poor diet: High consumption of processed foods

## Discussion

The findings highlight the urgent need for comprehensive NCD prevention strategies in urban Nigeria. Key recommendations include:
- Implementation of city-wide health promotion programs
- Integration of NCD screening into primary healthcare
- Policy interventions to improve urban food environments
- Community-based lifestyle intervention programs

## Conclusion

The epidemiological transition in Nigeria demands immediate action to address the growing NCD burden. Urban areas face particular challenges that require targeted interventions combining healthcare system strengthening with population-level prevention strategies.''',
            'type': 'Research Article',
            'field': 'Epidemiology',
            'reviewed_by': 'Prof. Elizabeth Thompson',
            'contributor_id_number': 'AHII-2024-001',
            'special_note': 'Peer-reviewed and approved for publication'
        },
        {
            'user': users[1],
            'title': 'Health Policy Reforms and Universal Health Coverage in West Africa',
            'sub_title': 'Lessons from Ghana and Nigeria\'s healthcare financing systems',
            'abstract': 'This comparative analysis examines health policy reforms aimed at achieving universal health coverage (UHC) in West Africa, focusing on Ghana\'s National Health Insurance Scheme and Nigeria\'s ongoing healthcare financing reforms. The study evaluates policy effectiveness, implementation challenges, and recommendations for sustainable UHC.',
            'keywords': 'Health policy, Universal health coverage, Healthcare financing, West Africa, Policy reform',
            'full_journal': '''## Executive Summary

Universal Health Coverage (UHC) remains a critical goal for West African nations. This study compares health financing reforms in Ghana and Nigeria, providing insights for other countries in the region pursuing similar objectives.

## Background

West Africa faces significant healthcare financing challenges:
- Limited government health expenditure
- High out-of-pocket payments
- Fragmented health insurance systems
- Rapid population growth and urbanization

## Ghana's National Health Insurance Scheme (NHIS)

### Structure and Implementation
- Established in 2003
- Covers 40% of the population
- Premium-based system with government subsidies
- District Mutual Health Insurance Schemes

### Achievements
- Increased healthcare utilization by 25%
- Reduced catastrophic health expenditures
- Improved financial protection for vulnerable groups

### Challenges
- Sustainability concerns due to funding gaps
- Quality of care issues in some facilities
- Administrative inefficiencies

## Nigeria's Healthcare Financing Reforms

### Current System
- National Health Insurance Scheme (NHIS) established 2005
- Covers only 5% of the population
- Fragmented state-level implementations
- Heavy reliance on out-of-pocket payments

### Ongoing Reforms
- Basic Health Care Provision Fund (BHCPF)
- State Social Health Insurance Programs
- Private sector partnerships

### Implementation Barriers
- Weak institutional capacity
- Political interference in state programs
- Limited financial resources
- Poor data management systems

## Comparative Analysis

### Policy Effectiveness
- Ghana: More successful in expanding coverage
- Nigeria: Better integration with primary healthcare
- Both countries struggle with financial sustainability

### Key Success Factors
- Political commitment and leadership
- Stakeholder engagement
- Gradual implementation approach
- Monitoring and evaluation systems

## Recommendations

### For Nigeria
1. Strengthen NHIS institutional capacity
2. Increase government health financing to 5% of GDP
3. Develop state-level implementation frameworks
4. Improve data collection and management
5. Enhance private sector participation

### For West Africa Region
1. Regional knowledge sharing platforms
2. Harmonized health financing policies
3. Capacity building programs
4. South-South cooperation initiatives

## Conclusion

Achieving UHC in West Africa requires sustained political commitment, adequate financing, and strong institutional frameworks. While Ghana provides valuable lessons, each country must adapt reforms to their specific context and capacity constraints.''',
            'type': 'Policy Analysis',
            'field': 'Health Policy and Management',
            'reviewed_by': 'Dr. Robert Mensah',
            'contributor_id_number': 'AHII-2024-002',
            'special_note': 'Commissioned policy review'
        }
    ]

    for journal_info in journals_data:
        journal, created = Journal.objects.get_or_create(
            title=journal_info['title'],
            defaults={
                'user': journal_info['user'],
                'sub_title': journal_info['sub_title'],
                'abstract': journal_info['abstract'],
                'keywords': journal_info['keywords'],
                'full_journal': journal_info['full_journal'],
                'type': journal_info['type'],
                'field': journal_info['field'],
                'reviewed_by': journal_info['reviewed_by'],
                'contributor_id_number': journal_info['contributor_id_number'],
                'special_note': journal_info['special_note'],
                'is_published': True
            }
        )
        if created:
            print(f"✓ Created journal: {journal.title}")
            print(f"  Author: {journal.user.user_profile.full_name}")
            print(f"  Field: {journal.field}")
        else:
            print(f"⚠ Journal already exists: {journal.title}")

    print("\n=== Summary ===")
    total_journals = Journal.objects.filter(is_published=True).count()
    print(f"Total published journals: {total_journals}")

    print("\n✓ Journal creation completed successfully!")
    print("You can now view the journals at: http://127.0.0.1:8000/journal/")

if __name__ == '__main__':
    main()