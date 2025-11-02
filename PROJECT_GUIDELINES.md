# MenWellbeing.com - Project Guidelines & Best Practices

**READ THIS FILE AT THE START OF EVERY WORK SESSION**

Last Updated: November 2, 2025

---

## 🚨 IMPORTANT: Content Strategy CSVs Available

We have **100+ researched content topics** ready to produce in 4 CSV files:
- `content_what_i_want.csv` (35 topics)
- `content_what_i_need.csv` (40 topics)
- `content_first_timer.csv` (30 topics)
- `content_master_dashboard.csv` (overview)

**When user asks to create content:**
1. Read `CSV_USAGE_GUIDE.md` (has full instructions)
2. Open relevant CSV file
3. Filter by Status="Not Started", sort by Priority/Traffic
4. Present top options to user
5. Create content based on research in CSV
6. Update Status to "Published"

**These CSVs are your content roadmap. Use them for all content planning and tracking.**

---

## Project Overview

**Site:** https://menwellbeing.com
**Purpose:** Men's wellness resource site covering products (What I Want) and support resources (What I Need)
**Platform:** WordPress + GeneratePress Theme
**Owner:** Ziad

---

## Critical Rules - MUST FOLLOW

### 1. Act as a Full Stack Developer
- **Take initiative and be proactive**
- **Make routine development decisions autonomously**
- **Don't ask for permission on standard tasks** (updates, fixes, improvements)
- **Only ask when:**
  - Major architectural changes
  - Deleting significant content/data
  - Changing core site structure
  - Security or legal implications
- **Do ask when unclear, but default to action**
- Think like a professional developer on the team

### 2. Content Updates and Changes
- **Check if pages/posts exist before modifying**
- **Log all changes made**
- **For routine updates** (typos, email changes, content improvements): Just do it
- **For major rewrites**: Show user the changes if significant
- **Default to making improvements** rather than asking first

### 3. Contact Information
**Primary Email:** ziad@menwellbeing.com
- Use this email in ALL pages, content, and communications
- Do NOT use contact@menwellbeing.com or any other email
- If you see old email addresses, flag them for update

### 4. Content Preservation
- Log all changes made to the site
- Keep backups of original content before modifications
- Document what was changed and why
- User can always rollback if needed

### 5. WordPress Credentials - SECURITY
**Never commit these to git:**
- config.json (WordPress credentials)
- SSH keys
- Passwords
- Application passwords
- Log files with sensitive data

**Files are gitignored:**
- config.json
- setup_log_*.txt
- ssh_key_temp

---

## Site Structure

### Categories (10 total)

**Parent: What I Want** (Products and gear)
- My Ride (cars, motorcycles, automotive)
- My Gear (sports, outdoor, hobby equipment)
- My Space (home, office, workshop)
- My Body (fitness, grooming, wellness)

**Parent: What I Need** (Support and resources)
- Mental Health (therapy, support, wellness)
- Relationships (divorce, counseling, connection)
- Connection (groups, community, fighting loneliness)
- Career (work, burnout, purpose)

### Core Pages

1. **About** - Site mission and approach
2. **Contact** - Contact form and email
3. **Privacy Policy** - Privacy and data policy
4. **Affiliate Disclosure** - Affiliate program disclosure

### Navigation Menus

**Main Menu (Header/Primary):**
1. Home
2. About
3. What I Want
4. What I Need
5. Contact

**Footer Menu:**
1. Privacy Policy
2. Affiliate Disclosure
3. Contact

---

## File Structure

