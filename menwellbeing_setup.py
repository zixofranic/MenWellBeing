#!/usr/bin/env python3
"""
MenWellbeing.com WordPress Site Setup Automation
Uses WordPress REST API to create pages, categories, and navigation menus
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
from pathlib import Path


class WordPressSetup:
    """WordPress site setup automation using REST API"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize with configuration file"""
        self.config = self._load_config(config_path)
        self.site_url = self.config['site_url'].rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.auth = (self.config['username'], self.config['app_password'])

        # Setup logging
        log_filename = f"setup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Log file: {log_filename}")

        # Track created items
        self.created_categories = {}
        self.created_pages = {}

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            required_fields = ['site_url', 'username', 'app_password']
            for field in required_fields:
                if not config.get(field):
                    raise ValueError(f"Missing required field: {field}")

            return config
        except FileNotFoundError:
            print(f"❌ ERROR: Configuration file '{config_path}' not found!")
            print("Please create config.json with your WordPress credentials.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ ERROR: Invalid JSON in '{config_path}'")
            sys.exit(1)
        except ValueError as e:
            print(f"❌ ERROR: {e}")
            sys.exit(1)

    def test_connection(self) -> bool:
        """Test WordPress API connection and authentication"""
        self.logger.info("Testing WordPress API connection...")
        try:
            response = requests.get(
                f"{self.api_base}/users/me",
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 200:
                user = response.json()
                self.logger.info(f"✅ Connected successfully as: {user.get('name', 'Unknown')}")
                return True
            elif response.status_code == 401:
                self.logger.error("❌ Authentication failed. Check username and application password.")
                return False
            else:
                self.logger.error(f"❌ Connection failed with status {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Connection error: {e}")
            return False

    def create_category(self, name: str, slug: str, description: str, parent_id: Optional[int] = None) -> Optional[int]:
        """Create a WordPress category"""
        self.logger.info(f"Creating category: {name}")

        # Check if category already exists
        try:
            check_response = requests.get(
                f"{self.api_base}/categories",
                params={'slug': slug},
                auth=self.auth,
                timeout=10
            )

            if check_response.status_code == 200 and check_response.json():
                existing = check_response.json()[0]
                self.logger.info(f"⏭️  Category '{name}' already exists (ID: {existing['id']})")
                self.created_categories[slug] = existing['id']
                return existing['id']
        except Exception as e:
            self.logger.warning(f"Could not check for existing category: {e}")

        # Create new category
        data = {
            'name': name,
            'slug': slug,
            'description': description
        }

        if parent_id:
            data['parent'] = parent_id

        try:
            response = requests.post(
                f"{self.api_base}/categories",
                json=data,
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 201:
                category_id = response.json()['id']
                self.created_categories[slug] = category_id
                self.logger.info(f"✅ Created category '{name}' (ID: {category_id})")
                return category_id
            else:
                self.logger.error(f"❌ Failed to create category '{name}': {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error creating category '{name}': {e}")
            return None

    def create_page(self, title: str, slug: str, content: str, force_update: bool = False) -> Optional[int]:
        """Create a WordPress page"""
        self.logger.info(f"Creating page: {title}")

        # Check if page already exists
        try:
            check_response = requests.get(
                f"{self.api_base}/pages",
                params={'slug': slug},
                auth=self.auth,
                timeout=10
            )

            if check_response.status_code == 200 and check_response.json():
                existing = check_response.json()[0]
                self.logger.info(f"⚠️  Page '{title}' already exists (ID: {existing['id']})")

                # Ask user if they want to overwrite
                if not force_update:
                    self.logger.info(f"⏭️  Skipping '{title}' - already exists. Use force_update=True to overwrite.")
                    self.created_pages[slug] = existing['id']
                    return existing['id']
                else:
                    self.logger.info(f"🔄 Updating existing page '{title}'...")
                    # Will proceed to update below
                    return self._update_page(existing['id'], title, content, slug)

        except Exception as e:
            self.logger.warning(f"Could not check for existing page: {e}")

        # Create new page
        data = {
            'title': title,
            'slug': slug,
            'content': content,
            'status': 'publish'
        }

        try:
            response = requests.post(
                f"{self.api_base}/pages",
                json=data,
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 201:
                page_id = response.json()['id']
                self.created_pages[slug] = page_id
                self.logger.info(f"✅ Created page '{title}' (ID: {page_id})")
                return page_id
            else:
                self.logger.error(f"❌ Failed to create page '{title}': {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error creating page '{title}': {e}")
            return None

    def _update_page(self, page_id: int, title: str, content: str, slug: str) -> Optional[int]:
        """Update an existing WordPress page"""
        data = {
            'title': title,
            'slug': slug,
            'content': content,
            'status': 'publish'
        }

        try:
            response = requests.post(
                f"{self.api_base}/pages/{page_id}",
                json=data,
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 200:
                self.created_pages[slug] = page_id
                self.logger.info(f"✅ Updated page '{title}' (ID: {page_id})")
                return page_id
            else:
                self.logger.error(f"❌ Failed to update page '{title}': {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error updating page '{title}': {e}")
            return None

    def get_menu_locations(self) -> Dict:
        """Get available menu locations from theme"""
        try:
            # Try to get menu locations (requires authentication)
            response = requests.get(
                f"{self.site_url}/wp-json/wp-api-menus/v2/menu-locations",
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning("Could not fetch menu locations via API")
                return {}
        except Exception as e:
            self.logger.warning(f"Error fetching menu locations: {e}")
            return {}

    def create_menu(self, name: str, items: List[Dict], location: Optional[str] = None) -> bool:
        """
        Create a navigation menu
        Note: WordPress REST API doesn't fully support menus, so this provides instructions
        """
        self.logger.info(f"Menu creation: {name}")
        self.logger.info("ℹ️  Note: WordPress REST API has limited menu support.")
        self.logger.info("   Menus must be created manually in WordPress admin.")
        self.logger.info(f"   Menu name: {name}")
        if location:
            self.logger.info(f"   Location: {location}")
        self.logger.info("   Items to add:")
        for i, item in enumerate(items, 1):
            self.logger.info(f"   {i}. {item['title']} -> {item.get('type', 'custom')}")

        return True

    def run_setup(self) -> bool:
        """Run the complete setup process"""
        self.logger.info("="*60)
        self.logger.info("MenWellbeing.com WordPress Setup - Starting")
        self.logger.info("="*60)

        # Test connection
        if not self.test_connection():
            self.logger.error("Setup aborted due to connection failure")
            return False

        self.logger.info("\n" + "="*60)
        self.logger.info("STEP 1: Creating Categories")
        self.logger.info("="*60)

        # Create parent categories first
        parent_categories = [
            {
                'name': 'What I Want',
                'slug': 'what-i-want',
                'description': 'Products and gear that improve daily life',
                'parent': None
            },
            {
                'name': 'What I Need',
                'slug': 'what-i-need',
                'description': 'Support, resources, and help',
                'parent': None
            }
        ]

        for cat in parent_categories:
            self.create_category(cat['name'], cat['slug'], cat['description'])

        # Create child categories under "What I Want"
        want_children = [
            {
                'name': 'My Ride',
                'slug': 'my-ride',
                'description': 'Cars, motorcycles, and automotive',
                'parent': 'what-i-want'
            },
            {
                'name': 'My Gear',
                'slug': 'my-gear',
                'description': 'Sports, outdoor, and hobby equipment',
                'parent': 'what-i-want'
            },
            {
                'name': 'My Space',
                'slug': 'my-space',
                'description': 'Home, office, and workshop',
                'parent': 'what-i-want'
            },
            {
                'name': 'My Body',
                'slug': 'my-body',
                'description': 'Fitness, grooming, and wellness',
                'parent': 'what-i-want'
            }
        ]

        for cat in want_children:
            parent_id = self.created_categories.get(cat['parent'])
            if parent_id:
                self.create_category(cat['name'], cat['slug'], cat['description'], parent_id)
            else:
                self.logger.error(f"❌ Parent category '{cat['parent']}' not found for '{cat['name']}'")

        # Create child categories under "What I Need"
        need_children = [
            {
                'name': 'Mental Health',
                'slug': 'mental-health',
                'description': 'Therapy, support, and mental wellness',
                'parent': 'what-i-need'
            },
            {
                'name': 'Relationships',
                'slug': 'relationships',
                'description': 'Divorce, counseling, and connection',
                'parent': 'what-i-need'
            },
            {
                'name': 'Connection',
                'slug': 'connection',
                'description': 'Groups, community, and fighting loneliness',
                'parent': 'what-i-need'
            },
            {
                'name': 'Career',
                'slug': 'career',
                'description': 'Work, burnout, and purpose',
                'parent': 'what-i-need'
            }
        ]

        for cat in need_children:
            parent_id = self.created_categories.get(cat['parent'])
            if parent_id:
                self.create_category(cat['name'], cat['slug'], cat['description'], parent_id)
            else:
                self.logger.error(f"❌ Parent category '{cat['parent']}' not found for '{cat['name']}'")

        self.logger.info("\n" + "="*60)
        self.logger.info("STEP 2: Creating Pages")
        self.logger.info("="*60)

        pages = [
            {
                'title': 'About',
                'slug': 'about',
                'content': self._get_about_content()
            },
            {
                'title': 'Contact',
                'slug': 'contact',
                'content': self._get_contact_content()
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'content': self._get_privacy_content()
            },
            {
                'title': 'Affiliate Disclosure',
                'slug': 'affiliate-disclosure',
                'content': self._get_affiliate_content()
            }
        ]

        for page in pages:
            self.create_page(page['title'], page['slug'], page['content'])

        self.logger.info("\n" + "="*60)
        self.logger.info("STEP 3: Menu Creation Instructions")
        self.logger.info("="*60)

        # Main menu
        main_menu_items = [
            {'title': 'Home', 'type': 'custom', 'url': self.site_url},
            {'title': 'About', 'type': 'page', 'object': 'about'},
            {'title': 'What I Want', 'type': 'category', 'object': 'what-i-want'},
            {'title': 'What I Need', 'type': 'category', 'object': 'what-i-need'},
            {'title': 'Contact', 'type': 'page', 'object': 'contact'}
        ]

        self.create_menu('Main Menu', main_menu_items, 'primary')

        # Footer menu
        footer_menu_items = [
            {'title': 'Privacy Policy', 'type': 'page', 'object': 'privacy-policy'},
            {'title': 'Affiliate Disclosure', 'type': 'page', 'object': 'affiliate-disclosure'},
            {'title': 'Contact', 'type': 'page', 'object': 'contact'}
        ]

        self.create_menu('Footer Menu', footer_menu_items, 'footer')

        self.logger.info("\n" + "="*60)
        self.logger.info("Setup Complete!")
        self.logger.info("="*60)

        self._print_summary()
        self._print_manual_steps()

        return True

    def _print_summary(self):
        """Print summary of created items"""
        self.logger.info("\n📊 SUMMARY:")
        self.logger.info(f"   Categories created: {len(self.created_categories)}")
        self.logger.info(f"   Pages created: {len(self.created_pages)}")
        self.logger.info(f"   Menus to create manually: 2")

    def _print_manual_steps(self):
        """Print manual steps required"""
        self.logger.info("\n⚠️  MANUAL STEPS REQUIRED:")
        self.logger.info("\n1. Create Main Menu:")
        self.logger.info(f"   - Go to: {self.site_url}/wp-admin/nav-menus.php")
        self.logger.info("   - Create new menu named 'Main Menu'")
        self.logger.info("   - Add items: Home, About, What I Want, What I Need, Contact")
        self.logger.info("   - Assign to 'Primary' location")

        self.logger.info("\n2. Create Footer Menu:")
        self.logger.info(f"   - Go to: {self.site_url}/wp-admin/nav-menus.php")
        self.logger.info("   - Create new menu named 'Footer Menu'")
        self.logger.info("   - Add items: Privacy Policy, Affiliate Disclosure, Contact")
        self.logger.info("   - Assign to 'Footer' location")

        self.logger.info("\n3. Verify everything:")
        self.logger.info(f"   - Categories: {self.site_url}/wp-admin/edit-tags.php?taxonomy=category")
        self.logger.info(f"   - Pages: {self.site_url}/wp-admin/edit.php?post_type=page")

    # Content methods
    def _get_about_content(self) -> str:
        return """<!-- wp:heading {"level":1} -->
<h1>About MenWellbeing</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Most men's wellness sites get it wrong.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>They either tell you to buy supplements and gear like that'll fix everything, or they tell you material things don't matter and you just need therapy and meditation.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Both approaches miss the point.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What You Want. What You Need.</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Real wellbeing isn't either/or. It's both.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Some days, getting a new fishing rod or setting up a home gym actually helps. Having control over something tangible matters. Taking care of your car, your space, your body—these things aren't shallow. They're part of taking care of yourself.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>But gear and hobbies aren't substitutes for dealing with the hard stuff. Divorce, burnout, loneliness, mental health struggles—you can't buy your way out of those. Sometimes you need actual support from actual people.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>This site exists because both things are true:</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Taking care of the controllable stuff (your gear, your hobbies, your daily habits) genuinely improves your quality of life</li>
<li>Getting real help with the uncontrollable stuff (your relationships, your mental health, your purpose) is how you actually heal</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>What We Do</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>What I Want</strong> - Product research, gear guides, and recommendations for the tangible things that make daily life better. Cars, outdoor equipment, fitness gear, grooming, workspace setup. Honest takes on what's worth buying based on thorough research and real user feedback.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>What I Need</strong> - Real resources for the harder stuff. Therapists who get men's issues. Support groups that don't suck. Divorce resources. Mental health help. Career coaches. The support you might need but won't always ask for.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Our Approach</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We don't shame you for wanting nice things. We also don't pretend that buying things fixes everything.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>No guru bullshit. No "alpha male" nonsense. No generic wellness advice written by people who've never been through anything.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Just honest information about products worth buying and resources worth using, written for men who are dealing with real life.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What Makes This Different</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Most men's sites are either:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Affiliate content farms that'll recommend anything for a commission</li>
<li>Therapy-speak that doesn't understand how men actually talk</li>
<li>Toxic masculinity garbage that makes everything worse</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>We're none of those.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>This is a resource site</strong>, not a personal brand. We research products thoroughly, recommend support services that actually help, and write in plain language about things that matter.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>If you're here because you're going through something hard—divorce, career crisis, mental health struggles, or just feeling lost—you're not alone. Millions of men are dealing with the same things. Some gear helps with the day-to-day. Real support helps with the deeper stuff. Both are okay to need.</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:paragraph -->
<p><strong>Contact:</strong> ziad@menwellbeing.com</p>
<!-- /wp:paragraph -->"""

    def _get_contact_content(self) -> str:
        return """<!-- wp:heading {"level":1} -->
<h1>Contact</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Have questions, suggestions, or want to share your story?</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>[Note: Contact form will be added separately via WPForms plugin]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>We read every message. Response time is typically 24-48 hours.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>You can also email us directly at: ziad@menwellbeing.com</p>
<!-- /wp:paragraph -->"""

    def _get_privacy_content(self) -> str:
        return """<!-- wp:heading {"level":1} -->
<h1>Privacy Policy</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Last updated: November 2, 2025</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>MenWellbeing.com ("we," "our," or "us") respects your privacy. This Privacy Policy explains how we collect, use, and protect your information.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Information We Collect</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Information you provide:</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Email address (if you subscribe to our newsletter)</li>
<li>Name (if you fill out contact forms)</li>
<li>Any information you voluntarily share in messages</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p><strong>Automatically collected information:</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Log data (IP address, browser type, pages visited)</li>
<li>Cookies (for site functionality and analytics)</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>How We Use Your Information</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>To send you our newsletter (if you subscribed)</li>
<li>To respond to your inquiries</li>
<li>To improve our website</li>
<li>To analyze site usage via Google Analytics</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Third-Party Services</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We use:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Google Analytics</strong> - to understand how visitors use our site</li>
<li><strong>Amazon Associates</strong> - affiliate program (cookies may be placed)</li>
<li><strong>Email service providers</strong> - for newsletter delivery</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Affiliate Links</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>This site contains affiliate links. When you click these links and make a purchase, we may earn a commission at no additional cost to you. See our Affiliate Disclosure for details.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Your Rights</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>You can:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Unsubscribe from emails anytime</li>
<li>Request deletion of your data</li>
<li>Contact us with privacy concerns</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Contact</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>For privacy questions: ziad@menwellbeing.com</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Changes to This Policy</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We may update this policy. Changes will be posted on this page with a new "Last updated" date.</p>
<!-- /wp:paragraph -->"""

    def _get_affiliate_content(self) -> str:
        return """<!-- wp:heading {"level":1} -->
<h1>Affiliate Disclosure</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>MenWellbeing.com participates in affiliate marketing programs.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What This Means</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>When you click on certain links on this site and make a purchase, we may earn a commission at no additional cost to you.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>We are a participant in:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Amazon Services LLC Associates Program</li>
<li>Udemy Affiliate Program</li>
<li>Other affiliate programs</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Our Promise</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>We only recommend products and services we believe are valuable.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>All opinions are our own</li>
<li>We research products thoroughly before recommending them</li>
<li>We base recommendations on research, user reviews, and specifications</li>
<li>Commission rates do not influence our recommendations</li>
<li>We clearly mark affiliate links when possible</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>How It Works</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>When you click an affiliate link and make a purchase:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
<li>The company tracks that you came from our site</li>
<li>They pay us a small commission</li>
<li>Your price stays exactly the same</li>
<li>This helps us keep the site running and content free</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Transparency</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>We believe in transparency:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Affiliate relationships do not influence our honest opinions</li>
<li>We disclose affiliate links in articles</li>
<li>We never recommend products solely for commission</li>
<li>Your trust matters more than any commission</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2>Questions?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Contact us: ziad@menwellbeing.com</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:paragraph -->
<p><strong>Thank you for supporting MenWellbeing by using our links!</strong></p>
<!-- /wp:paragraph -->"""


def main():
    """Main entry point"""
    print("="*60)
    print("MenWellbeing.com WordPress Setup Automation")
    print("="*60)
    print()

    # Check if config exists
    config_path = Path("config.json")
    if not config_path.exists():
        print("❌ ERROR: config.json not found!")
        print()
        print("Please create config.json with your WordPress credentials:")
        print(json.dumps({
            "site_url": "https://your-site.com",
            "username": "your-username",
            "app_password": "your-application-password"
        }, indent=2))
        print()
        print("See README.md for detailed setup instructions.")
        sys.exit(1)

    try:
        setup = WordPressSetup()
        success = setup.run_setup()

        if success:
            print("\n✅ Setup completed successfully!")
            print("Check the log file for details.")
            sys.exit(0)
        else:
            print("\n❌ Setup failed. Check the log file for details.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.exception("Unexpected error during setup")
        sys.exit(1)


if __name__ == "__main__":
    main()
