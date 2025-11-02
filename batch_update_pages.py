#!/usr/bin/env python3
"""
Batch update all pages with new email address
"""

import sys
sys.path.insert(0, '.')

from menwellbeing_setup import WordPressSetup

def main():
    print("="*60)
    print("Batch Updating All Pages with New Email")
    print("="*60)
    print()

    setup = WordPressSetup()

    # Test connection first
    if not setup.test_connection():
        print("❌ Connection failed. Aborting.")
        return False

    print("\nUpdating pages with ziad@menwellbeing.com...")
    print("-"*60)

    # Update all 4 pages
    pages = [
        {
            'title': 'About',
            'slug': 'about',
            'content': setup._get_about_content()
        },
        {
            'title': 'Contact',
            'slug': 'contact',
            'content': setup._get_contact_content()
        },
        {
            'title': 'Privacy Policy',
            'slug': 'privacy-policy',
            'content': setup._get_privacy_content()
        },
        {
            'title': 'Affiliate Disclosure',
            'slug': 'affiliate-disclosure',
            'content': setup._get_affiliate_content()
        }
    ]

    for page in pages:
        # Force update existing pages
        setup.create_page(page['title'], page['slug'], page['content'], force_update=True)

    print()
    print("="*60)
    print("✅ All pages updated successfully!")
    print("="*60)
    print()
    print("Updated pages:")
    print("- About: https://menwellbeing.com/about/")
    print("- Contact: https://menwellbeing.com/contact/")
    print("- Privacy Policy: https://menwellbeing.com/privacy-policy/")
    print("- Affiliate Disclosure: https://menwellbeing.com/affiliate-disclosure/")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
