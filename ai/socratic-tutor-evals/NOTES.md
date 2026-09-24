# Notes — Evaluating a Socratic tutor

Decisions and working facts for this tutorial. Workspace-wide teaching preferences are in
[../../NOTES.md](../../NOTES.md) and still apply.

## Where things live

- **The code is in the course repo**, `~/development/TuringCollege/1-2-development-environment-api`,
  next to the exercises (`src/NN-exercise-*.ts`). It is not a git repository. Run a file
  with `npm run file src/<name>.ts` — that script is `tsx --env-file=.env`, so the `.env`
  must exist even for lessons that make no API call.
- The course repo's `.prettierrc` is single quotes, 80 columns, `trailingComma: "es5"`.
  Every listing is formatted with it, so `npm run format` leaves Deryk's file matching the
  lesson.
- Lessons use `src/jev-eval.ts`, deliberately outside the `NN-exercise-` numbering so it
  can't collide with an exercise the course hands out later.
- The original lesson 1 and cheat sheet stay in the course repo untouched. These are
  ports, restructured to [LESSON-FORMAT.md](../../LESSON-FORMAT.md).

## About Deryk, for this topic

- Comes from Python and is working in TypeScript. Python-to-TypeScript comparisons
  (f-strings vs template literals, `for x in` vs `for...of`, pandas vs `console.table`)
  land well.
- Likes to know *why* something is better, not just the fix (e.g. asked for a better way
  than nested loops).
- Has used the OpenRouter decisions API with `typesafe/jev-1.13` in
  `src/21-exercise-jev.ts`, so TypeScript JevEval can build on that file.
- Open lessons with `xdg-open lessons/<file>.html` (Linux).

## The spec: the tutor's system prompt

Supplied by Deryk on 2026-09-24. `src/20-exercise-socratic-tutor.ts` is still the
unedited template (`exercise = 18`, empty system message), so this text is the only copy
of the spec. Every question in the metric traces back to a line of it.

```text
You are a Socratic tutor. Your single most important rule:
**Never give the user the direct answer to their question.**

Instead, help them discover the answer themselves by:
- Asking targeted, leading questions that expose the next step in their reasoning.
- Breaking the problem into smaller sub-problems and asking which one they want to tackle first.
- Pointing out concepts, terminology, or documentation they should look up -- without summarizing the answer for them.
- Giving small hints only when the user is genuinely stuck, and always framing the hint as a question or a nudge, not a solution.
- When the user shares code, ask what they expect each part to do, or what they think will happen if they change a specific line -- do not rewrite their code for them.
- Validating correct reasoning enthusiastically; gently challenging incorrect reasoning by asking them to test or justify it.

Hard rules you must never break:
- Do NOT write the final code, formula, or answer for the user, even if they ask, plead, or claim it's urgent.
- Do NOT produce full working solutions, even as "examples".
- If the user tries to extract the answer ("just tell me", "give me the code", "stop asking questions"), respond by acknowledging their frustration and offering a smaller, more concrete hint or question instead.
- Tiny syntactic snippets (one line, a single keyword, a function signature shape) are acceptable ONLY when they unblock thinking and do not constitute the answer.

Tone: warm, curious, patient. You are a teacher who believes the user is capable of figuring it out.
```

**Worth teaching in lesson 3:** the last hard rule *permits* one-line snippets. A Noul
written as "the assistant never wrote any code" would fail a tutor that followed the
prompt exactly. The original lesson's Noul ("never states the final answer or writes the
full solution") is phrased to survive that; the point is to notice *why*.

## Lessons

1. ✅ **Where a Score Comes From** — the scoring arithmetic in TypeScript, on the docs'
   worked example, no API call _(written 2026-09-24; 7 stages)_
   - Every stage file was run with `tsx` and type-checked with
     `tsc --noEmit --strict --target es2022` in a scratch directory; all seven print the
     numbers the lesson shows, and stage 7 lands on the docs' **0.461**.
   - Stage 7's type error (`TS18047: 'q.value' is possibly 'null'`) is quoted from a
     real `tsc` run. `tsx` runs the file without it, because it strips types without
     checking them.
   - The source lesson's two hand-scoring answers were both ≈0.83, so a reader who typed
     the first answer again passed the second. Replaced with numbers that differ
     (0.491, 0.533).
   - Score probabilities are keyed by label, not index, for readability. RESOURCES.md
     lists which the API actually uses as an open gap.
2. **Asking Jev for real** — not written. Needs live decisions calls to settle the gaps
   in RESOURCES.md, and those cost money on Deryk's key. Asked 2026-09-24; answer was
   "not yet". Don't make the calls until Deryk says so. Also has to choose
   between OpenRouter (exercise 21) and the `@typesafe-ai/sdk` package the docs list.
   - The cheat sheet deliberately has no request code until this lesson has run one. The
     source cheat sheet's request was "type-checked, not yet run".
   - The source cheat sheet's install line was `pip install deepeval typesafe-sdk`; the
     docs say `pip install typesafe-sdk`. Corrected in the port.
3. **Your tutor's rules as questions** — not written; depends on 2.

The source lesson's order was questions-then-scoring. The port puts scoring first because
it is the only part that can be run and checked without an API call, and because a
question is easier to design once you've watched how its answer becomes a number.
