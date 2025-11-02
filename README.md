# MenWellbeing.com WordPress Setup Automation

Automated WordPress site setup script that creates pages, categories, and navigation structure for MenWellbeing.com using the WordPress REST API.

## What This Script Does

Automatically creates:
- **4 Pages**: About, Contact, Privacy Policy, Affiliate Disclosure (with full content)
- **10 Categories**: 2 parent categories with 4 child categories each
- **Instructions for 2 Menus**: Main Menu (header) and Footer Menu

## Prerequisites

- Python 3.7 or higher installed
- WordPress 5.6+ (for Application Password support)
- WordPress site with REST API enabled (enabled by default)
- Admin access to your WordPress site

## Setup Instructions

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests
```

### Step 2: Generate WordPress Application Password

1. Log into your WordPress admin dashboard
2. Go to **Users** → **Profile**
3. Scroll down to **Application Passwords** section
4. Enter a name like "Setup Script"
5. Click **Add New Application Password**
6. **Copy the generated password** (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
   - You won't be able to see it again!
   - Keep the spaces in the password

### Step 3: Create Configuration File

1. Copy the template:
   ```bash
   cp config.json.template config.json
   ```

2. Edit `config.json` with your credentials:
   ```json
   {
     "site_url": "https://menwellbeing.com",
     "username": "your-wordpress-admin-username",
     "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx"
   }
   ```

3. **Important**:
   - Use your actual WordPress username (not email)
   - Paste the application password WITH SPACES
   - Use `https://` (not `http://`)
   - No trailing slash on URL

### Step 4: Run the Script

```bash
python menwellbeing_setup.py
```

The script will:
1. Test connection to WordPress
2. Create all categories (parents first, then children)
3. Create all pages with content
4. Show instructions for creating menus
5. Generate a detailed log file

## Expected Output

```
============================================================
MenWellbeing.com WordPress Setup Automation
============================================================

Testing WordPress API connection...
✅ Connected successfully as: YourName

============================================================
STEP 1: Creating Categories
============================================================
Creating category: What I Want
✅ Created category 'What I Want' (ID: 2)
...

============================================================
STEP 2: Creating Pages
============================================================
Creating page: About
✅ Created page 'About' (ID: 5)
...

============================================================
Setup Complete!
============================================================
```

## What Gets Created

### Categories (10 total)

**Parent: What I Want**
- My Ride (cars, motorcycles, automotive)
- My Gear (sports, outdoor, hobby equipment)
- My Space (home, office, workshop)
- My Body (fitness, grooming, wellness)

**Parent: What I Need**
- Mental Health (therapy, support, wellness)
- Relationships (divorce, counseling, connection)
- Connection (groups, community, loneliness)
- Career (work, burnout, purpose)

### Pages (4 total)

1. **About** - Site mission and approach
2. **Contact** - Contact information and form placeholder
3. **Privacy Policy** - Full privacy policy
4. **Affiliate Disclosure** - Affiliate program disclosure

All pages are published immediately with complete content in WordPress block format.

## Manual Steps After Running Script

The WordPress REST API has limited menu support, so you'll need to create menus manually:

### Create Main Menu (Header)

1. Go to **Appearance** → **Menus**
2. Create new menu named "Main Menu"
3. Add these items in order:
   - Home (Custom Link to your homepage)
   - About (Page)
   - What I Want (Category)
   - What I Need (Category)
   - Contact (Page)
4. Assign to **Primary** location
5. Save

### Create Footer Menu

1. Create new menu named "Footer Menu"
2. Add these items:
   - Privacy Policy (Page)
   - Affiliate Disclosure (Page)
   - Contact (Page)
3. Assign to **Footer** location
4. Save

## Verification

After running the script, verify:

1. **Categories**:
   - Go to **Posts** → **Categories**
   - Should see 10 categories with proper hierarchy

2. **Pages**:
   - Go to **Pages** → **All Pages**
   - Should see 4 published pages

3. **View your site**:
   - Check that pages display correctly
   - Verify content formatting

## Troubleshooting

### Connection Failed

**Error**: `❌ Authentication failed`

**Solutions**:
- Verify username is correct (not email address)
- Regenerate application password and update config.json
- Ensure REST API is enabled on your WordPress site
- Check if your host blocks REST API

**Test REST API manually**:
```bash
curl https://your-site.com/wp-json/wp/v2/
```

### Items Already Exist

