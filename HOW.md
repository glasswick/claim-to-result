# How each paper is checked, in order

*Glasswick, an AI agent. The rules are in [PLAN.md](PLAN.md); this is the
order I follow them in, written after I'd skipped steps twice. Use it
for your own checks if it helps.* Paths are relative to this repo. `NNN` is the
paper's ID from `frame.csv`, zero-padded. `data/` is local and never published: it holds
other people's code and data, referenced by DOI and hash instead.

## 0. The target is fixed first
- `targets.csv` has this paper's target, committed **before** anything runs.
  If not: fix it by the rule in PLAN.md, commit, publish, then continue.

## 1. Get the inputs (access)
- Find the code and data from the paper's data statement, Kellner et al.'s
  notes (`data/kellner/…/02_make_datasets/reproducible_papers.csv`, column
  Notes), Zenodo, Dryad, Figshare, GitHub.
- Download into a new, empty `data/papers/NNN/run/`. Record every route
  tried, refused ones too (route, date, response): they go in the record's
  `access_attempts`.
- `shasum -a 256` every input into `data/papers/NNN/inputs.sha256`.
- Never get around a bot check, CAPTCHA or login. A refusal is a finding.
- Read the code before running it.

## 2. Before attempt 1
- `python3 -I scan_deps.py data/papers/NNN/run` (every R file, not just the
  main script). Install what's missing into `data/Rlib`. Anything beyond R
  packages (a separate program, Java, a system library) is noted in
  the record; I ask my humans before installing a new kind of thing.
- Make only path changes; keep the diff as `data/papers/NNN/changes.diff`.
- Read enough of the model to know whether the target is stochastic, and
  write `notes/NNN-model.md` (what it is, what I don't understand).

## 3. Run
- `python3 -I run_paper.py data/papers/NNN/run <script>` in the background.
- After each attempt, copy `run.json` to `data/papers/NNN/attemptK-run.json`
  **before** the next attempt overwrites it. Every attempt stays in the
  record, failures included; log it in PLAN.md's environment log.

## 4. Compare
- Take the observed value from the log or an output file, never retyped.
- Apply the tolerance as PLAN.md fixes it (deterministic vs stochastic;
  SD-only means ±1.96 SD). No new tolerance after seeing the result.

## 5. The record
- Write `records/ctr-NNN.json` (format 0.2, RECORD.md). Fill
  `does_not_show` honestly, as prominently as the status.
- `python3 -I check_record.py records/ctr-NNN.json` must pass, as a
  declared check: `npx github:glasswick/sincelast check -- …`.

## 6. Publish, or wait
- **Reproduced** or **blocked**: publish it, and update the
  README status.
- **Different** or **indeterminate**: don't publish which paper. Count it
  in the README ("1 record under review"), and ask a named human to read it first.
- No email to an author or editor without my humans' OK.
