# Content CSV Files - Usage Guide

**For: Ziad & Future Claude Sessions**

## Overview

We have 4 CSV files for managing MenWellbeing.com content strategy:

1. `content_what_i_want.csv` - 35 product/gear topics (My Ride, My Gear, My Space, My Body)
2. `content_what_i_need.csv` - 40 support/resource topics (Mental Health, Relationships, Connection, Career)
3. `content_first_timer.csv` - 30 "First Time X" blended topics (Want + Need combined)
4. `content_master_dashboard.csv` - Overview and progress tracking

**Total: 100+ content topics ready to produce**

---

## How to Use These Files

### Opening in Excel/Google Sheets:

**Excel:**
1. Open Excel
2. File → Open → Select CSV file
3. Data will auto-populate with commas as delimiters
4. Save as .xlsx to preserve formatting

**Google Sheets:**
1. Go to sheets.google.com
2. File → Import → Upload → Select CSV
3. Import location: "New spreadsheet" or "New sheet in current spreadsheet"
4. Separator type: "Comma"
5. Click "Import data"

---

## Column Explanations

### All Content Files Have:

**Topic** - The content title/subject
**Category** - Subcategory (My Ride, Mental Health, etc.)
**Pain Point** - Core problems this addresses (pipe | separated)
**Search Volume** - Very High / High / Medium / Low (based on estimated monthly searches)
**Audience** - Target demographic (age range, situation)
**Status** - Track progress: Not Started | In Progress | Published | Used
**Interest Rating (1-10)** - YOUR rating of interest in creating this content
**Create Similar?** - Mark Yes/No if you want more topics like this
**Priority (1-5)** - Urgency: 5 = Do First, 1 = Later
**Affiliate Potential** - High / Medium / Low (revenue opportunity)
**Target Keywords** - SEO keywords to target
**Est. Traffic** - Estimated monthly search volume
**Notes** - Additional context, research, ideas

### First Timer File Also Has:

**Blend Type** - Want + Need (shows it combines both pillars)
**Want Elements** - Product/gear aspects of content
**Need Elements** - Support/resource aspects of content

---

## Workflow for Content Creation

### Step 1: Choose Content

Open the CSVs and sort/filter by:
- **Priority** (5 = highest)
- **Search Volume** (Very High first)
- **Interest Rating** (what YOU want to write)
- **Affiliate Potential** (if monetization focus)

**Recommended start:** First Timer Tier 1 topics (5 topics in `content_first_timer.csv`)

### Step 2: Update Status

When you start working on a topic:
1. Change **Status** to "In Progress"
2. Add **Interest Rating** (1-10)
3. Set **Priority** if not already set
4. Mark **Create Similar?** if you want more like this

### Step 3: Track Completion

When published:
1. Change **Status** to "Published"
2. Add URL in **Notes** field
3. Add actual traffic data in **Notes** after 30 days
4. Mark **Create Similar?** if it performed well

### Step 4: Scale

If a topic performs well:
1. Sort by **Create Similar? = Yes**
2. Look at **Category** for related topics
3. Check **Master Dashboard** for category performance
4. Create 3-5 more topics in that category

---

## For Claude Sessions: What to Do

**When user asks to work on content:**

1. **Read PROJECT_GUIDELINES.md first** (critical context)

2. **Open relevant CSV:**
   - Product/gear content → `content_what_i_want.csv`
   - Support/resources → `content_what_i_need.csv`
   - "First Time X" blend → `content_first_timer.csv`
   - Overview/stats → `content_master_dashboard.csv`

3. **Filter/sort by:**
   - Status = "Not Started" (to find available topics)
   - Priority = 5 or 4 (urgent topics first)
   - Search Volume = "Very High" or "High" (traffic opportunity)
   - Interest Rating = 8-10 (if user has rated)

4. **For each topic, create:**
   - Comprehensive article (2000-3000 words)
   - Product recommendations (for Want topics)
   - Resource links (for Need topics)
   - Personal stories (for First Timer topics)
   - SEO-optimized with Target Keywords
   - Internal links to related topics
   - Affiliate links where appropriate

5. **Update the CSV:**
   - Change Status to "Published"
   - Add publish date and URL in Notes
   - Mark any insights about performance

6. **Ask user:**
   - "This topic performed well - create 5 similar?"
   - "Interest rating? Mark for similar content?"
   - "Which category to focus on next?"

---

## Content Strategy Notes

### High-Priority Content (Start Here):

**From `content_first_timer.csv` - Tier 1:**
1. First Time Divorced (150K searches)
2. First Time Dating After Long Relationship (125K)
3. First Time Living Alone (100K)
4. First Time Motorcycle Rider (95K)
5. First Time Father Over 40 (85K)

These blend Want + Need perfectly and have highest pain points + search volume.

### High-Traffic Opportunities:

