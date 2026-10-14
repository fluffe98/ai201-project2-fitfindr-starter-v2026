# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

You type what you're hunting for in plain language, like "vintage graphic tee under $30, size M". FitFindr pulls the price and size out of the sentence and searches a set of secondhand listings from Depop, thredUp and Poshmark for the best match. It then suggests one or two outfits that pair the find with clothes already in your wardrobe, and writes a short social media caption (a "fit card") about it. If nothing matches, it tells you what to change, such as raising the budget, dropping the size or using broader words, instead of making something up.

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the listings data for items matching a description, with an optional size filter and an optional price ceiling.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of listing dicts, best match first, at most `config.SEARCH_RESULT_LIMIT` long. Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), `platform`.
  - Price rule: inclusive, so a listing passes when `price <= max_price`.
  - Size rule: the listing size is lowercased and split on spaces, slashes and brackets into tokens. The requested size (lowercased) must equal one whole token. So "M" matches "S/M" and "M/L" but not "XL", and "L" does not match "XL". Listings with size "One Size", "One Size (adjustable)" or "One Size / Oversized" always pass the size filter. Known side effect: "L" also matches "W30 L30", because L is a whole token there.
  - Scoring rule: each listing is scored by how many description keywords appear in its title, description, style_tags, category, colors and brand (brand may be None). A score of zero is dropped.
- **When it has nothing:** Returns an empty list `[]`. Never `None`, never an exception.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits that use the found item together with pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict, a listing), `wardrobe` (dict with an `"items"` key holding a list)
- **Returns:** A non-empty string of outfit suggestions that names wardrobe pieces the user owns.
- **When it has nothing:** When `wardrobe["items"]` is an empty list, it returns general styling advice for the item as a non-empty string. It checks `wardrobe["items"]`, not the wardrobe dict itself, because the dict is never empty.

### `create_fit_card`

- **What it does:** Writes a short social media caption about the find.
- **Inputs:** `outfit` (str), `new_item` (dict, a listing)
- **Returns:** A string of two to four sentences that mentions the item, its price and its platform once each, and sounds like a real post.
- **When it has nothing:** If `outfit` is empty or only whitespace, it returns a descriptive message string saying there is no outfit to write about. Not `""` and not an exception.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that tells the user what to change (raise the budget, drop the size, or use broader words), leave `session["fit_card"]` as `None`, and return the session without calling `suggest_outfit`. Otherwise, take the first result as `session["selected_item"]`, call `suggest_outfit`, then call `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** regex. A price comes from "under $N" or "$N", a size comes from "size X", and the leftover words become the description.

**What moves through the session:** `query`, `parsed`, `search_results`, `selected_item`, `outfit_suggestion`, `fit_card`, with `error` set only when the run ends early.

---

## Sample Run

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Y2K Streetwear**
Pair the Y2K Baby Tee — Butterfly Print with your Baggy straight-leg jeans, dark wash, and layer the Black cropped zip hoodie on top. Finish the look with your Chunky white sneakers and Black crossbody bag for an effortless throwback vibe.

**Outfit 2: Soft Contrast**
Style the Y2K Baby Tee — Butterfly Print tucked into your Wide-leg khaki trousers, accented by the Brown leather belt. Throw on the Vintage black denim jacket and ground the outfit with your Black combat boots to mix sweet cottagecore elements with vintage edge.

  Fit card: Found this absolute dream of a butterfly print baby tee while thrifting and I'm honestly obsessed with the Y2K energy. It's listed on Depop right now for just $18 so you can live out all your 2000s streetwear or soft grunge fantasies without breaking the bank. Grab it before I change my mind and keep it for myself!

0 model calls this session, 2 served from cache
```

Note: this run printed "0 model calls, 2 served from cache" because I had already run the same query once through `python agent.py`, so the two model answers came from the cache. The text is what the model returned the first time.

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual Streetwear**
Pair the vintage Levi's with the **White ribbed tank top** tucked in, layered under the **Vintage black denim jacket**. Finish the look with the **Chunky white sneakers**, the **Brown leather belt**, and the **Black crossbody bag** for an effortless, everyday vibe.

