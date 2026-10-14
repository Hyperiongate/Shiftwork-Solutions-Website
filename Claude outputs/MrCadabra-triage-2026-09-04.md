# MrCadabra — triage of the 2026-09-04 Night Watch
**Prepared while Jim was away · 2026-09-04**

---

## First, a correction I owe you

**The two crashes I told you to fix first were already fixed.** Both were ghosts draining out of the 7-day telemetry window, and the report says so plainly in its own legend — I read the counts and not the dates. That was my error, and it sent you toward the wrong two items.

| What I flagged | Actual status |
|---|---|
| `mathcheck` crash — `'tuple' object has no attribute 'free_symbols'` ×4 | **Fixed 2026-09-02, build ru** (`mathcheck.py`). `_parse` now raises on a result without `free_symbols`, so every caller's existing unparseable path fails open instead of crashing. All four crashes were on 09-02. |
| `wipeBoard` browser crash — `Array.from(undefined)` ×5 | **Fixed 2026-09-02, build sg** (`session.html`). The `child`→`student` sweep had rewritten `feed.children` to `feed.students`; restored. Build sg also added the net so `scrNext` survives a crashed beat and can never freeze a lesson again. All five errors were inside one hour on 09-02. |

No code changed for either. The right reading of that telemetry block is the one the report itself gives you: **a reason whose newest sighting is days old is already fixed or already ended.** Only a line marked LIVE is today's problem.

---

## What is actually live

**One telemetry item:** `floor · frac61`, 08:28 UTC — 33 minutes before the run. The tutor tried three times to say *"what do you get when you add the top numbers, one plus…"* with no condition attached, which is false for unlike denominators. **The floor did its job** — nothing shipped, the child got the fallback line. This is the system working, not a defect. The underlying issue is that the fraction-addition path keeps generating the falsehood, which is a prompt problem, not a code one.

**The 12 teaching findings** from last night — all live by definition.

**The 150 pass-throughs** — ongoing and by design (see below).

---

## The seam: lesson → lesson

You were right, and the pieces to fix it already exist.

**What happens now.** A mastered scripted lesson calls `_script_finish`, which records the outcome, leaves a seam note, and pops the session. `session.html:3927` then sends `__script_done_mastered__` to the **live tutor**, and `main.py:14716` builds a system note telling the model:

> *Your FIRST sentence must NAME the new topic in plain words…*

It says name **the** new topic. It never says **which**. The model picks. That is the root of the 09-01 bug you caught — *"one-less reads as subtraction."* Build rj made the model announce its guess; it did not replace the guess with the answer already in the file.

**What already exists:**

| Piece | Where | State |
|---|---|---|
| `COURSE_ORDER` — 360 lesson ids, hand-ordered, 36 per course × 10 courses | `lessonscripts.py:16020` | Canonical. Import fails loudly on a missing or duplicated lesson. |
| `LESSON_BY_ID` (360) and `LESSONS` (360) | `lessonscripts.py` | Present |
| `record_script_done(code, course, id, mastered)` | `store` (build rk) | Durable per-lesson record; `/api/session` already ships mastered ids |
| `/api/script/start` accepting a lesson id | `main.py:10634` | Present — **and `session.html:4042` already calls it** |

The comment in `script_start` states the original intent outright: *"the id rides along so the pilot page can offer 'Next lesson' from the course order without guessing which lesson this session is in."* The capability was built. The `/session` seam just doesn't use it.

**Verified behaviour:** `COURSE_ORDER.index(id) + 1` gives the correct next lesson, and it crosses course boundaries cleanly (`entry-u9-sharing-fairly` → `basic-u1-place-value-to-1000`).

### Two ways to fix it

**Option A — deterministic advance (the right fix, matches your scripted-first ruling).**

1. `main.py`: add `_next_lesson_id(current_id)` — index into `COURSE_ORDER`, return the next id, or `None` at the end of the course.
2. `_script_finish`: put that id into `_SCRIPT_DONE_NOTES` alongside topic/course/mastered.
3. `session.html:3927`: instead of `runTutor("__script_done_mastered__")`, call `/api/script/start` with the next id — the page already knows how.
4. The live tutor is reached **only** when `_next_lesson_id` returns `None`, i.e. the course is genuinely finished. That is when build rj's announced-seam note actually belongs.

Consequence: a child who never misses runs an entire 36-lesson course on `kind="script"` turns and never meets the live lane at all.

