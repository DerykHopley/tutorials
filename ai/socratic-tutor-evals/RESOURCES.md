# Evaluating a Socratic Tutor with JevEval: Resources

## Knowledge

- [Docs: JevEval — deepeval](https://deepeval.com/docs/metrics-jev-eval)
  Primary source. Question types, scoring formulas, strict mode, the worked example ending
  at 0.461, and how to write questions about a conversation. Use for: anything about how a
  JevEval score is produced. Every number in the worked example was checked on 2026-09-24
  and reproduces exactly in lesson 1's code.
- [Guide: JevEval examples — deepeval](https://deepeval.com/guides/guides-jev-eval-examples)
  Worked metrics per use case, including a multi-turn trace. Use for: how many questions,
  which types, choosing weights.
- [Docs: Multi-turn test cases — deepeval](https://deepeval.com/docs/evaluation-multiturn-test-cases)
  `ConversationalTestCase`, `Turn`, `scenario`, `expected_outcome`. Use for: building tutor
  conversations to evaluate.
- [Docs: G-Eval — deepeval](https://deepeval.com/docs/metrics-llm-evals)
  The generative-judge alternative. Use for: comparing with JevEval and with the exercise
  19 judge.
- [Blog: Introducing Jev in deepeval](https://deepeval.com/blog/introducing-jev-in-deepeval)
  Why a "System One" decision model instead of an LLM judge; hybrid and system_one modes;
  pricing. Use for: the reasoning behind Jev.
- [Docs: Jev on OpenRouter](https://openrouter.ai/docs/guides/community/jev)
  Decisions API endpoint, model ids (`typesafe/jev-1.13`), answer fields. Use for: calling
  Jev from TypeScript, as in exercise 21.
- [Article: "Your AI Product Needs Evals" — Hamel Husain](https://hamel.dev/blog/posts/evals/)
  Practitioner guide to the evaluation loop: scoped tests, test cases, looking at lots of
  data. Use for: workflow and test-case design.
- [Article: "A Field Guide to Rapidly Improving AI Products" — Hamel Husain](https://hamel.dev/blog/posts/field-guide/)
  Error analysis and iterating on real failures. Use for: deciding what to fix after a run.
- [Paper: "Towards Responsible Development of Generative AI for Education: An Evaluation-Driven Approach" — Jurenka et al., Google, 2024](https://arxiv.org/abs/2407.12687)
  Turning learning-science principles into tutor evaluations (LearnLM-Tutor). Use for:
  which tutoring behaviours are worth measuring.

## Wisdom (Communities)

- [deepeval Discord](https://discord.gg/a3K9c8GRGt)
  Official community linked from the deepeval docs. Use for: JevEval questions, metric
  design critique.
- Your Turing College cohort and mentors
  Use for: comparing tutor metrics and test sets with peers doing the same exercise.

## Gaps

- **No verified source yet on the exact meaning of `score` in OpenRouter's decisions API
  response.** 0-based expected level is assumed from the deepeval worked example. Lesson 2
  exists to measure this against a real response before anything is built on it.
- **Whether a Score answer's probabilities come back keyed by level index or by label.**
  The docs show them by index (`{0: 0.05, 1: 0.30, …}`); lesson 1 keys them by label for
  clarity and says so. Same measurement as above.
- **Which TypeScript route to call Jev by.** The deepeval docs list `npm install
  @typesafe-ai/sdk` with `TYPESAFE_API_KEY`; exercise 21 used the OpenRouter decisions API
  with `OPENROUTER_API_KEY`. Found 2026-09-24, not yet compared. Lesson 2 has to pick one.
- No practitioner write-up yet on adversarial test sets specifically for "never give the
  answer" tutors.
