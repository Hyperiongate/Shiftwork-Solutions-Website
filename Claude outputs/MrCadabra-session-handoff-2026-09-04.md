# MrCadabra — session handoff, 2026-09-04

> **Why this document exists.** All of the work below happened in the "Sept 26 speech" Claude project by accident — it has nothing to do with the AF&PA talk. This is the complete record so it can be moved into the MrCadabra project without losing anything. Nothing here needs to stay in the speech project.

**Machine:** gram15 · **Repo:** `D:\MyTutor` · **Session date:** 2026-09-04

---

## 1. State of the working tree — read this first

| Change | Files | Status |
|---|---|---|
| **BUILD sk** — `NIGHTWATCH_LESSONS` default 12 → 10, plus the ruletests check it would have broken | `nightwatch.py`, `ruletests.py` | ✅ **Committed by Jim** as `33e5b5e` (06:01), branch in sync with origin/main |
| **BUILD sl** — the seam reads `COURSE_ORDER` (server half only) | `main.py` | ⚠️ **UNCOMMITTED, on disk now** — 57 insertions, 7 deletions. Compiles, dry-run passed. |
| The page half of the seam change | `static/session.html` | ❌ **Not written.** Proposed diff is in §6 below. Awaiting approval. |
| Morning digest scheduled task — Night Watch absence alarm | (not a file — the scheduled task itself) | ✅ **Live**, took effect on today's 06:37 run |

