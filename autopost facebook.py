#!/usr/bin/env python3
"""
Daily Amazon deal poster for a Facebook Page.

What it does each run:
  1. Reads deals.csv and picks the first deal not yet posted.
  2. Builds your Amazon affiliate link (your tag added to the product link).
  3. Writes a post (with the required earnings disclosure).
  4. Publishes it to your Facebook Page and marks the deal as posted.

Run safely first (nothing is posted):   python autopost.py
Run for real:                           python autopost.py --post

Settings come from environment variables (see README.md):
  AMAZON_TAG       your Associates tracking ID, e.g. mystore-20
  FB_PAGE_ID       your Facebook Page ID
  FB_PAGE_TOKEN    your Page access token
"""
import csv
import json
import os
import random
import sys
import urllib.parse
import urllib.request
from datetime import date

CSV_FILE = "deals.csv"
GRAPH_VERSION = "v21.0"

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

# No prices on purpose: Amazon doesn't allow showing stale prices.
TEMPLATES = [
    "🔥 Today's pick: {title}\n{hook}\nCheck the current price here 👉 {link}",
    "💥 Deal alert! {title}\n{hook}\nSee today's price 👉 {link}",
    "👀 Found this one for you: {title}\n{hook}\nTake a look 👉 {link}",
    "⚡ Worth a look today: {title}\n{hook}\nGrab it before it's gone 👉 {link}",
]


def build_link(asin, tag):
    return f"https://www.amazon.com/dp/{asin.strip()}?tag={tag}"


def build_caption(row, link):
    hook = (row.get("hook") or "").strip()
    text = random.choice(TEMPLATES).format(
        title=row["title"].strip(), hook=hook, link=link
    )
    # Tidy up if hook was empty
    text = "\n".join(line for line in text.split("\n") if line.strip())
    return f"{text}\n\n{DISCLOSURE}"


def post_to_facebook(page_id, token, message, link):
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{page_id}/feed"
    data = urllib.parse.urlencode(
        {"message": message, "link": link, "access_token": token}
    ).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    live = "--post" in sys.argv
    tag = os.environ.get("AMAZON_TAG")
    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_PAGE_TOKEN")

    if not tag:
        sys.exit("Missing AMAZON_TAG. See README.md step 3.")
    if live and not (page_id and token):
        sys.exit("Missing FB_PAGE_ID or FB_PAGE_TOKEN. See README.md step 2.")

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    next_row = next((r for r in rows if not (r.get("posted") or "").strip()), None)
    if next_row is None:
        sys.exit("No unposted deals left in deals.csv. Add more rows!")

    link = build_link(next_row["asin"], tag)
    caption = build_caption(next_row, link)

    print("----- POST PREVIEW -----")
    print(caption)
    print("------------------------")

    if not live:
        print("Dry run only. Nothing was posted. Add --post to publish.")
        return

    try:
        result = post_to_facebook(page_id, token, caption, link)
    except urllib.error.HTTPError as e:
        sys.exit(f"Facebook rejected the post: {e.read().decode()}")

    print("Posted! Facebook post id:", result.get("id"))
    next_row["posted"] = date.today().isoformat()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