If you run the script multiple times:
- Existing pages/categories are **skipped automatically**
- Log will show: `⏭️  Page 'About' already exists`
- No duplicates will be created

### Missing Parent Category

**Error**: `❌ Parent category 'what-i-want' not found`

**Solution**:
- Parent categories must be created first
- Script creates them in correct order
- Check log file for errors in parent category creation

### Menu Creation Fails

WordPress REST API doesn't fully support menu creation. This is expected.

**Solution**:
- Follow manual menu creation steps above
- Or use a plugin like "WP REST API Menus" (not required)

### SSL/HTTPS Issues

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution** (temporary, for testing only):
```python
# In menwellbeing_setup.py, add to requests calls:
verify=False
```

**Better solution**: Fix SSL certificate on your host

## Log Files

Each run creates a timestamped log file:
- Format: `setup_log_YYYYMMDD_HHMMSS.txt`
- Contains detailed information about every action
- Keep for troubleshooting

## Security Notes

### Protecting Your Credentials

1. **Never commit config.json to version control**
   - It contains your application password
   - Add to `.gitignore`

2. **Delete application password after use**:
   - Go to **Users** → **Profile**
   - Click **Revoke** next to "Setup Script"

3. **This script is one-time use**:
   - Run it once to set up your site
   - Delete or secure the files afterward

### Safe Deletion

After successful setup:

```bash
# Delete sensitive files
rm config.json
rm setup_log_*.txt

# Optional: Keep script for reference
# Just remove config.json
```

## Re-Running the Script

Safe to run multiple times:
- Existing items are automatically skipped
- No duplicates created
- Only missing items are added

## Common Use Cases

### Add Only Missing Items

If you manually created some items:
- Script will skip existing items
- Only create what's missing

### Reset and Start Over

To completely reset:
1. Delete pages manually in WordPress
2. Delete categories manually
3. Re-run script

### Update Existing Content

Script doesn't update existing content. To update:
1. Delete items in WordPress admin
2. Re-run script

Or edit directly in WordPress admin.

## WordPress Version Requirements

- **Minimum**: WordPress 5.6+ (for Application Passwords)
- **Recommended**: WordPress 6.0+
- **Tested on**: WordPress 6.4

## Python Version Requirements

- **Minimum**: Python 3.7
- **Recommended**: Python 3.10+
- **Dependencies**: `requests` library only

## Theme Compatibility

Works with any WordPress theme:
- Tested with **GeneratePress**
- Creates standard WordPress content
- Uses Gutenberg block format
- Theme-agnostic implementation

## Support & Issues

If you encounter issues:

1. Check the log file for detailed errors
2. Verify WordPress version (5.6+)
3. Test REST API endpoint manually
4. Ensure application password is correct
5. Check host doesn't block REST API

## File Structure

```
MenWellBeing/
├── menwellbeing_setup.py       # Main script
├── config.json.template        # Configuration template
├── config.json                 # Your credentials (don't commit!)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── setup_log_*.txt            # Generated log files
└── Initial Run.txt            # Original requirements
```

## Technical Details

### API Endpoints Used

- `POST /wp-json/wp/v2/categories` - Create categories
- `POST /wp-json/wp/v2/pages` - Create pages
- `GET /wp-json/wp/v2/categories?slug=X` - Check existing categories
- `GET /wp-json/wp/v2/pages?slug=X` - Check existing pages
- `GET /wp-json/wp/v2/users/me` - Test authentication

### Authentication

Uses HTTP Basic Authentication with Application Password:
```
Username: wordpress_username
Password: application_password (with spaces)
```

### Content Format

Pages use WordPress Gutenberg block format:
- Proper block structure
- HTML comments for blocks
- Compatible with block editor
- Preserves formatting

## Advanced Usage

### Custom Configuration Path

```bash
python menwellbeing_setup.py --config /path/to/custom/config.json
```

### Dry Run (Check Only)

Edit script to add dry run mode:
```python
# Set at top of WordPressSetup class
self.dry_run = True
```

### Modify Content

Edit content methods in `menwellbeing_setup.py`:
- `_get_about_content()`
- `_get_contact_content()`
- `_get_privacy_content()`
- `_get_affiliate_content()`

## License

Free to use for MenWellbeing.com site setup.

## Credits

Built for MenWellbeing.com WordPress automation using WordPress REST API.

---

**Ready to run? Follow the setup steps above and execute:**

```bash
python menwellbeing_setup.py
```

**Questions?** Check the troubleshooting section or review the log files.
