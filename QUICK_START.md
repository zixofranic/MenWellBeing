# Quick Start Guide

## 5-Minute Setup

### 1. Install Python Package
```bash
pip install requests
```

### 2. Create config.json

Create a file named `config.json` with this content:

```json
{
  "site_url": "https://menwellbeing.com",
  "username": "your-admin-username",
  "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx"
}
```

### 3. Get Application Password

1. Log into WordPress admin
2. Go to **Users** → **Profile**
3. Scroll to **Application Passwords**
4. Name it "Setup Script"
5. Click **Add New Application Password**
6. **Copy the password** and paste into `config.json`

### 4. Run Script

```bash
python menwellbeing_setup.py
```

### 5. Create Menus (Manual)

Go to **Appearance** → **Menus** in WordPress:

**Main Menu** (assign to Primary):
1. Home
2. About
3. What I Want
4. What I Need
5. Contact

**Footer Menu** (assign to Footer):
1. Privacy Policy
2. Affiliate Disclosure
3. Contact

## Done!

Your site now has:
- ✅ 10 categories with hierarchy
- ✅ 4 pages with full content
- ✅ Everything published and ready

## Need Help?

See README.md for detailed instructions and troubleshooting.
