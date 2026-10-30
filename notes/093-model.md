# Paper 93: what the model is (my notes, 2026-10-30)

*Jiménez, Díaz-Ruiz, Monterroso, Tobajas & Ferreras (2022), "Occupancy
data improves parameter precision in spatial capture-recapture models",
Ecology and Evolution, doi:10.1002/ece3.9250. Sources: the abstract, and
the authors' code (`Stone_marten_SCR-Occ-Tel.R`, zenodo 6976873), lines
cited below. Written by reading, before the run finished; nothing here
is a result.*

## In one paragraph, for an ecologist
A Bayesian spatial capture-recapture model with data augmentation,
integrating three data sources that share one set of activity centres
and one movement scale σ. Stone martens are imagined as up to M = 500
potential individuals; each is real with probability ψ (`z[i] ~
dbern(psi)`), with an activity centre uniform over a rectangle: the
camera grid's extent plus a 2 km buffer (`buff <- 2`, coordinates in
km). Density is N/area, where N is the number of real individuals
(`D <- N/area`). The target, 0.352 (SD 0.081) per km², is the posterior
mean and SD of that D.

## The three submodels (code lines 379-463)
1. **Box traps, individuals known** (live capture, transponders). Daily
   detection hazard falls off with distance as a half-normal,
   `p0.trp * exp(-d²/2σ²)`, turned into a probability `1 - exp(-hazard)`;
   each individual's captures at a trap are binomial over that trap's
   operating days (`y[i,j] ~ dbinom(pscr*z, KT.trap[j])`).
2. **Cameras, individuals not known** ("occupancy" data). For each camera
   only the number of days with any marten detected (counts turned to
   0/1 per day, line 233). The chance of a detection on a day is one
   minus the chance that no real individual is detected
   (`1 - prod(pn[1:M,j])`), binomial over operating days. This is what
   extends the model beyond the box-trap area and, per the abstract,
   improves precision by 37% (coefficient of variation) over standard SCR.
3. **Telemetry**, 4 collared animals: each location is normal around
   that animal's activity centre with SD σ, so telemetry pins down σ,
   the scale shared by both detection models.

## What this means for checking the number
- D depends on the state-space area, set by the 2 km buffer; my run uses
  the authors' code unchanged, so the same definition.
- It's MCMC with no fixed seed (`setSeed = FALSE`): stochastic. My
  tolerance (PLAN.md): the larger of 5% of 0.352 and 10% of the
  ±1.96 SD interval's width, about 0.032.
- Kellner et al. noted "apparently missing some models from paper". From
  the abstract, those are the standard-SCR comparison and the
  simulations; the 0.352 comes from the integrated model, which is the
  one in the code. So the target is computable from what's shared.
- The run is slow because every camera-day likelihood takes a product
  over all 500 potential individuals.
- A check I can do on the result: if ψ's posterior crowds against 1,
  M = 500 was too small and N is truncated.

## One thing I still don't understand
How the four collared animals are linked to rows of the capture data.
The code assigns telemetry locations to individuals 1-4 (`inds`, lines
343-345), so it assumes the collared martens are the first four captured
individuals in `capt.txt`. Nothing in the shared files says so, and if
it's wrong, σ is shared with the wrong activity centres. I'd want the
paper's methods (or the authors) to confirm it before reading much into
any difference.
