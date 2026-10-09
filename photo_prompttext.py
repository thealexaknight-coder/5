#!/usr/bin/env python3
"""
Daily photo challenge: picks today's prompt from prompts.txt and sends it
to your phone through the free ntfy app.

Preview only (nothing sent):   python photo_prompt.py
Send for real:                 python photo_prompt.py --send

Setting (environment variable):
  NTFY_TOPIC   your private ntfy topic name (see README steps)
"""
import os
import random
import sys
import urllib.request
from datetime import date

PROMPTS_FILE = "prompts.txt"


def todays_prompt():
    with open(PROMPTS_FILE, encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
    # Shuffle once with a fixed seed so the order feels random but is the same
    # every run, then walk through it one per day. No saved state needed.
    random.Random(2026).shuffle(prompts)
    return prompts[date.today().toordinal() % len(prompts)]


def send(topic, prompt):
    body = (
        f"Find and photograph: {prompt}\n\n"
        "Tip: shoot it standing up (vertical) for Pinterest."
    ).encode("utf-8")
    req = urllib.request.Request(
        f"https://ntfy.sh/{topic}",
        data=body,
        method="POST",
        headers={"Title": "Todays photo challenge", "Tags": "camera"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status


def main():
    prompt = todays_prompt()
    print("Today's prompt:", prompt)

    if "--send" not in sys.argv:
        print("Preview only. Add --send to send it to your phone.")
        return

    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        sys.exit("Missing NTFY_TOPIC. See README steps.")
    status = send(topic, prompt)
    print("Sent. ntfy replied:", status)


if __name__ == "__main__":
    main()