**Outfit 2: Cozy & Classic**
Style the medium wash jeans with the **Oversized grey crewneck sweatshirt** for a relaxed silhouette. Add the **Brown leather belt** for definition, and ground the outfit with the **Black combat boots** to balance the vintage denim with a touch of grunge.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Finally found the holy grail of denim and they're giving major 90s off-duty model vibes when paired with fresh white sneakers. These vintage Levi's 501 jeans in the dreamiest medium wash are up on my Depop right now for just $38.00 before they sell out. Grab them while you can!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Help writing the Tool Inventory spec for
  search_listings, especially how to match sizes.
- *What came back:* Claude suggested matching the requested size against
  whole words in the listing size, so "M" matches "S/M" but "L" does not
  match "XL". I printed every size in the data to test that. The idea held
  up, but Claude pointed out two gaps: "One Size" listings, and "L"
  matching "W30 L30".
- *What I changed:* I added a rule that One Size listings always pass the
  size filter. I kept the "L matches W30 L30" side effect and wrote it
  into the spec as a known issue to look at in unit 4.

**Moment 2**

- *What I asked for:* I gave Claude Code my README spec and asked it to
  build search_listings, suggest_outfit, create_fit_card and run_agent to
  match it.
- *What came back:* Working tools and loop. The happy path found the Y2K
  baby tee and gave an outfit and a caption. The ballgown query stopped
  with a message and fit_card stayed None.
- *What I changed:* Nothing in the code. I ran both paths
  myself and checked the output against my spec.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Same item handed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card shape | 4 of 5 | PASS | PASS | FAIL | PASS | PASS | MET (4/5) |
| 5. Size filtering (5 searches: M, L, S, XL, W30) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output**, pasted as text, naming the file and function that produced it:

Criterion 1, one try (Try 1), from `results/run_2026-10-13_1956_before.md`, produced by `run_eval.py::main`:

```
**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
**Outfit 1: Y2K Streetwear**
Pair the Y2K Baby Tee — Butterfly Print with the baggy straight-leg jeans, dark wash. Layer the black cropped zip hoodie on top, and finish with the chunky white sneakers and black crossbody bag for an effortless, nostalgic look.

**Outfit 2: Casual Contrast**
Combine the Y2K Baby Tee — Butterfly Print with the wide-leg khaki trousers. Cinch the waist using the brown leather belt, and style with the vintage black denim jacket and black combat boots to balance the tee's feminine pink and purple graphic with a touch of edge.
```

Fit card:

```
Found this pink and purple butterfly baby tee thrifting and honestly didn't want to part with it, but she needs a new home. She's giving total early 2000s mall rat energy, whether you style her sweet with low-rise denim or edgy with some combat boots. Grab her on my Depop right now for just $18 before I change my mind!
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: **Outfit 1: Y2K Streetwear** Pair the Y2K Baby Tee — Butterfly Print with the baggy straight-leg jeans, dark w…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Found this pink and purple butterfly baby tee thrifting and honestly didn't want to part with it, but she need…
```
```

Criterion 2, one try (Try 1), from `results/run_2026-10-13_1956_before.md`, produced by `run_eval.py::main`:

```
**Try 1**

- stopped early: yes — No listings matched. Try raising your budget, dropping the size, or using broader words.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] stop
      →    branch: search returned [], skipping suggest_outfit and create_fit_card
```
```

Criterion 4, one try (Try 3, the FAIL), from `results/run_2026-10-13_1956_before.md`, produced by `run_eval.py::main`:

```
**Try 3**

- stopped early: no
- selected_item: Corduroy Wide-Leg Pants — Rust ($32.0, depop)
- search_results: 2

Outfit suggestion:

```
**Outfit 1: Cozy 70s Earth Tones**
Pair the corduroy pants with the white ribbed tank top layered under the oversized grey crewneck sweatshirt. Add the brown leather belt and finish the look with the chunky white sneakers for a relaxed, vintage-inspired everyday fit.

**Outfit 2: Retro Edge**
Style the rust wide-leg pants with the white ribbed tank top and top it off with the vintage black denim jacket. Cinch the waist with the brown leather belt and step into the black combat boots to lean into the vintage cottagecore meets grunge aesthetic.
```

Fit card:

```
Nothing beats finding the ultimate cozy 70s earth tone pants while thrifting, and this rust wide-leg pair is seriously too good to keep. Grab them now on Depop for just $32.0 before I change my mind and keep them for myself!
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 2 items: Corduroy Wide-Leg Pants — Rust, Low-Rise Cargo Pants — Khaki
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: **Outfit 1: Cozy 70s Earth Tones** Pair the corduroy pants with the white ribbed tank top layered under the ov…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Nothing beats finding the ultimate cozy 70s earth tone pants while thrifting, and this rust wide-leg pair is s…
```
```