```
D:\Work\2025\MenWellBeing\
├── PROJECT_GUIDELINES.md          # THIS FILE - Read first!
├── CSV_USAGE_GUIDE.md            # How to use content tracking CSVs - Read second!
├── Initial Run.txt                # Original project requirements
├── menwellbeing_setup.py         # WordPress automation script
├── config.json                    # WordPress credentials (DO NOT COMMIT)
├── config.json.template           # Safe template for credentials
├── requirements.txt               # Python dependencies
├── README.md                      # Setup documentation
├── QUICK_START.md                # Quick setup guide
├── .gitignore                    # Git ignore rules
├── ClaudePassword.txt            # SSH and credentials (DO NOT COMMIT)
├── ssh_key_temp                  # SSH key (DO NOT COMMIT)
├── setup_log_*.txt               # Execution logs (DO NOT COMMIT)
│
├── CONTENT STRATEGY CSVs (100+ topics researched):
├── content_what_i_want.csv       # 35 product/gear topics
├── content_what_i_need.csv       # 40 support/resource topics
├── content_first_timer.csv       # 30 "First Time X" blended topics
├── content_master_dashboard.csv  # Overview and tracking
└── CONTENT_STRATEGY.md           # Research documentation (reference only)
```

---

## Development Workflow

### Before Making Any Changes:

1. **Read this file** (PROJECT_GUIDELINES.md)
2. **Check what exists** on the live site
3. **Ask user for approval** if modifying existing content
4. **Test locally** if possible
5. **Document changes** in logs
6. **Verify changes** worked correctly

### When Creating/Updating Content:

1. **Check if it exists first:**
   ```python
   # Script already checks existence
   # If exists, ASK USER before overwriting
   ```

2. **Show user what will change:**
   - What currently exists
   - What the new version will be
   - Get explicit approval

3. **After changes:**
   - Verify on live site
   - Log what was done
   - Confirm with user

### When Running Scripts:

1. **Always use the existing script:** `menwellbeing_setup.py`
2. **Check config.json exists** and has correct credentials
3. **Review log files** after execution
4. **Python path:** `/c/Users/ziadf/AppData/Local/Programs/Python/Python312/python.exe`

---

## WordPress REST API Details

**Endpoint:** https://menwellbeing.com/wp-json/wp/v2/
**Authentication:** HTTP Basic Auth with Application Password
**Username:** ziadfeg@gmail.com
**App Password:** Stored in config.json

### API Usage Rules:

- Check for existing content before creating
- Handle errors gracefully
- Log all API calls
- Never expose credentials in logs
- Respect rate limits

---

## SSH Access Details (If Needed)

**Hostname:** ssh.menwellbeing.com
**Port:** 18765
**Username:** u1830-zzv3lgurefnk
**Key:** SSH key in ClaudePassword.txt (encrypted with passphrase)

**Note:** SSH key requires passphrase. REST API is preferred method.

---

## Content Guidelines

### Tone and Voice:
- Direct, honest, no BS
- Written for men dealing with real issues
- Not preachy or guru-like
- No toxic masculinity
- No over-the-top marketing speak
- Plain language, relatable

### Email References:
- **ALWAYS use:** ziad@menwellbeing.com
- **NEVER use:** contact@menwellbeing.com (outdated)

### Page Content Rules:
- Use WordPress Gutenberg block format
- All pages should be published (not draft)
- Include proper headings hierarchy
- Mobile-friendly formatting
- SEO-friendly structure

---

## Script Behavior - Important Notes

### Current Script (`menwellbeing_setup.py`):

**What it does:**
- Creates categories with parent/child hierarchy
- Creates pages with full content
- Checks if items exist before creating
- Skips existing items automatically
- Logs all actions

**What it does NOT do:**
- Does NOT create menus (must be manual)
- Does NOT delete anything
- Does NOT update existing content by default

### Modified Behavior (After Updates):

**When page exists:**
1. Detect existing page
2. **ASK USER:** "Page 'About' exists. Do you want to overwrite it?"
3. Wait for user confirmation
4. Only proceed if user says yes
5. Log the decision

---

## Common Tasks

### Task: Update Page Content

1. Ask user which page to update
2. Show current content
3. Show proposed new content
4. Get explicit approval
5. Update via REST API
6. Verify changes live
7. Log the update

