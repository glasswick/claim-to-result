"""List the R packages a run folder's code loads, and which aren't installed.
Run before attempt 1, so a missing package doesn't cost an attempt
(paper 93's first attempt died on a package loaded by a sourced helper).

  python3 -I scan_deps.py <run-dir>

Scans every .R/.r/.Rmd file in the folder (not only the main script) for
library(), require(), requireNamespace() and pkg::fn."""
import os, re, subprocess, sys

run_dir = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r"""(?:library|require|requireNamespace)\(\s*['"]?([A-Za-z][A-Za-z0-9.]*)|\b([A-Za-z][A-Za-z0-9.]*)::""")
found = {}
for root, _, files in os.walk(run_dir):
    for f in files:
        if f.lower().endswith((".r", ".rmd")):
            text = open(os.path.join(root, f), encoding="latin-1").read()
            for m in PAT.finditer(text):
                found.setdefault(m.group(1) or m.group(2), set()).add(f)
env = dict(os.environ, R_LIBS_USER=os.path.join(here, "data", "Rlib"))
have = set(subprocess.run(["Rscript", "-e", "cat(rownames(installed.packages()), sep='\\n')"],
                          env=env, capture_output=True, text=True).stdout.split())
missing = sorted(p for p in found if p not in have)
for p in sorted(found):
    print(f"{'MISSING' if p in missing else 'ok     '} {p:20} {', '.join(sorted(found[p]))}")
print(f"{len(found)} packages, {len(missing)} missing" + (f": {' '.join(missing)}" if missing else ""))
sys.exit(1 if missing else 0)
