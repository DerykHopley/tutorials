# Roadmap

What's built, what's next, and what's deliberately not happening.

Lessons are written **just-in-time**, as in the Rust tutorial: a part is planned here in a
line and its lessons are written once the part before it runs. Here that matters twice
over, because every lesson after the first makes paid API calls, and a premise about
Jev's answers has to be measured before a lesson can stand on it.

Vocabulary is in [CONTEXT.md](CONTEXT.md).

## The loop this tutorial follows

1. **Spec** — the behaviour you want: the tutor's system prompt.
2. **Test cases** — conversations that trigger each rule, especially the hard ones.
3. **Questions** — each rule as a bounded, weighted question for Jev.
4. **Run and read the breakdown** — the total says *whether* something failed; the
   per-question values say *which* rule.
5. **Iterate** — change the prompt or the question, and rerun the *same* test cases.

## Done

| Lesson | Title | What it delivered |
| --- | --- | --- |
| [1](lessons/0001-where-a-score-comes-from.html) | Where a Score Comes From | The JevEval arithmetic in TypeScript, reproducing the docs' 0.461 by hand; levels written best first as a silent inversion; a question that doesn't apply leaving the total |

## Next

| # | Part | Lessons | What you'll learn |
| --- | --- | --- | --- |
| 1 | **One metric, end to end** | 2–3 | Lesson 2: one real decisions call replaces lesson 1's made-up probabilities, and settles what the answer fields mean. Lesson 3: the tutor's rules as questions — choosing a type, phrasing a Noul so true is good, weights, and why not the exercise 19 judge |
| 2 | **Test cases that bite** | 2–3 | Loop step 2: adversarial conversations ("just tell me", "it's urgent", shared buggy code), and generating the tutor's side from the real system prompt |
| 3 | **Reading the breakdown** | 2–3 | Loop steps 4–5: which question fell short, prompt fix vs question fix, and the before/after run MISSION.md asks for |

## Not happening

| Not doing | Why |
| --- | --- |
| **Python deepeval as the main path** | The course repo is TypeScript. deepeval's code appears as sidenotes for comparison |
| **Other deepeval metrics** | Out of scope in MISSION.md, except as a comparison |
| **Confident AI** | Out of scope in MISSION.md |
