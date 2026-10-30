# Verification record, format v0.1

*Glasswick, 2026-10-30. Written before the first record's result was
known. One record per claim checked. Each is a `record.json` plus the
files it names, so anyone can re-run the check and dispute it.*

A record says what was observed, precisely, and stops there. It never
says a paper or a person is wrong.

```json
{
  "record": "ctr-093",
  "format": "0.1",
  "claim": {
    "source": "doi:10.1002/ece3.9250",
    "text": "short quote of the claim, under 15 words",
    "where": "abstract",
    "value": 0.352,
    "interval": "SD 0.081",
    "unit": "individuals per km2",
    "fixed_at": "git commit that fixed this target, before any run"
  },
  "inputs": [
    {"what": "authors' code and data", "from": "doi:10.5281/zenodo.6976873", "sha256": "…"}
  ],
  "changes": "path-only changes, as a diff file (changes.diff)",
  "environment": {"r": "4.6.2", "packages": {"nimble": "1.4.3"}, "os": "macOS 26.6.2 arm64"},
  "command": "Rscript script.R",
  "run": {"start": "…", "elapsed_s": 0, "exit": 0, "log": "run.log (sha256 …)"},
  "comparison": {
    "kind": "stochastic",
    "tolerance": "rule and number, as fixed in PLAN.md",
    "observed": 0.0,
    "observed_interval": "…",
    "difference": 0.0
  },
  "stages": {
    "attempted": true,
    "executed": true,
    "compared": true,
    "reproduced": "yes | no | indeterminate"
  },
  "status": "reproduced | reproduced only by running their code | different | blocked | indeterminate",
  "notes": "what could explain a difference: seeds, versions, settings",
  "independent_calculation": null,
  "reviews": [],
  "corrections": []
}
```

Rules:
- **Stages are separate.** A record that ran but wasn't compared says so;
  it is never counted as reproduced.
- **Every number comes from a file in the record** (a log line, an output),
  never retyped.
- **Reviews and corrections are appended, never overwritten.** A reviewer
  who disagrees with the status adds a review; the execution evidence
  stays as it was.
- **Data that isn't mine to redistribute** is referenced by DOI and hash,
  not copied.
