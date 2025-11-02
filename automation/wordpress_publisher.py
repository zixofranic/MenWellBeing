#!/usr/bin/env python3
"""
WordPress Post Publisher
Automatically publishes content to WordPress via REST API
"""

import requests
import json
import sys
from pathlib import Path
from datetime import datetime


class WordPressPublisher:
    """Publish posts to WordPress via REST API"""

    def __init__(self, config_path="../config.json"):
        """Initialize with WordPress credentials"""
        self.config = self._load_config(config_path)
        self.site_url = self.config['site_url'].rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.auth = (self.config['username'], self.config['app_password'])

    def _load_config(self, config_path):
        """Load WordPress credentials"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ ERROR: Configuration file '{config_path}' not found!")
            sys.exit(1)

    def get_category_id(self, category_name):
        """Get category ID by name, create if doesn't exist"""
        try:
            # Check if category exists
            response = requests.get(
                f"{self.api_base}/categories",
                params={'search': category_name},
                auth=self.auth,
                timeout=10
            )

            if response.status_code == 200 and response.json():
                # Category exists
                return response.json()[0]['id']
            else:
                # Create category
                response = requests.post(
                    f"{self.api_base}/categories",
                    json={'name': category_name},
                    auth=self.auth,
                    timeout=10
                )
                if response.status_code == 201:
                    return response.json()['id']
                else:
                    print(f"⚠️  Warning: Could not create category '{category_name}'")
                    return None

        except Exception as e:
            print(f"⚠️  Warning: Error with category '{category_name}': {e}")
            return None

    def create_post(self, title, content, categories=None, tags=None,
                   status='draft', featured_image_url=None):
        """
        Create WordPress post

        Args:
            title (str): Post title
            content (str): Post content (HTML or Gutenberg blocks)
            categories (list): List of category names
            tags (list): List of tag names
            status (str): 'draft' or 'publish'
            featured_image_url (str): URL to featured image

        Returns:
            dict: Post data with URL and ID
        """
        print("="*60)
        print(f"Creating WordPress Post: {title}")
        print("="*60)

        # Get category IDs
        category_ids = []
        if categories:
            for cat_name in categories:
                cat_id = self.get_category_id(cat_name)
                if cat_id:
                    category_ids.append(cat_id)

        # Prepare post data
        post_data = {
            'title': title,
            'content': content,
            'status': status,
            'categories': category_ids if category_ids else [],
        }

        # Add tags if provided
        if tags:
            # WordPress expects tag IDs, but we'll use tag names for simplicity
            # This requires tag creation endpoint
            post_data['tags'] = []  # TODO: Implement tag creation

        try:
            # Create post
            response = requests.post(
                f"{self.api_base}/posts",
                json=post_data,
                auth=self.auth,
                timeout=30
            )

            if response.status_code == 201:
                post_info = response.json()
                post_id = post_info['id']
                post_url = post_info['link']

                print(f"✅ Post created successfully!")
                print(f"   Status: {status.upper()}")
                print(f"   Post ID: {post_id}")
                print(f"   URL: {post_url}")

                if status == 'draft':
                    print(f"   Preview: {post_url}?preview=true")

                return {
                    'success': True,
                    'post_id': post_id,
                    'url': post_url,
                    'status': status
                }
            else:
                print(f"❌ Failed to create post")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text}")
                return {'success': False, 'error': response.text}

        except Exception as e:
            print(f"❌ Error creating post: {e}")
            return {'success': False, 'error': str(e)}

    def convert_markdown_to_gutenberg(self, markdown_content):
        """
        Convert markdown to WordPress Gutenberg blocks

        Note: This is a simplified converter
        For production, use proper markdown->Gutenberg library
        """
        # For now, we'll just use standard HTML
        # WordPress will auto-convert to blocks

        # Basic markdown to HTML conversion
        html = markdown_content

        # Headers
        html = html.replace('# ', '<h1>').replace('\n\n', '</h1>\n\n')
        html = html.replace('## ', '<h2>').replace('\n\n', '</h2>\n\n')
        html = html.replace('### ', '<h3>').replace('\n\n', '</h3>\n\n')

        # Bold
        import re
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)

        # Paragraphs
        paragraphs = html.split('\n\n')
        html = '\n\n'.join([f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs])

        return html


def main():
    """Example usage"""

    # Initialize publisher
    publisher = WordPressPublisher()

    # Example post
    title = "Test Post from Python"
    content = """
    <h2>This is a test post</h2>

    <p>This post was created programmatically using the WordPress REST API.</p>

    <p>Features:</p>
    <ul>
        <li>Auto-posting</li>
        <li>Category assignment</li>
        <li>Draft mode</li>
    </ul>
    """

    categories = ["What I Want"]

    # Create draft post
    result = publisher.create_post(
        title=title,
        content=content,
        categories=categories,
        status='draft'
    )

    if result['success']:
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print(f"View your draft post at:")
        print(f"{result['url']}?preview=true")
    else:
        print("\n" + "="*60)
        print("FAILED!")
        print("="*60)


if __name__ == "__main__":
    main()
