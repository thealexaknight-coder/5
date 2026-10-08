# Daily Amazon Deal Poster

Posts one Amazon deal per day to your Facebook Page, with your affiliate link
and the required earnings disclosure. It runs for free on GitHub, so your
computer does not need to be on.

## What's in this folder

| File | What it does |
|---|---|
| `deals.csv` | Your list of products. The script posts the next row that has no date in `posted`. |
| `autopost.py` | Builds your link, writes the post, publishes it, marks the row as posted. |
| `.github/workflows/daily.yml` | The daily timer (runs at 10am Central). |

## Setup (one time)

### Step 1: Put the project on GitHub
1. Make a free account at github.com.
2. Create a **private** repository and upload these files (keep the `.github` folder).

### Step 2: Get your Facebook Page ID and token
1. Go to developers.facebook.com and create an app (type: Business).
2. Add the Pages permissions `pages_manage_posts` and `pages_read_engagement`.
3. In Graph API Explorer, generate a **Page access token** for your Page.
4. Exchange it for a long-lived token (Meta's docs: "Long-Lived Tokens"). Page tokens
   made from a long-lived user token do not expire.
5. Your Page ID is on your Page under About > Page transparency.

Facebook's screens change often. If a step looks different, search for
"get Facebook Page access token" or ask me and I will walk you through it.

### Step 3: Add your secrets to GitHub
In your repo: Settings > Secrets and variables > Actions > New repository secret.
Add these three:

- `AMAZON_TAG`: your Associates tracking ID, like `mystore-20`
- `FB_PAGE_ID`: your Page ID
- `FB_PAGE_TOKEN`: your Page access token

Never put these in the files themselves.

### Step 4: Add your deals
Open `deals.csv` and replace the examples. One row per deal:

- `asin`: the 10-character code in the Amazon link (`amazon.com/dp/B0XXXXXXXX`)
- `title`: product name
- `hook`: one short line on why it's a good deal
- `posted`: leave empty. The script fills in the date after posting.

Do not put prices in the title or hook; prices change and Amazon restricts showing old ones.

### Step 5: Test it
On your computer (needs Python), run:

    AMAZON_TAG=yourtag-20 python autopost.py

This prints a preview and posts nothing. When it looks right, in GitHub go to
Actions > Daily deal post > Run workflow to send a real test post.

## Day to day
Just keep adding rows to `deals.csv`. When it runs out, the run fails with
"No unposted deals left" and GitHub emails you.

## Rules to follow
- Keep the disclosure line in every post (the script adds it).
- Your Amazon Associates account needs real sales within 180 days or it closes.
- Facebook may limit Pages that post only links. Mixing in regular posts helps.
