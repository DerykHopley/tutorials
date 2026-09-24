# Mission: Evaluating a Socratic tutor

> **Draft.** Written from the first request and not yet confirmed. See "To confirm" at the
> bottom. Ported from the Turing College course repo on 2026-09-24.

## Why

Build the Socratic tutor for exercise 20 and show, with repeatable evaluations, that it
keeps its hard rules — above all, never give the direct answer. Learn the deep-evaluation
workflow well enough to reuse it on later LLM projects in the course.

## Success looks like

- A JevEval metric that covers every rule in the tutor's system prompt, with weights you
  can justify
- A set of test conversations, including adversarial "just tell me" / "it's urgent"
  cases, that the metric runs against
- Reading a per-question breakdown and deciding whether to change the prompt or the
  question
- A before/after run showing that a prompt change improved the score

## Constraints

- **TypeScript, in the course repo** (Node, OpenRouter). Deryk comes from Python, so
  Python equivalents appear as sidenotes, never as the main path. deepeval's own JevEval
  is a Python library; the TypeScript route sends the same questions to Jev through the
  OpenRouter decisions API and does the scoring arithmetic in code — which is also the
  route that shows where the score comes from.
- Cost-sensitive nano/mini models for the tutor itself (curriculum rule).
- The code lives in the course repo, where the exercise is marked. This tutorial holds
  the lessons, not the project.

## Out of scope

- Other deepeval metrics (G-Eval, DAG, …) except as a comparison
- The Confident AI cloud platform

## To confirm

- Is the goal mainly to complete exercise 20, or to own the evaluation workflow as a
  reusable skill? If it's the second, this tutorial is misnamed and should become
  `ai/llm-evals`.
- ~~Run JevEval through Python deepeval, or stay in TypeScript?~~ **TypeScript**,
  confirmed by Deryk on 2026-09-24 (see Constraints).
- Any deadline or session length?