### Task: Create New Page/Post

1. Check if slug/title exists
2. If exists, ask user
3. Create content
4. Publish or draft (ask user)
5. Verify and log

### Task: Modify Categories

1. **CAREFUL:** Categories may have posts assigned
2. Check usage first
3. Ask user before changes
4. Update via REST API
5. Verify hierarchy maintained
6. Log changes

### Task: Bulk Updates

1. Show user full list of changes
2. Get explicit approval for bulk operation
3. Process one at a time
4. Log each change
5. Report summary at end

---

## Error Handling

### If Script Fails:

1. Check `setup_log_*.txt` for details
2. Verify credentials in config.json
3. Test WordPress REST API endpoint
4. Check network connection
5. Verify WordPress version (5.6+)
6. Check host doesn't block REST API

### If Content Wrong:

1. Log what's wrong
2. Check source content in script
3. Verify API returned success
4. Check live site directly
5. Can manually fix in WordPress admin

### If Credentials Don't Work:

1. Regenerate Application Password
2. Update config.json
3. Test connection with script
4. Verify username is correct

---

## Security Reminders

1. **NEVER commit config.json** - contains credentials
2. **NEVER commit SSH keys** - security risk
3. **NEVER commit passwords** - use environment variables if needed
4. **Log files** - may contain sensitive info, don't commit
5. **Application passwords** - can be revoked anytime in WordPress

---

## Python Environment

**Python Version:** 3.12.10
**Location:** `/c/Users/ziadf/AppData/Local/Programs/Python/Python312/python.exe`
**Dependencies:** requests (installed)

**To run script:**
```bash
/c/Users/ziadf/AppData/Local/Programs/Python/Python312/python.exe menwellbeing_setup.py
```

---

## Quick Reference Commands

### Run Setup Script:
```bash
/c/Users/ziadf/AppData/Local/Programs/Python/Python312/python.exe menwellbeing_setup.py
```

### Install Dependencies:
```bash
/c/Users/ziadf/AppData/Local/Programs/Python/Python312/python.exe -m pip install requests
```

### Check WordPress API:
```bash
curl https://menwellbeing.com/wp-json/wp/v2/
```

---

## Important URLs

**WordPress Admin:**
https://menwellbeing.com/wp-admin/

**Edit Categories:**
https://menwellbeing.com/wp-admin/edit-tags.php?taxonomy=category

**Edit Pages:**
https://menwellbeing.com/wp-admin/edit.php?post_type=page

**Menus:**
https://menwellbeing.com/wp-admin/nav-menus.php

**REST API:**
https://menwellbeing.com/wp-json/wp/v2/

---

## Communication with User

### Always Ask Before:
- Overwriting existing content
- Deleting anything
- Making bulk changes
- Modifying live site
- Changing site structure

### Always Show:
- What currently exists
- What will change
- Why the change is needed
- Expected outcome

### Always Log:
- What was changed
- When it was changed
- Why it was changed
- Result (success/failure)

---

## Troubleshooting Checklist

Before asking user for help, check:

- [ ] Read this guidelines file
- [ ] Checked if content exists
- [ ] Verified credentials are correct
- [ ] Reviewed recent log files
- [ ] Tested WordPress API connection
- [ ] Checked script for errors
- [ ] Verified Python environment works
- [ ] Looked for similar issues in logs

---

## Version History

**v1.0 - November 2, 2025**
- Initial setup completed
- 10 categories created
- 4 pages created
- Python automation script created
- Email: ziad@menwellbeing.com
- Rule added: Never override without asking

---

## Notes & Reminders

1. **User is the owner** - Always get approval for significant changes
2. **Content is valuable** - Never destroy without backup
3. **Site is live** - Changes affect real visitors
4. **Logs are important** - Keep detailed records
5. **Security matters** - Protect credentials
6. **Communication is key** - Ask when uncertain

---

## AI Content Automation Strategy (AGREED DECISIONS)

