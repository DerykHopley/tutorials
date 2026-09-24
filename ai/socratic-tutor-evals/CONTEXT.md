# Evaluating a Socratic Tutor

The vocabulary this tutorial commits to. Terms are used consistently across
`ROADMAP.md`, the lessons, and the code. Most come from deepeval's JevEval docs; where
this tutorial uses a word more narrowly, the entry says so.

Definitions only. Plans live in [ROADMAP.md](ROADMAP.md), constraints in
[MISSION.md](MISSION.md).

## Language

**Spec**:
The behaviour you want, written down. For this tutorial, the tutor's system prompt,
verbatim in [NOTES.md](NOTES.md).
_Avoid_: Requirements, rubric (a rubric is one way of scoring against a spec)

**Test case**:
One input to evaluate — for the tutor, one conversation — together with the fields a
question is allowed to look at.
_Avoid_: Example, sample (both also mean "a line of training data")

**Jev**:
The decision model that answers questions about a test case with probabilities rather
than text. Reached from TypeScript through the OpenRouter decisions API.
_Avoid_: Judge, grader (both imply it writes a verdict; it doesn't)

**Question**:
One bounded thing Jev is asked about a test case. Always one of three types — Noul,
Score, or Choice.
_Avoid_: Check, criterion (a criterion is an option's *description* inside a question)

**Noul**:
A question that is a single true-or-false statement. Its value is the probability Jev
gives to true.

**Score**:
A question with ordered levels, written worst first. Its value is the expected level,
counted from 0, divided by the highest level.

**Choice**:
A question with unordered options, each given a Credit. Its value is the credit Jev's
answer earns, averaged over the options that count.

**Credit**:
What a Choice option is worth, from 0 to 1 — or `null` (Python: `None`), meaning "if this
is what happened, the question doesn't apply". Credits live in your code; Jev never sees
them.

**Value**:
One question's result for one test case, from 0 to 1 — or `null` when it doesn't apply.
_Avoid_: Score (that is a question type, and also the metric's result)

**Weight**:
How much one question counts towards the metric, relative to the others.

**Applicable**:
A question whose value counts. A Choice stops being applicable when its `null`-credited
options hold half the probability or more; its weight then leaves the total as well.

**Metric**:
A set of weighted questions. Its result — the **JevEval score** — is the weighted mean of
the applicable values, or 1 if none apply.
