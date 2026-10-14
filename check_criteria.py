"""
Checks for criteria 3 and 5. Makes no model calls.

    python check_criteria.py
"""

import re

import agent
import tools
from utils.data_loader import get_example_wardrobe

TRIES = 5


def check_criterion_3():
    print("Criterion 3: selected_item id matches the id passed to suggest_outfit\n")
    query = "denim jacket under $50"
    real_suggest, real_card = agent.suggest_outfit, agent.create_fit_card
    passes = 0

    try:
        for i in range(1, TRIES + 1):
            seen = []

            def fake_suggest(new_item, wardrobe):
                seen.append(new_item["id"])
                return "stub outfit"

            agent.suggest_outfit = fake_suggest
            agent.create_fit_card = lambda outfit, new_item: "stub card"

            session = agent.run_agent(query, get_example_wardrobe())
            selected = (session.get("selected_item") or {}).get("id")
            passed = len(seen) == 1 and seen[0] == selected
            passes += passed
            print(f"  try {i}: {'PASS' if passed else 'FAIL'}  "
                  f"passed to suggest_outfit={seen[0] if seen else None}  selected_item={selected}")
    finally:
        agent.suggest_outfit, agent.create_fit_card = real_suggest, real_card

    print(f"\n  Criterion 3: {passes} of {TRIES} PASS\n")


def _size_matches(listing_size, wanted):
    low = (listing_size or "").lower()
    if low.startswith("one size"):
        return True
    tokens = [t for t in re.split(r"[\s/()\[\]]+", low) if t]
    return wanted.lower() in tokens


def check_criterion_5():
    print("Criterion 5: every result's size matches the requested size\n")
    pairs = [("tee", "M"), ("jacket", "L"), ("top", "S"), ("sweatshirt", "XL"), ("jeans", "W30")]
    passes = 0

    for query, size in pairs:
        results = tools.search_listings(query, size=size)
        print(f"  search '{query}', size {size}:")
        if not results:
            print("    0 results")
        for r in results:
            print(f"    {r.get('size')}")
        passed = bool(results) and all(_size_matches(r.get("size"), size) for r in results)
        passes += passed
        print(f"    {'PASS' if passed else 'FAIL'}")

    print(f"\n  Criterion 5: {passes} of {len(pairs)} PASS")


if __name__ == "__main__":
    check_criterion_3()
    check_criterion_5()
