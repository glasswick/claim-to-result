"""Run one paper's R script under the study's rules (PLAN.md):
a hard 24-hour limit, the lane's own R library, everything logged.

  python3 -I run_paper.py <run-dir> <script.R>

Writes <run-dir>/run.log (all output) and <run-dir>/run.json (start, end,
elapsed, exit code or "timeout", R and package versions)."""
import json, os, subprocess, sys, time

LIMIT = 24 * 3600
run_dir, script = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, R_LIBS_USER=os.path.join(here, "data", "Rlib"))
info = {"script": script, "start": time.strftime("%Y-%m-%d %H:%M:%S %z")}
t0 = time.time()
with open(os.path.join(run_dir, "run.log"), "w") as log:
    try:
        rc = subprocess.run(["Rscript", script], cwd=run_dir, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=LIMIT).returncode
    except subprocess.TimeoutExpired:
        rc = "timeout"
info.update(end=time.strftime("%Y-%m-%d %H:%M:%S %z"), elapsed_s=round(time.time() - t0), exit=rc)
info["session"] = subprocess.run(["Rscript", "-e", "for (p in rownames(installed.packages(lib.loc=Sys.getenv('R_LIBS_USER')))) cat(p, as.character(packageVersion(p)), '\\n'); cat(R.version.string, '\\n')"],
                                 env=env, capture_output=True, text=True).stdout
json.dump(info, open(os.path.join(run_dir, "run.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in info.items() if k != "session"}))
sys.exit(0 if rc == 0 else 1)
