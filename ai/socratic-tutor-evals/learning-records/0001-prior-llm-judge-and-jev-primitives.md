# Prior knowledge: rubric LLM judge and Jev's three primitives

> Ported from the Turing College course repo on 2026-09-24, unchanged apart from this
> note.

Before this course, the user built a rubric-based LLM-as-a-judge pipeline (exercise 19: a
1–5 rubric on four dimensions, parsing `Dimension: score | justification` text) and
called Jev directly through the OpenRouter decisions API with noul, choice and score
questions (exercise 21). So the idea of a judge and the request shape of the three
primitives are known. What is new is how JevEval turns answers into a score (value
mappings, weights, `None` applicability) and the wider evaluation loop.

**Evidence:** `src/19-exercise-LLM-as-a-Judge.ts` and `src/21-exercise-jev.ts` in the
course repo. Exercise 19 was written with a lot of help, so treat the judge pipeline as
familiar, not mastered.

## Implications

- Don't re-teach what an LLM judge is. Start from the score mapping and question design,
  and contrast with exercise 19's parse-and-fallback approach.
- Exercise 21 already made one real decisions call, so lesson 2's API call is a small
  step from known ground — the new part is checking what the answer fields mean.