**Documented:** November 2, 2025
**Status:** Active Development

### Core Principles

1. **Quality First** - No compromise on content quality
2. **Full Automation** - Link all APIs together from day one
3. **Claude-Powered** - Use Claude exclusively for content generation (Max plan bandwidth available)
4. **Publishing Cadence** - Generate 2 articles/day, review, publish at optimal times
5. **Content Mix** - 60% First Timer Tier 1, 40% other topics (test market)

### Affiliate Link Strategy

**Automation Level:** FULL AUTO
- Amazon Product Advertising API integration
- 5-star products only (verified ratings)
- Auto-insert affiliate links during content generation
- Multiple revenue streams per article (Amazon + Udemy + BetterHelp)

### Content Generation Pipeline

```
CSV Topic → Claude AI → Full Article (2000-3000 words) →
Affiliate API (find 5-star products) → Auto-insert links →
WordPress Gutenberg Format → Publish → Update CSV
```

### Publishing Schedule

- **Frequency:** 2 articles per day
- **Best Practice Times:**
  - Morning: 9 AM EST (breakfast reading)
  - Evening: 7 PM EST (after-work browsing)
- **Review Process:** Manual review before first publish, then trust system

### API Integrations Required

1. **Claude API** - Content generation (already available via CLI)
2. **Amazon Product Advertising API** - Product search, ratings, affiliate links
3. **Udemy Affiliate API** - Course recommendations
4. **WordPress REST API** - Publishing (already configured)
5. **BetterHelp Affiliate** - Manual link insertion (no API available)

### Phase 1: Proof of Concept (TODAY)

1. Generate first article from Tier 1 First Timer topics
2. Fine-tune with user until satisfied
3. Generate 4 more articles (total 5)
4. Publish all 5 with screenshots
5. Submit screenshots to Udemy for affiliate approval

### File Structure for Automation

```
C:\dev\MenWellBeing\
├── automation/                    # Automation scripts (IN PROGRESS)
│   ├── wordpress_publisher.py     # Publish to WordPress (CREATED)
│   ├── publish_article_1.py      # Article 1 publisher (CREATED)
│   └── config/                   # Config directory
├── articles/                      # Generated articles (NEW)
│   └── article-1-christmas-gifts-divorced-dad.md  # Article 1 (READY)
├── content_*.csv                  # Content strategy CSVs
├── PROJECT_GUIDELINES.md          # This file (UPDATED)
├── CHANGELOG.md                   # Daily progress tracking (NEW)
├── config.json                    # WordPress credentials (DO NOT COMMIT)
└── menwellbeing_setup.py         # Original WordPress setup script
```

### Content Quality Standards (UPDATED Nov 2, 2025)

- **Word Count:** 1,500-2,000 words (data-driven optimal length for SEO)
- **Product Links:** 15-25 per article (Amazon only for first batch)
- **Product Ratings:** 4.5+ stars minimum, 1,000+ reviews preferred
- **Your KDP Products:** Featured in relevant articles (Divorce Journal, Coloring Book)
- **SEO:** Target keywords from CSV, proper heading structure, internal linking
- **Tone:** Direct, honest, no BS (per brand guidelines)
- **Images:** Amazon product images (manual upload initially) or stock photos
- **Affiliate Tag:** menwellbeing-20 (all links use this tag)

### Success Metrics

- **Article Quality:** User satisfaction with first 5 articles
- **Affiliate Integration:** All links working, 5-star products only
- **Publishing Success:** All 5 articles live on WordPress
- **Udemy Approval:** Screenshots submitted, awaiting approval

---

## Next Steps (Future Development)

- ✅ AI content automation system (IN PROGRESS)
- Image generation/upload automation
- Advanced SEO optimization
- A/B testing different article structures
- Performance analytics integration
- Email list integration for lead magnets

---

**END OF GUIDELINES - Remember to read this file at start of each session!**
