# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. The same item is handed from search to outfit

In 5 of 5 tries on a query that matches a listing, the id of the item in
`session["selected_item"]` is the same as the id of the item passed into
`suggest_outfit`.

**Why this target:** Moving the item between tools is plain code with no model involved, so nothing random can change it. If it fails once, that is a bug in how I used the session, so I set 5 of 5.


---

## 4. The fit card has the right shape

In 4 of 5 tries, the fit card is 2 to 4 sentences and mentions the item name, the price and the platform.

**Why this target:** A model writes the caption, so the words change every run and I can't test exact text. I test things that must always be true. I picked 4 of 5 because a model sometimes skips a detail.


---

## 5. Size filtering returns the right sizes

Across 5 searches using sizes M, L, S, XL and W30, in at least 4 of them every result has a size that matches the requested size under the whole-token rule in my README. One Size listings also count as a match.

**Why this target:** My size data is messy (S/M, W30 L30, XL (oversized)), so size matching is the part of search most likely to go wrong. I picked 4 of 5 because size L also matches W30 L30, and I expect that edge case to cause a miss.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