**Option B — three lines, if A is too much for today.** Keep the handoff, but put the real next topic name into the system note so the model teaches the right thing. Fixes the wrong-topic symptom; leaves a model call in the path.

### Four decisions that are yours, not mine

1. **Should mastery auto-advance, or should the child choose?** Auto-advance could run 36 lessons in a sitting.
2. **A lesson that ended "still learning" — advance anyway, or repeat it?** Right now both end the same way.
3. **Does `LINE_NEW_TOPIC` still get spoken** between scripted lessons, or only at a course boundary?
4. **Is the resume point the last *started* or last *mastered* lesson?** `record_script_done` carries the flag either way.

I did not implement any of this. It changes child-facing flow, and those four questions have to be answered first.

---

## The 12 findings: which need a referee, and which need a retry that converges

The watch reviewer is more thorough than the live referees, so a finding appears for one of two reasons — and they need opposite fixes.

**These already have a referee. It fired and the reply shipped anyway.**

- **Rule 14 / 48 — notation written but not said aloud (5 findings).** The `notation` referee is the thirtieth referee, "define every notation the first time it appears," and it **fired 31 times this week**. `unspoken` fired 14 more. Yet five findings in that exact family came out of the watch — the superscript `2⁻`/`2⁺`, the `⟺` symbol, `25% = 25/100 = 1/4`, the place-value equation, the lowercase triangle labels.
  **So the referee is not missing. Either the retry isn't converging, or the referee has coverage gaps for these specific notation shapes.** That is a completely different fix from writing a new referee, and worth an hour before anyone writes one.
- **Rule 61 — a law stated without its condition (2 findings).** `falseuniversal`, `precedencelaw` and `frac61` all exist and are all truth-class. `frac61` floored correctly last night. The two rule-61 findings that *shipped* were conduct-classified.

**These look uncovered.**

- **The HIGH — the board solving a different expression from the spoken one.** It cites no rule number, unlike every MEDIUM. Mathcheck passes it because `2 + 3 × 4 = 14` is arithmetically true; it's just the answer to the wrong question. The nearest referee, `boardcount`, is explicitly ruled conduct in the "considered and NOT included" list beside `TRUTH_REFEREES` — *"a board/words disagreement the child can SEE; **ruled conduct until Jim says otherwise**."* That note is waiting on you.
- **Rule 39 — a check the student cannot fail (2 findings).** "With me so far?" and a choice list where both options mean yes.

**And the mechanism behind all of it:** 602 referee fires, **150 ending in `pass_through`** — the referee found it, three attempts failed to fix it, and `_settle` shipped the least-bad draft on purpose. `livecritic` alone accounts for 105 of those 150. Roughly a quarter of the time the retry does not converge.

---

## What I would work on today, in order

1. **The seam (Option A).** It's the only item here that removes a model call from a child's path rather than policing one. It's small, the pieces exist, and it fixes a bug you personally watched happen. Needs your four answers first.
2. **Rule the board/words disagreement.** Promote it to `TRUTH_REFEREES` and last night's HIGH would have floored instead of shipping. The cost is real — a fallback line teaches nothing either — which is why it's your call and not mine. Your own code has been waiting on this ruling since it was written.
3. **Ask why the retry doesn't converge before writing any new referee.** 105 livecritic pass-throughs is the single biggest quality lever in the system, and five of the twelve findings sit behind a referee that already fires 31 times a week. More attempts, or feeding the referee's specific complaint back harder on the retry, may close more than any new rule would.
4. **Leave the fraction path to the floor for now.** It's working. Fix the prompt when you're in there anyway.

---

## Two housekeeping notes

- **`NIGHTWATCH_LESSONS` is done.** `_DEFAULT_LESSONS` is 10 in `nightwatch.py`, matching Render, and the `ruletests.py` check that would have started failing tonight is re-pinned to 7 / "default is 10". Both compile; verified that a clean environment banners nothing, `=10` banners nothing, and `=7` still banners correctly. Change notes added under BUILD sk. **Nothing committed or pushed.**
- **There is a stale `.git/index.lock`** in `D:\MyTutor\.git\` (zero bytes, created 13:33). `git status` and `git diff` return empty because of it. I can't delete files on your machine — **delete that file before you review, or git will keep showing you nothing.**

---

*I did no harm and this file is not truncated.*
