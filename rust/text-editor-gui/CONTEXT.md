# Text Editor GUI

The vocabulary this tutorial commits to. Terms here are used consistently across
`ROADMAP.md`, the lessons, and the code — a word that means two things in the roadmap
becomes two features nobody can tell apart.

Definitions only. Plans live in [ROADMAP.md](ROADMAP.md), constraints in
[MISSION.md](MISSION.md).

## Language

**Buffer**:
One file's text held in memory, together with what the editor knows about it — where it
came from and whether it differs from disk.
_Avoid_: Document, file (when you mean the in-memory thing)

**Untitled Buffer**:
A Buffer with no location on disk yet. It cannot be saved without being given one.
_Avoid_: New file, unsaved buffer (which means a Buffer with unwritten edits — a
different thing an Untitled Buffer may or may not also be)

**Directory**:
A location on disk the editor is displaying the contents of. Carries no metadata and
nothing is remembered about it between runs.
_Avoid_: Folder, workspace, project (when no metadata is involved)

**Project**:
A Directory plus metadata that tells the editor something it could not work out by
looking at the files.
_Avoid_: Workspace, folder

## Notes

**Directory and Project are different intentions, not two sizes of the same thing.**
"Open directory" shows you what is on disk. "Open project" additionally tells the editor
something about how to treat it. A Directory never becomes a Project by growing; it
becomes one when metadata is attached.
