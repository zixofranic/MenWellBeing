#!/usr/bin/env python3
"""
MenWellbeing.com - Page Update Utility
Safely update WordPress pages with user confirmation
"""

import requests
import json
import sys
from pathlib import Path


def load_config(config_path="config.json"):
    """Load WordPress credentials"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Configuration file '{config_path}' not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ ERROR: Invalid JSON in '{config_path}'")
        sys.exit(1)


def get_page(site_url, auth, slug):
    """Fetch existing page by slug"""
    try:
        response = requests.get(
            f"{site_url}/wp-json/wp/v2/pages",
            params={'slug': slug},
            auth=auth,
            timeout=10
        )

        if response.status_code == 200 and response.json():
            return response.json()[0]
        return None
    except Exception as e:
        print(f"❌ Error fetching page: {e}")
        return None


def update_page(site_url, auth, page_id, title, content):
    """Update WordPress page"""
    try:
        response = requests.post(
            f"{site_url}/wp-json/wp/v2/pages/{page_id}",
            json={
                'title': title,
                'content': content,
                'status': 'publish'
            },
            auth=auth,
            timeout=10
        )

        if response.status_code == 200:
            print(f"✅ Successfully updated page '{title}' (ID: {page_id})")
            return True
        else:
            print(f"❌ Failed to update page: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating page: {e}")
        return False


def main():
    """Main entry point"""
    print("="*60)
    print("MenWellbeing.com - Page Update Utility")
    print("="*60)
    print()

    # Load config
    config = load_config()
    site_url = config['site_url'].rstrip('/')
    auth = (config['username'], config['app_password'])

    # Available pages
    pages = {
        '1': {'slug': 'about', 'title': 'About'},
        '2': {'slug': 'contact', 'title': 'Contact'},
        '3': {'slug': 'privacy-policy', 'title': 'Privacy Policy'},
        '4': {'slug': 'affiliate-disclosure', 'title': 'Affiliate Disclosure'}
    }

    # Show menu
    print("Select page to update:")
    print()
    for key, page in pages.items():
        print(f"{key}. {page['title']}")
    print()
    print("0. Exit")
    print()

    choice = input("Enter your choice (0-4): ").strip()

    if choice == '0':
        print("Exiting...")
        sys.exit(0)

    if choice not in pages:
        print("❌ Invalid choice!")
        sys.exit(1)

    selected = pages[choice]
    slug = selected['slug']
    title = selected['title']

    print()
    print(f"Selected: {title}")
    print("-"*60)

    # Fetch existing page
    print(f"Fetching current page content...")
    page = get_page(site_url, auth, slug)

    if not page:
        print(f"❌ Page '{title}' not found!")
        sys.exit(1)

    print(f"✅ Found page (ID: {page['id']})")
    print()
    print("Current content (first 200 chars):")
    print("-"*60)
    # Strip HTML tags for preview
    import re
    clean_text = re.sub('<[^<]+?>', '', page['content']['rendered'])
    print(clean_text[:200] + "..." if len(clean_text) > 200 else clean_text)
    print("-"*60)
    print()

    # Confirm update
    confirm = input(f"⚠️  Do you want to UPDATE this page? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("❌ Update cancelled.")
        sys.exit(0)

    # Get new content from main script
    print()
    print("📝 Fetching updated content from main script...")

    # Import content methods from main script
    sys.path.insert(0, str(Path(__file__).parent))
    from menwellbeing_setup import WordPressSetup

    # Create temporary instance to get content
    wp = WordPressSetup()

    # Get appropriate content based on slug
    content_methods = {
        'about': wp._get_about_content,
        'contact': wp._get_contact_content,
        'privacy-policy': wp._get_privacy_content,
        'affiliate-disclosure': wp._get_affiliate_content
    }

    if slug not in content_methods:
        print(f"❌ No content method found for '{slug}'")
        sys.exit(1)

    new_content = content_methods[slug]()

    print(f"✅ Got updated content")
    print()

    # Final confirmation
    final = input(f"🚀 Ready to update '{title}' on LIVE SITE. Proceed? (yes/no): ").strip().lower()

    if final != 'yes':
        print("❌ Update cancelled.")
        sys.exit(0)

    # Perform update
    print()
    print(f"Updating page '{title}'...")
    success = update_page(site_url, auth, page['id'], title, new_content)

    if success:
        print()
        print("="*60)
        print("✅ Page updated successfully!")
        print("="*60)
        print()
        print(f"View page: {site_url}/{slug}/")
    else:
        print()
        print("❌ Update failed. Check error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
