# Working Notes — workspace-wide

Everything here applies to **every** topic in this workspace. Topic-specific notes
live in `<topic>/<tutorial>/NOTES.md`.

## About Deryk

- Machine: Fedora-based atomic desktop (rpm-ostree, `/var/home` layout), kernel 7.1.8,
  Wayland. Prefer per-user toolchains in `$HOME` over `rpm-ostree install` — layering
  packages onto the base image is the wrong move on an atomic desktop.
- Started this workspace 2026-08-16.

## Teaching preferences

These were earned through real friction and generalise past any one topic. The
mechanics of each live in [LESSON-FORMAT.md](./LESSON-FORMAT.md); the *reasons* live here.

- **Never show finished work up front** (2026-08-16). Build it in stages, explain each
  part as it's added, and make every stage runnable. Stated why: "I would like to
  understand what each part is doing while building up to completion." A finished
  artifact teaches recognition; watching it become necessary teaches causation.
- **`main` stays pristine; Deryk works on a branch** (2026-08-16). `main` holds the
  scaffold a *new* learner starts from — never anyone's completed lesson code — because
  it may be published for others. Deryk's progress lives as commits on a
  `work/<topic>-<tutorial>` branch on top of it.
  **Never commit lesson solutions to `main`, and never modify the working files on
  Deryk's branch** — doing the work is the entire point. Write the lesson; leave the code
  alone.
- **Single self-contained HTML files.** Nothing loaded from disk at runtime. Authored
  from `assets/` and inlined by `python3 build.py`.
- **Highlight must-do details** that are easy to skim past, and put them *before* the
  thing they apply to. Prompted 2026-08-16 by missing a renamed parameter that was
  mentioned only in prose after the code block.
- **One block, one change.** Two edits in one block means the second gets lost.
  Prompted 2026-08-16 by an "… and at the bottom of main:" comment doing exactly that.
- **Prefers structural navigation over line numbers** — and was right about why. See
  the reasoning in [LESSON-FORMAT.md](./LESSON-FORMAT.md); it generalises to any topic
  where instructions point into a larger artifact.
- **Wants a fast way back to the source material** from a self-test they got wrong.
- **Gloss domain jargon on first use — but don't avoid it.** Say the plain thing, then
  name the term of art: "shifts four spaces to the left — also called a *dedent*". Stated
  2026-08-16 after Deryk asked whether "dedents" was a misspelling and then said knowing
  the word was useful. Dropping the jargon entirely would have withheld something worth
  having; using it unexplained cost them a detour. Do both.

## How I should verify things

Deryk has caught me shipping claims I hadn't checked, and the checks keep finding real
bugs. Standing rules:

- **Never trust parametric memory for an API.** Compile it, run it, or fetch the docs.
  The egui `App` trait signature changed in a way my priors got wrong.
- **Render the document and look at it.** Screenshot the actual output rather than
  reasoning about the CSS. This caught illegible chips, a white scrollbar on a dark
  block, and a line-count mismatch.
- **Extract code back out of the rendered lesson and compile *that*.** It checks what
  Deryk will actually read, not what I meant to write.
- **Verify interactive behaviour by driving the page**, not by reading the JS.
- **Never touch Deryk's in-progress working files** to run a check. Use a scratch
  target and delete it. That includes fixing their code when a lesson misled them —
  tell them the line to add; doing it for them removes the work.
- **Diagnose from their actual file, not from the lesson.** When Deryk reports a
  mismatch, read their source first. Twice now the reported cause and the real cause
  differed.