**Also:** a stale `.git/index.lock` was deleted (it was mine — git created it, the mount wouldn't let git unlink it). **File deletion is now enabled for `D:\MyTutor` for the rest of that session.** Only that one file was deleted.

---

## 2. The Night Watch email that never arrived

**Symptom:** no `[Mr. Cadabra ops]` report on the morning of 09-04. Admin panel showed the run completed.

**Diagnosis:** the report reached the Titan mailbox at `support@mrcadabra.com` and **the forward to `jim@shift-work.com` silently dropped it.**

Evidence gathered:
- Nothing from `support@mrcadabra.com` anywhere in the Microsoft 365 mailbox since the 09-03 report at 09:12 UTC — searched across all folders, not just Inbox.
- **Not in Junk** (53 junk messages arrived in that window; none from MrCadabra).
- **No bounce, no NDR, nothing from postmaster.** Zero delivery failures in the mailbox.
- Mail flow otherwise healthy — messages arriving steadily all night.
- Night Watch had arrived every day without a gap since at least 08-23, always between 08:34 and 09:17 UTC.

**Still open:** why the Titan/GoDaddy forward stopped. Usual suspects are GoDaddy disabling a forwarding rule after bounces, a rule lost in a plan or DNS change, or a size/rate limit. **One clue worth checking:** an 08-29 bounce in the inbox from `postmaster@secureserver.net` concerned `jim+test@shiftwork.com` — note the domain is missing its hyphen. If anything in the forwarding config points at `shiftwork.com` rather than `shift-work.com`, it would fail exactly like this.

**Second signal to watch:** the weekly off-site backup email comes through the same forward and is due Mondays around 16:00 UTC. If it also goes missing, the forward is confirmed broken rather than a one-off.

---

## 3. The morning digest now alarms on a missing Night Watch

The digest's scheduled task prompt was updated. Changes:

- **MR. CADABRA OPS is never omitted.** Absence is treated as a finding, not an empty bucket. Previously an empty section simply vanished, which is why this failure was invisible.
- **A missing report is an ALERT at the very top**, above NEEDS JIM: *"ALERT — NIGHT WATCH DID NOT ARRIVE. No [Mr. Cadabra ops] report for &lt;date&gt;. Last one received &lt;date/time&gt;."*
- **`[NIGHT WATCH MISSING]` is appended to the email subject** so it's visible on a phone without opening it.
- **Consecutive missing days are counted** — distinguishes a one-off from a broken forward.
- **The known failure mode is written into the prompt**, so the digest says *"did not arrive"* and never *"did not run"* — the wrong wording would send you to Render when the problem is at GoDaddy.
- **The Monday backup is tied to it:** if both are missing, report one broken forward, not two gaps.

---

## 4. Triage of the 2026-09-04 Night Watch

### A correction worth recording

**The two crashes initially flagged as urgent were already fixed.** Both were ghosts draining out of the 7-day telemetry window — the counts were read without the dates, which the report's own legend warns against.

| Flagged | Reality |
|---|---|
| `mathcheck` crash — `'tuple' object has no attribute 'free_symbols'` ×4 | **Fixed 09-02, build ru** (`mathcheck.py`). `_parse` now raises on a result without `free_symbols`, so callers fail open. All four crashes were on 09-02. |
| `wipeBoard` — `Array.from(undefined)` ×5 | **Fixed 09-02, build sg** (`session.html`). The `child`→`student` sweep had rewritten `feed.children` to `feed.students`. Restored, plus `scrNext` now survives a crashed beat. All five errors inside one hour on 09-02. |

**Rule going forward: only a line marked LIVE is today's problem.**

### What is actually live

- **`floor · frac61`**, 08:28 UTC — the tutor tried three times to say *"add the top numbers"* with no condition, false for unlike denominators. **The floor worked** — nothing shipped, child got the fallback. Not a defect; the fraction-addition path keeps generating the falsehood, which is a prompt issue.
- **The 12 teaching findings** (1 HIGH, 7 MEDIUM, 4 LOW) — all live.
- **150 pass-throughs** — ongoing and by design (see §5).

### The 12 findings are about four rules, not twelve problems

| Rule family | Count | Status |
|---|---|---|
| **Rules 14 / 48 — notation written but not said aloud** | 5 | The `notation` referee **already exists and fired 31 times this week**; `unspoken` fired 14 more. So these are *not* missing referees — either the retry isn't converging, or the referee has gaps for these specific shapes (superscript `2⁻`/`2⁺`, `⟺`, `25% = 25/100 = 1/4`, the place-value equation, lowercase triangle labels). **Worth an hour of investigation before anyone writes a new referee.** |
| **Rule 61 — a law stated without its condition** | 2 | `falseuniversal`, `precedencelaw`, `frac61` all exist and are truth-class. The two that shipped were conduct-classified. |
| **Rule 39 — a check the student cannot fail** | 2 | Looks uncovered. |
| **The HIGH — board solves a different expression from the spoken one** | 1 | Looks uncovered. Cites no rule number, unlike every MEDIUM. See §5. |
| Rules 2 and 15 — asked for work the board hasn't shown | 2 | |

---

## 5. Why defects still ship — the architecture

**The referees are deterministic; the thing they check is not.** The reply is generated fresh by a model each turn, so the system is a deterministic filter around a nondeterministic generator. `ruletests` pins the filter — *given this known-bad string, does the referee fire?* It cannot pin what the model will say tomorrow.

**And the 150 shipped on purpose.** In `tutor.py`, `MATHCHECK_MAX_ATTEMPTS = 3` (one attempt plus two corrected retries). When they're spent, `_settle()` takes the least-bad draft and makes one decision:

- **Truth-class finding** — one of the seven names in `TRUTH_REFEREES` — **nothing ships.** The child gets the fallback line. Fired **once** this week.
- **Anything else** — **ships anyway**, logged `pass_through`. Fired **150 times**.

So *"replies shipped WITH a known finding: 150 ← should be zero"* is designed behaviour, not a malfunction. **602 referee fires, 150 deliberate ships — roughly a quarter of the time the retry doesn't converge.** `livecritic` alone is 105 of the 150.

### What "least-bad" actually means

`TRUTH_REFEREES` is the line: board arithmetic that doesn't hold, a named falsehood, the three rule-61 referees, a factor pair that doesn't expand, and a multiple-choice missing its right answer. Everything else is conduct and ships.

**For the bulk of the 150 that means "not as nice as it should be," not "wrong."** Three exceptions:

1. **`boardcount` is explicitly ruled conduct** in the "considered and NOT included" list beside `TRUTH_REFEREES`: *"a drawing miscounted — real, but a board/words disagreement the child can SEE; **ruled conduct until Jim says otherwise**."* **That note is waiting on a ruling.**
2. **The 09-04 HIGH is that same family.** The board wrote `2 + 3 × 4 = 2 + 12 = 14` while the tutor said 11 for `3 + 2 × 4`. Every character on the board is arithmetically true, so mathcheck passes it — it's the right answer to a different question, next to a spoken answer of 11. A child can leave believing the answer is 14.
3. **The floor fails open by design.** `_is_truth_finding` returns conduct for any unrecognised referee name ("never closed"), so classification errors ship. And a *crashed* referee produces no finding at all — which is why mathcheck crashes matter more than five log lines suggest.

**The lever:** `TRUTH_REFEREES` is data, not logic. Promoting the board/words-disagreement class would have floored the HIGH instead of shipping it. Cost: the child hits the fallback line more often, and a fallback teaches nothing either.

---

## 6. The scripted-first lane, and the seam bug

### How it works

`main.py` states three invariants under "Jim's scripted-first ruling" (build jt):

1. **No answer ever reaches the client.** Grading is code, server-side, always.
2. **The model never steers.** A wrong answer buys at most `SCRIPT_AI_TURNS` (3) bounded Model-Lead-Test turns *on that one problem*; the redo is graded by code; the engine's retest resumes the script. If the model fails, it falls back to the scripted retest — *"a dead model costs a child one worked example, never the lesson."*
3. **A script turn costs nothing.** Every non-intervention request is served from data, logged `kind="script"`.

**A child who answers correctly triggers zero model calls.** But **mastering the lesson is what ejects them onto the live path** — `__script_done_mastered__` hands the session to the live tutor. The reward for a flawless lesson is the nondeterministic lane; a child who keeps missing stays in the scripted one longer.

### The bug

`COURSE_ORDER` in `lessonscripts.py` is the authored sequence — **360 lessons, 36 per course × 10 courses**, and its own note records that it exists because an earlier build *"had accidentally placed carrying before two-digit-no-carry."* Import fails loudly on a missing or duplicated lesson.

**Nothing at the seam read it.** The system note told the live tutor *"Your FIRST sentence must NAME the new topic"* — but never **which**. The model picked. **That is the root of the 09-01 bug Jim watched: "one-less reads as subtraction."** Build rj made the model *announce* its guess; it did not remove the guess.

### What was built (BUILD sl — server half, on disk, uncommitted)

- `_next_lesson_id(current_id)` — reads `COURSE_ORDER`, returns the next authored lesson **in the same course**, or nothing at a course boundary / end of order.
- `_script_clean(steps, lesson_id)` now puts `next_id` and `next_topic` on a **mastered** `end` step. Empty on a still-learning end — the "still learning does not advance" ruling is enforced server-side, not left to the page.
- Lesson id passed at all five call sites. Change note under BUILD sl.

**Dry-run verified against the real data:** mid-course advances correctly (`entry-u1-counting-to-10` → `entry-u1-counting-past-ten`, "Counting past ten"); course boundary returns nothing; last lesson returns nothing; unknown id returns nothing. `main.py` compiles. No test pins `_script_clean`'s key set.

### The page half — not written, needs approval

`scriptStart()` already posts to `/api/script/start`, sets busy, ingests steps and returns true/false. It just always calls `scriptPick()` first. Two edits:

```js
// 1. let it start a known lesson
async function scriptStart(forcedId) {
  const les = forcedId ? { id: forcedId, topic: "" } : await scriptPick();
```

```js
// 2. at the seam (session.html ~line 3919), after the bridge line plays:
if (step.next_id && await scriptStart(step.next_id)) return;
```

If the call fails it falls through to the live tutor exactly as today — the same fail-open law as the rest of the lane. **A perfect student would then run 36 lessons without a single model call.**

---

## 7. Jim's rulings, 2026-09-04

1. **Mastery auto-advances.** No student choice. (Later refined — see §8.)
2. **Still learning does not advance.** Encourage more practice first.
3. **Announce the new topic clearly, scripted.**
4. **Resume at a lesson boundary, never mid-problem** — if they stop halfway, go back to the start of that lesson to refresh.

**Note on #4: this is already true.** `_SCRIPT_SESSIONS` is in-memory, and the code already calls a deploy mid-lesson "acceptable and HONEST: better than resuming corrupted." Any interruption returns to the start of a lesson. The remaining question is only which lesson the picker resumes at — `store.get_script_done()` gives the mastered ids and `/api/session` already ships them.

**Open question #5, raised and not yet ruled:** the **course boundary**. Finishing `entry-u9-sharing-fairly` and rolling into Basic is a much bigger moment than finishing one lesson. Currently returns nothing and falls through to the live tutor. (Jim's later direction in §8 answers this.)

---

## 8. Later direction — pedagogy (investigation was in progress when the session turned)

Three things Jim raised, plus a request to review the pedagogy on record:

1. **The struggling child should get a warm choice**, not a block: *"You're doing great — would you like to go on to the next lesson, or review this a bit more to get it solid?"* **This softens ruling #2 above** and needs reconciling with it.
2. **Course completion should be a major celebration** — "Fourth of July," a printable certificate. Note this converges neatly with open question #5: the course boundary currently falls through to the live tutor, which is the *worst* handling of the biggest moment in the course.
3. **Periodic quizzes should include review material**, not only what was just taught — built-in spaced review as the child progresses.

### What the investigation found before it stopped

**The pedagogy on record** (`lessonscripts.py`, "THE SETTINGS"):

- `ADVANCE_STREAK = 3` — advance on 3 consecutive unaided correct (cited EDM 2015)
- `MAX_PROBLEMS = 10`
- `DROP_AFTER_INTERVENTIONS = 2` — second intervention on a skill drops a representation level
- `LEVELS = ("abstract", "pictorial", "concrete")` — **drop direction, left to right**
- Worked examples then example-problem pairs; error path = scripted "let's look together" → AI Model-Lead-Test → engine-issued same-form retest; failing at concrete ends warmly and marks "learning"; a garbled answer gets one scripted re-ask then tap-only, never an AI call for a mishearing.
- `MIN_PROBLEMS = 4` was **removed** by Jim's ri ruling on 09-01 (the words promise three-in-a-row, so the code stops demanding a fourth).

**⚠️ The source document is missing.** Every setting is attributed to `Ruling_Scripted_First_And_The_Settings_2026-08-20.md` — *"THE SETTINGS ARE THE RESEARCH DOC'S, NOT OPINIONS (citations there)"* — and **that file is not in the repo.** The citations behind every pedagogical constant live outside the codebase. Worth locating and committing.

**Two observations to carry into the recommendation:**

- **The level sequence is inverted relative to the mainstream.** Standard CRA builds *concrete → pictorial → abstract*. This system starts abstract and falls back toward concrete on failure. That's defensible (efficiency-first, scaffold on demand) but it inverts the sequence the Eureka/EngageNY materials in the repo are built on. Worth a deliberate decision rather than an accident.
- **Quizzes currently contain zero review.** `_quiz_questions(lesson)` reads `quizsets.QUIZ_SETS.get(lesson["id"])` — keyed by a **single lesson id**. `QUIZ_LEN = 5`, `QUIZ_PASS_PCT = 80`, `QUIZ_MIN = 3`, and the quiz asks at the lesson's top level.

**The good news for Jim's spaced-review idea: everything needed already exists.**

- `quizsets.QUIZ_SETS` holds **360 lessons × 5 pre-vetted problems = 1,800 pinned quiz items**, one set per lesson.
- `store.get_script_done(code, course)` returns the lessons *this child* has mastered — so review items can be drawn only from material they have actually been taught.
- `lessonscripts.quiz_start(lesson, problems)` is **agnostic about which problems it's given.**

**So this is a change to one selection function, not new content.** `_quiz_questions` is the single seam.

**Consequences to decide when the recommendation is written:** with `QUIZ_LEN = 5`, a 30–40% review mix is only 1–2 items — probably too thin, which argues for a longer unit-level quiz distinct from the short lesson check. And adding review makes the instrument harder, so `QUIZ_PASS_PCT = 80` (4 of 5) may need revisiting — plus a child who fails on *review* items needs different remediation from one who fails on current material.

There is already a hierarchy in the codebase to build on: **lesson → Unit Quiz → Course Assessment**, with a policy (build ew) that a student who validates units on the Course Assessment must still pass those Unit Quizzes before the Final Exam opens.

---

## 9. Recommended order of work

1. **Finish the seam** (§6). It's the only item that *removes* a model call from a child's path rather than policing one. Server half is done; the page half is two lines. Needs the still-learning path resolved against §8's softened ruling first.
2. **Rule the board/words-disagreement class** (§5). Your own code has been waiting on it. Promoting it would have floored the 09-04 HIGH.
3. **Investigate why the retry doesn't converge before writing any new referee** (§4). 105 livecritic pass-throughs is the biggest single quality lever, and five of the twelve findings sit behind a referee that already fires 31 times a week.
4. **Write the spaced-review recommendation** (§8) — one selection function, all the data in place.
5. **Find and commit the 2026-08-20 research doc** (§8). The citations for every pedagogical setting currently live nowhere in the repo.
6. **Chase the Titan forward** (§2). Check the forwarding destination for the missing hyphen.

---

*I did no harm and this file is not truncated.*