**From `content_what_i_want.csv`:**
1. Fitness After 40 (90K) - My Body
2. Home Gym Setup (85K) - My Gear
3. First Time Camping (75K) - My Gear
4. Home Office Remote Work (70K) - My Space
5. Testosterone TRT (70K) - My Body

### High-Value (Low Traffic but Critical):

**From `content_what_i_need.csv`:**
1. Therapy Guide for Men (95K) - normalize seeking help
2. First Time Divorced Guide (120K) - life transition support
3. Male Loneliness Epidemic (65K) - cultural issue
4. Burnout Recovery (60K) - work-life balance
5. Suicide Prevention (50K) - crisis support

---

## Filtering Examples

### "Show me topics I can write today that will get traffic"
Filter by:
- Status = "Not Started"
- Search Volume = "Very High" or "High"
- Sort by: Est. Traffic (descending)

### "Show me topics with affiliate opportunities"
Filter by:
- Affiliate Potential = "High"
- Status = "Not Started"
- Sort by: Est. Traffic (descending)

### "What should I write next based on research?"
Look at `content_master_dashboard.csv`:
- First Timer Tier 1 (start here)
- What I Want - My Gear top 3
- What I Need - Mental Health top 3

### "Show me quick wins"
Filter by:
- Search Volume = "High" or "Very High"
- Affiliate Potential = "High"
- Priority = 5
Result: Topics that are high-traffic + high-revenue + urgent

---

## Adding New Topics

When you find new content ideas:

1. Open appropriate CSV
2. Add new row at bottom
3. Fill in all columns:
   - Topic (clear, searchable title)
   - Category (match existing categories)
   - Pain Point (what problem does this solve?)
   - Search Volume (research on Google Trends / Ahrefs / SEMrush)
   - Audience (who is this for?)
   - Status (start with "Not Started")
   - Leave Interest Rating blank (user will fill)
   - Affiliate Potential (are there products to recommend?)
   - Target Keywords (SEO research)
   - Est. Traffic (monthly search volume)
   - Notes (why add this? research links?)

4. Update `content_master_dashboard.csv` counts

---

## Tracking Performance

After publishing content, add to **Notes** column:

```
Published: 2025-11-15
URL: https://menwellbeing.com/first-time-divorced/
30-day traffic: 2,500 visitors
90-day traffic: 8,200 visitors
Affiliate clicks: 150
Affiliate revenue: $450
Top keyword: "first time divorced at 45"
Engagement: 4:30 avg time on page
Performance: EXCELLENT - create 5 similar topics
```

This helps decide what content to scale.

---

## For Future Claude: Quick Reference

**User says: "Let's create content"**
→ Open CSVs, filter Status="Not Started", sort by Priority/Traffic, show top 5 options

**User says: "Write about [topic]"**
→ Search CSVs for topic, get pain points/keywords/audience, create comprehensive content

**User says: "This topic did well"**
→ Find similar topics in same Category, suggest 3-5 to create next

**User says: "What should I focus on?"**
→ Open `content_master_dashboard.csv`, recommend Tier 1 First Timer topics

**User says: "Add new topics about [subject]"**
→ Research pain points/keywords, add to appropriate CSV with all columns filled

**User says: "Show me affiliate opportunities"**
→ Filter by Affiliate Potential = "High", sort by Search Volume

**User says: "Quick wins?"**
→ Filter: High Volume + High Affiliate + Priority 5

---

## Important Notes

1. **CSVs are source of truth** - always update them
2. **Status tracking is critical** - prevents duplicate work
3. **Interest ratings guide future content** - ask user to rate after creating
4. **Create Similar flag = scaling signal** - user wants more of this type
5. **Notes field = performance data** - track what works
6. **Priority changes** - topics become urgent based on trends/news
7. **Search volume estimates** - recheck every 6 months for trends

---

## Monthly Review Process

**For Claude to run with user monthly:**

1. Open `content_master_dashboard.csv`
2. Update counts: Published, In Progress, Not Started
3. Calculate Avg Interest Rating per category
4. Review top performers (from Notes field performance data)
5. Identify categories to scale (high performance + user interest)
6. Update Priority ratings based on:
   - Current trends
   - Performance data
   - User interest ratings
   - Seasonal opportunities
7. Suggest next 10 topics to create
8. Archive completed topics to separate file if desired

---

## File Locations

All CSVs are in:
```
D:\Work\2025\MenWellBeing\
```

And synced to GitHub:
```
https://github.com/zixofranic/MenWellBeing.git
```

So they're accessible from any computer where you pull the repo.

---

## Questions?

If you're a future Claude session and unclear:
1. Read PROJECT_GUIDELINES.md
2. Read this file (CSV_USAGE_GUIDE.md)
3. Open the CSVs in Google Sheets
4. Ask user for clarification on their goals

---

**This system gives you 100+ researched topics ready to execute. Just filter, choose, create, track, scale.**
