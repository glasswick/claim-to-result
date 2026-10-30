"""Check verification records against RECORD.md's format.

  python3 -I check_record.py            the example in RECORD.md
  python3 -I check_record.py a.json ... record files

A record must have a status, all four stages, and a non-empty
does_not_show (format 0.2: what the record does not show is as required
as what it does)."""
import json, os, re, sys

STATUSES = {"reproduced", "reproduced only by running their code", "different", "blocked", "indeterminate"}
here = os.path.dirname(os.path.abspath(__file__))

def problems(d, example=False):
    out = []
    if d.get("format") != "0.2": out.append(f"format is {d.get('format')!r}, expected '0.2'")
    if not example and d.get("status") not in STATUSES: out.append(f"status {d.get('status')!r} is not one of {sorted(STATUSES)}")
    if set(d.get("stages", {})) != {"attempted", "executed", "compared", "reproduced"}: out.append("stages must be attempted, executed, compared, reproduced")
    if not d.get("does_not_show"): out.append("does_not_show is missing or empty")
    for k in ("claim", "inputs", "environment", "reviews", "corrections"):
        if k not in d: out.append(f"missing {k}")
    return out

if len(sys.argv) == 1:
    text = open(os.path.join(here, "RECORD.md")).read()
    block = re.search(r"```json\n(.*?)\n```", text, re.S).group(1)
    targets = [("RECORD.md example", json.loads(block), True)]
else:
    targets = [(p, json.load(open(p)), False) for p in sys.argv[1:]]
bad = 0
for name, d, ex in targets:
    ps = problems(d, ex)
    bad += bool(ps)
    print(("ok   " if not ps else "BAD  ") + name + ("" if not ps else ": " + "; ".join(ps)))
sys.exit(1 if bad else 0)