Criterion 3, all five tries, from `results/check_criteria_before.txt`, produced by `check_criteria.py` (the trace lines between tries are left out):

```
Criterion 3: selected_item id matches the id passed to suggest_outfit
  try 1: PASS  passed to suggest_outfit=lst_007  selected_item=lst_007
  try 2: PASS  passed to suggest_outfit=lst_007  selected_item=lst_007
  try 3: PASS  passed to suggest_outfit=lst_007  selected_item=lst_007
  try 4: PASS  passed to suggest_outfit=lst_007  selected_item=lst_007
  try 5: PASS  passed to suggest_outfit=lst_007  selected_item=lst_007
  Criterion 3: 5 of 5 PASS
```

Criterion 5, from `results/check_criteria_before.txt`, produced by `check_criteria.py`:

```
Criterion 5: every result's size matches the requested size

  search 'tee', size M:
    S/M
    S/M
    PASS
  search 'jacket', size L:
    M/L
    PASS
  search 'top', size S:
    S/M
    One Size / Oversized
    S/M
    S/M
    PASS
  search 'sweatshirt', size XL:
    XL (fits oversized)
    PASS
  search 'jeans', size W30:
    W30 L30
    PASS

  Criterion 5: 5 of 5 PASS
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes | 4 of 5 | MET (5/5) | All five tries of "vintage graphic tee under $30" ran all three tools and ended with a fit card and no error. |
| 2 | Impossible query stops early | 5 of 5 | MET (5/5) | All five tries of "designer ballgown size XXS under $5" stopped after the search with the "raise your budget" message, and the trace has no suggest_outfit or create_fit_card step. |
| 3 | Same item handed to suggest_outfit | 5 of 5 | MET (5/5) | In all five tries the id passed into suggest_outfit (lst_007) equalled session["selected_item"]["id"]. This used stubbed model tools ("stub outfit", "stub card"), so it tests only the item handoff and not the model output. |
| 4 | Fit card shape | 4 of 5 | MET (4/5) | I checked each card for 2 to 4 sentences plus the item name, the price and the platform. Try 3 was scored FAIL because the card says "earth tone pants" and "rust wide-leg pair" but never "corduroy", so the other four passed and it met the target at exactly 4 of 5. |
| 5 | Size filtering | 4 of 5 | MET (5/5) | All five searches (M, L, S, XL, W30) returned at least one result and every result's size matched. It could not fail on "L matches W30 L30", because its wording counts that as a match. |

The reasons written under criteria 1 and 2 in criteria.md were written after the test ran, not before.

**Diagnoses**

No criterion was missed, so there is no miss to diagnose. The targets were fairly safe. If I did this again I would tighten criterion 5 to require that a result matches the size and the search keywords, not only the size.

One weak spot showed up in criterion 4. In Try 3 the fit card dropped the item name, so the prompt in `tools.py::create_fit_card` asks for the item to be mentioned but doesn't force it. The same cards also print the price in different ways ("$32.0", "$32.00" and "$32"), because the prompt passes the raw price number to the model and doesn't format it.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: **Outfit 1: Y2K Streetwear** Pair the Y2K Baby Tee — Butterfly Print with your Baggy straight-leg jeans, dark …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Found this absolute dream of a butterfly print baby tee while thrifting and I'm honestly obsessed with the Y2K…
```

**Empty search**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[2] stop
      →    branch: search returned [], skipping suggest_outfit and create_fit_card
```

**On the MCP move:** I moved search_listings behind an MCP server in mcp_server.py, and run_agent() now calls it through mcp_client.call_tool instead of calling the function directly. The result has the same shape as before (a list of listing dicts, and [] when nothing matches), and both example queries behaved the same as before the move.

**Bad API key:** with a wrong key, run_agent() stops cleanly with fit_card as None and this message in session["error"]: "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com."


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
